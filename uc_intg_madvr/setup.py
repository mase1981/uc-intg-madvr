"""
Setup flow handler for madVR Envy integration.

:copyright: (c) 2025 by Meir Miyara
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
import asyncio
from typing import Callable, Awaitable

from ucapi import IntegrationSetupError, SetupAction, SetupComplete, SetupDriver
from ucapi.api_definitions import (
    AbortDriverSetup,
    DriverSetupRequest,
    RequestUserInput,
    UserDataResponse,
    SetupError,
)

from uc_intg_madvr.device import MadVRDevice
from uc_intg_madvr.config import MadVRConfig
from uc_intg_madvr import const

_LOG = logging.getLogger(__name__)


class MadVRSetup:
    """Setup flow manager for madVR integration."""

    def __init__(self, api, config: MadVRConfig, on_setup_complete: Callable[[], Awaitable[None]]):
        self._api = api
        self._config = config
        self._on_setup_complete = on_setup_complete
        _LOG.info("MadVRSetup initialized")

    async def handle_setup(self, msg: SetupDriver) -> SetupAction:
        """Handle setup flow messages."""
        _LOG.info("=" * 70)
        _LOG.info("SETUP: Received message type: %s", type(msg).__name__)
        _LOG.info("=" * 70)
        
        if isinstance(msg, DriverSetupRequest):
            _LOG.info("SETUP: Handling DriverSetupRequest")
            # Values come from the saved config (empty on a first setup).
            return self._form()

        elif isinstance(msg, UserDataResponse):
            _LOG.info("SETUP: Handling UserDataResponse")
            _LOG.info("SETUP: Input values: %s", msg.input_values)
            action = await self._handle_user_input(msg.input_values)
            
            if isinstance(action, SetupComplete) and self._on_setup_complete:
                await self._on_setup_complete()
                
            return action
        
        elif isinstance(msg, AbortDriverSetup):
            _LOG.info("SETUP: Setup aborted by user")
            return SetupError(IntegrationSetupError.OTHER)
        
        else:
            _LOG.error("SETUP: Unknown message type: %s", type(msg).__name__)
            return SetupError(IntegrationSetupError.OTHER)

    def _form(self, error: str = "", values: dict | None = None) -> RequestUserInput:
        """The connection form, with an optional problem shown at the top.

        :param values: what the user typed; defaults to the saved configuration
        """
        if values is None:
            values = {
                "host": self._config.host or "",
                "port": self._config.port or const.DEFAULT_PORT,
                "name": self._config.name or "madVR Envy",
                "polling_mode": self._config.polling_mode,
                "polling_interval": self._config.polling_interval,
            }
        settings = []
        if error:
            settings.append({
                "id": "error",
                "label": {"en": "Problem"},
                "field": {"label": {"value": {"en": error}}},
            })
        settings += [
            {
                "id": "host",
                "label": {"en": "IP Address"},
                "field": {"text": {"value": values["host"]}}
            },
            {
                "id": "port",
                "label": {"en": "Port"},
                "field": {"number": {"value": values["port"]}}
            },
            {
                "id": "name",
                "label": {"en": "Device Name"},
                "field": {"text": {"value": values["name"]}}
            },
            {
                "id": "polling_mode",
                "label": {"en": "Polling Mode"},
                "field": {
                    "dropdown": {
                        "value": values["polling_mode"],
                        "items": [
                            {"id": "enabled", "label": {"en": "Enabled (polls at interval)"}},
                            {"id": "on_demand", "label": {"en": "On-demand (only when viewing)"}},
                            {"id": "disabled", "label": {"en": "Disabled (saves battery)"}},
                        ]
                    }
                }
            },
            {
                "id": "polling_info",
                "label": {"en": ""},
                "field": {
                    "label": {
                        "value": {
                            "en": "Polling is used for data not available via push notifications (currently temperature sensors only). Disabling polling improves battery life. On-demand fetches data only when actively viewing the sensor."
                        }
                    }
                }
            },
            {
                "id": "polling_interval",
                "label": {"en": "Polling Interval (seconds)"},
                "field": {"number": {"value": values["polling_interval"], "min": const.MIN_POLL_INTERVAL}}
            }
        ]
        return RequestUserInput(title={"en": "madVR Envy Connection"}, settings=settings)

    async def _handle_user_input(self, input_values: dict[str, str]) -> SetupAction:
        """Process user input from setup form.

        The connection is tested with a configuration kept in memory; the saved
        configuration (which the running device uses) only changes once the test passes.
        Problems are shown on the form, keeping what the user typed.
        """
        _LOG.info("SETUP: Processing user input")

        host = str(input_values.get("host") or "").strip()
        port_str = str(input_values.get("port") or const.DEFAULT_PORT).strip()
        name = str(input_values.get("name") or "").strip() or "madVR Envy"
        polling_mode = input_values.get("polling_mode") or "enabled"
        try:
            polling_interval = int(float(input_values.get("polling_interval") or const.DEFAULT_POLL_INTERVAL))
        except (ValueError, TypeError):
            polling_interval = const.DEFAULT_POLL_INTERVAL
        values = {
            "host": host,
            "port": port_str,
            "name": name,
            "polling_mode": polling_mode,
            "polling_interval": polling_interval,
        }

        _LOG.info("SETUP: Host=%s, Port=%s, Name=%s", host, port_str, name)

        if not host:
            _LOG.error("SETUP: No host provided")
            return self._form("Enter the Envy's IP address.", values)

        try:
            port = int(float(port_str))
            if port < 1 or port > 65535:
                raise ValueError("Invalid port range")
        except (ValueError, TypeError) as e:
            _LOG.error("SETUP: Invalid port '%s': %s", port_str, e)
            return self._form(f"The port '{port_str}' is not valid. The Envy uses port {const.DEFAULT_PORT}.", values)

        _LOG.info("SETUP: Testing connection to %s:%d", host, port)

        test_config = MadVRConfig(persist=False)
        test_config.set_config(host, port, name)

        loop = asyncio.get_running_loop()
        test_device = MadVRDevice(test_config, loop)

        try:
            result = await test_device.send_command(const.CMD_HEARTBEAT)
            if not result["success"]:
                _LOG.error("SETUP: Failed to connect to madVR device: %s", result.get("error"))
                return self._form(
                    f"No connection to the Envy at {host}:{port}. It must be powered on (not in standby) "
                    "during setup. Check the IP address, and that the Remote and the Envy are on the same network.",
                    values,
                )

            _LOG.info("SETUP: Successfully connected to madVR device")

            _LOG.info("SETUP: Fetching MAC address for Wake-on-LAN...")
            await test_device._fetch_mac_address()
        except Exception as e:
            _LOG.error("SETUP: Connection test failed: %s", e, exc_info=True)
            return self._form(f"Setup failed: {e}", values)
        finally:
            try:
                await test_device.stop()
            except Exception:
                pass

        # Test passed: save. The device ID (entity IDs) is kept from an existing configuration.
        self._config.set_config(host, port, name)
        self._config.set_polling_config(polling_mode, polling_interval)
        if test_config.mac_address:
            _LOG.info("SETUP: MAC address retrieved: %s", test_config.mac_address)
            self._config.set_mac_address(test_config.mac_address)
        else:
            _LOG.warning("SETUP: Could not fetch MAC address, WOL may not work")

        _LOG.info("SETUP: Configuration saved successfully")
        _LOG.info("=" * 70)
        return SetupComplete()
