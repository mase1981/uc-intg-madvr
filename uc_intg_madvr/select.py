"""
MadVR Select entities.

:copyright: (c) 2025 by Meir Miyara
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from typing import Any

from ucapi import StatusCodes
from ucapi.select import Select, Attributes, Commands, States

from uc_intg_madvr.config import MadVRConfig
from uc_intg_madvr.device import MadVRDevice
from uc_intg_madvr import const

_LOG = logging.getLogger(__name__)


class MadVRAspectRatioSelect(Select):
    """Select entity for MadVR aspect ratio mode."""

    # Available aspect ratio modes
    ASPECT_RATIO_OPTIONS = [
        "Auto",
        "Hold",
        "4:3",
        "16:9",
        "1.85:1",
        "2.00:1",
        "2.35:1",
        "2.40:1",
        "2.55:1",
        "2.76:1",
    ]

    def __init__(self, config: MadVRConfig, device: MadVRDevice):
        """Initialize aspect ratio select entity.

        Args:
            config: MadVR configuration
            device: MadVR device instance
        """
        self._config = config
        self._device = device

        entity_id = f"select.{config.host.replace('.', '_')}.aspect_ratio_mode"

        attributes = {
            Attributes.STATE: States.UNKNOWN,
            Attributes.OPTIONS: self.ASPECT_RATIO_OPTIONS,
            Attributes.CURRENT_OPTION: "Auto"
        }

        super().__init__(
            identifier=entity_id,
            name=f"{config.name} Aspect Mode",
            attributes=attributes,
            cmd_handler=self.handle_command
        )

        _LOG.info(f"Created aspect ratio select entity: {entity_id}")

    async def handle_command(self, entity: Select, command: str, params: dict[str, Any] | None = None) -> StatusCodes:
        """Handle commands from the remote.

        Args:
            entity: The select entity instance
            command: Command to execute
            params: Optional command parameters

        Returns:
            Status code indicating success or failure
        """
        _LOG.info(f"Aspect ratio select command: {command}, params: {params}")

        try:
            if command == Commands.SELECT_OPTION:
                option = params.get("option") if params else None
                return await self._select_aspect_mode(option)
            elif command == Commands.SELECT_NEXT:
                return await self._select_next()
            elif command == Commands.SELECT_PREVIOUS:
                return await self._select_previous()
            elif command == Commands.SELECT_FIRST:
                return await self._select_aspect_mode(self.ASPECT_RATIO_OPTIONS[0])
            elif command == Commands.SELECT_LAST:
                return await self._select_aspect_mode(self.ASPECT_RATIO_OPTIONS[-1])
            else:
                _LOG.warning(f"Unsupported command: {command}")
                return StatusCodes.BAD_REQUEST

        except Exception as e:
            _LOG.error(f"Error executing command {command}: {e}", exc_info=True)
            return StatusCodes.SERVER_ERROR

    async def _select_aspect_mode(self, mode: str) -> StatusCodes:
        """Select a specific aspect ratio mode.

        Args:
            mode: Aspect ratio mode to select

        Returns:
            Status code indicating success or failure
        """
        if not mode or mode not in self.ASPECT_RATIO_OPTIONS:
            _LOG.error(f"Invalid aspect ratio mode: {mode}")
            return StatusCodes.BAD_REQUEST

        _LOG.info(f"Setting aspect ratio mode to: {mode}")

        # Map display names to API values
        api_value = self._map_mode_to_api(mode)

        # Send command to device
        result = await self._device.send_command(f"{const.CMD_SET_ASPECT_RATIO_MODE} {api_value}")

        if result["success"]:
            # Update device state
            self._device.set_aspect_ratio_mode(mode)
            _LOG.info(f"Aspect ratio mode set to: {mode}")
            return StatusCodes.OK
        else:
            _LOG.error(f"Failed to set aspect ratio mode: {result.get('error')}")
            return StatusCodes.SERVER_ERROR

    async def _select_next(self) -> StatusCodes:
        """Select the next aspect ratio mode."""
        current = self.attributes[Attributes.CURRENT_OPTION]

        try:
            current_index = self.ASPECT_RATIO_OPTIONS.index(current)
            next_index = (current_index + 1) % len(self.ASPECT_RATIO_OPTIONS)
            next_mode = self.ASPECT_RATIO_OPTIONS[next_index]

            _LOG.info(f"Selecting next aspect mode: {next_mode}")
            return await self._select_aspect_mode(next_mode)
        except (ValueError, IndexError) as e:
            _LOG.error(f"Error selecting next mode: {e}")
            return StatusCodes.SERVER_ERROR

    async def _select_previous(self) -> StatusCodes:
        """Select the previous aspect ratio mode."""
        current = self.attributes[Attributes.CURRENT_OPTION]

        try:
            current_index = self.ASPECT_RATIO_OPTIONS.index(current)
            prev_index = (current_index - 1) % len(self.ASPECT_RATIO_OPTIONS)
            prev_mode = self.ASPECT_RATIO_OPTIONS[prev_index]

            _LOG.info(f"Selecting previous aspect mode: {prev_mode}")
            return await self._select_aspect_mode(prev_mode)
        except (ValueError, IndexError) as e:
            _LOG.error(f"Error selecting previous mode: {e}")
            return StatusCodes.SERVER_ERROR

    def _map_mode_to_api(self, mode: str) -> str:
        """Map display mode name to API value.

        Args:
            mode: Display mode name

        Returns:
            API value for the mode
        """
        # Most modes are the same, just return as-is
        # The API expects exactly these values
        return mode
