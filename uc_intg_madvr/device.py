"""
madVR Envy device handler with polling and event management.

:copyright: (c) 2025 by Meir Miyara
:license: MPL-2.0, see LICENSE for more details.
"""

import asyncio
import logging
import socket
from enum import IntEnum, StrEnum
from asyncio import AbstractEventLoop
from pyee.asyncio import AsyncIOEventEmitter

from uc_intg_madvr.config import MadVRConfig
from uc_intg_madvr import const

_LOG = logging.getLogger(__name__)


class EVENTS(IntEnum):
    """Device events."""
    UPDATE = 1


class PowerState(StrEnum):
    """Power states for madVR device."""
    OFF = "OFF"
    ON = "ON"
    STANDBY = "STANDBY"
    UNKNOWN = "UNKNOWN"


class MadVRDevice:
    """madVR Envy device with polling and TCP communication."""

    def __init__(self, config: MadVRConfig, loop: AbstractEventLoop | None = None):
        self._loop: AbstractEventLoop = loop or asyncio.get_running_loop()
        self.events = AsyncIOEventEmitter(self._loop)
        self._config = config
        self._state: PowerState = PowerState.UNKNOWN
        self._signal_info: str = "Unknown"
        self._is_polling = False
        self._lock = asyncio.Lock()
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None

    @property
    def identifier(self) -> str:
        """Device identifier based on IP address."""
        return self._config.host.replace('.', '_')

    @property
    def name(self) -> str:
        """Device name from configuration."""
        return self._config.name

    @property
    def state(self) -> PowerState:
        """Current power state."""
        return self._state

    @property
    def signal_info(self) -> str:
        """Current signal information."""
        return self._signal_info

    async def start_polling(self):
        """Start the polling loop."""
        if self._is_polling:
            return
        self._is_polling = True
        
        if not self._config.mac_address:
            await self._fetch_mac_address()
        
        self._loop.create_task(self._poll_loop())
        _LOG.info(f"[{self.name}] Started polling")

    async def stop_polling(self):
        """Stop the polling loop."""
        self._is_polling = False
        await self._disconnect()
        _LOG.info(f"[{self.name}] Stopped polling")

    async def _poll_loop(self):
        """Continuous polling loop."""
        while self._is_polling:
            try:
                await self.update()
                await asyncio.sleep(const.POLL_INTERVAL)
            except asyncio.CancelledError:
                break
            except Exception as e:
                _LOG.error(f"[{self.name}] Polling error: {e}")
                await asyncio.sleep(const.POLL_INTERVAL)

    async def update(self):
        """Update device state and emit events if changed."""
        try:
            heartbeat_result = await self._send_command(
                const.CMD_HEARTBEAT, 
                timeout=const.COMMAND_TIMEOUT
            )
            
            if heartbeat_result["success"]:
                signal_result = await self._send_command(
                    const.CMD_GET_SIGNAL_INFO, 
                    timeout=const.COMMAND_TIMEOUT
                )
                
                if signal_result["success"] and signal_result.get("data"):
                    signal_data = signal_result["data"]
                    
                    if const.NO_SIGNAL in signal_data or const.RESPONSE_ERROR in signal_data:
                        new_state = PowerState.STANDBY
                        self._signal_info = "No Signal (Standby)"
                    else:
                        new_state = PowerState.ON
                        parts = signal_data.split()
                        if len(parts) > 1:
                            self._signal_info = " ".join(parts[1:5])
                        else:
                            self._signal_info = "Signal Active"
                else:
                    new_state = PowerState.STANDBY
                    self._signal_info = "Standby Mode"
            else:
                new_state = PowerState.OFF
                self._signal_info = "Powered Off"

            if self._state != new_state or self._signal_info != self._signal_info:
                old_state = self._state
                self._state = new_state
                
                _LOG.info(f"[{self.name}] State: {old_state} → {new_state}, Signal: {self._signal_info}")
                
                self.events.emit(EVENTS.UPDATE, self.identifier, {
                    "state": self._state,
                    "signal_info": self._signal_info
                })
            
        except Exception as e:
            _LOG.error(f"[{self.name}] Update failed: {e}")
            if self._state != PowerState.OFF:
                self._state = PowerState.OFF
                self._signal_info = "Connection Error"
                self.events.emit(EVENTS.UPDATE, self.identifier, {
                    "state": self._state,
                    "signal_info": self._signal_info
                })

    async def send_command(self, command: str) -> dict:
        """Send command to device (public interface)."""
        if command == const.CMD_STANDBY and self._state == PowerState.OFF:
            return await self._wake_on_lan()
        return await self._send_command(command)

    async def _send_command(self, command: str, timeout: float = None) -> dict:
        """Send command to madVR device with automatic reconnection."""
        if timeout is None:
            timeout = const.COMMAND_TIMEOUT
            
        async with self._lock:
            try:
                if not await self._ensure_connected():
                    return {"success": False, "error": "Connection failed"}

                _LOG.debug(f"[{self.name}] Sending: {command}")
                self._writer.write(f"{command}\r\n".encode())
                await self._writer.drain()

                try:
                    response_line = await asyncio.wait_for(
                        self._reader.readline(),
                        timeout=timeout
                    )
                    response = response_line.decode().strip()
                    _LOG.debug(f"[{self.name}] Received: {response}")

                    if response.startswith(const.RESPONSE_OK):
                        return {"success": True}
                    elif response.startswith(const.RESPONSE_ERROR):
                        error_msg = response.replace(const.RESPONSE_ERROR, "").strip().strip('"')
                        return {"success": False, "error": error_msg}
                    else:
                        return {"success": True, "data": response}

                except asyncio.TimeoutError:
                    _LOG.warning(f"[{self.name}] Command timeout: {command}")
                    await self._disconnect()
                    return {"success": False, "error": "Timeout"}

            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as e:
                _LOG.error(f"[{self.name}] Network error: {e}")
                await self._disconnect()
                return {"success": False, "error": f"Network error: {e.__class__.__name__}"}

            except Exception as e:
                _LOG.error(f"[{self.name}] Command failed: {e}")
                await self._disconnect()
                return {"success": False, "error": str(e)}

    async def _ensure_connected(self) -> bool:
        """Ensure TCP connection is established."""
        if self._writer and not self._writer.is_closing():
            return True

        try:
            _LOG.info(f"[{self.name}] Connecting to {self._config.host}:{self._config.port}")
            
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self._config.host, self._config.port),
                timeout=const.CONNECTION_TIMEOUT
            )

            welcome = await asyncio.wait_for(
                self._reader.readline(), 
                timeout=const.COMMAND_TIMEOUT
            )
            welcome_msg = welcome.decode().strip()
            _LOG.info(f"[{self.name}] Connected: {welcome_msg}")
            
            return True

        except Exception as e:
            _LOG.error(f"[{self.name}] Connection failed: {e}")
            await self._disconnect()
            return False

    async def _disconnect(self):
        """Close TCP connection."""
        if self._writer:
            try:
                self._writer.close()
                await self._writer.wait_closed()
            except Exception as e:
                _LOG.debug(f"[{self.name}] Disconnect error: {e}")
            finally:
                self._writer = None
                self._reader = None

    async def _fetch_mac_address(self):
        """Fetch and store device MAC address."""
        try:
            result = await self._send_command(const.CMD_GET_MAC_ADDRESS)
            if result["success"] and result.get("data"):
                mac_line = result["data"]
                if mac_line.startswith("MacAddress"):
                    mac_address = mac_line.split()[1]
                    self._config.set_mac_address(mac_address)
                    _LOG.info(f"[{self.name}] MAC address stored: {mac_address}")
        except Exception as e:
            _LOG.error(f"[{self.name}] Failed to fetch MAC address: {e}")

    async def _wake_on_lan(self) -> dict:
        """Send Wake-on-LAN magic packet."""
        mac_address = self._config.mac_address
        if not mac_address:
            _LOG.error(f"[{self.name}] No MAC address available for WOL")
            return {"success": False, "error": "No MAC address"}

        try:
            mac_bytes = bytes.fromhex(mac_address.replace("-", "").replace(":", ""))
            magic_packet = b'\xff' * 6 + mac_bytes * 16

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, ('<broadcast>', 9))
            sock.close()

            _LOG.info(f"[{self.name}] Wake-on-LAN packet sent to {mac_address}")
            
            await asyncio.sleep(3)
            
            return {"success": True}

        except Exception as e:
            _LOG.error(f"[{self.name}] Wake-on-LAN failed: {e}")
            return {"success": False, "error": str(e)}