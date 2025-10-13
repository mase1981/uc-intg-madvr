"""
Remote control entity for madVR Envy - Complete IP Control Implementation.

:copyright: (c) 2025 by Meir Miyara
:license: MPL-2.0, see LICENSE for more details.
"""

import asyncio
import logging
from typing import Any

from ucapi import StatusCodes
from ucapi.remote import Remote, Attributes, Commands, Features, States
from ucapi.ui import EntityCommand, Size, UiPage, create_ui_text

from uc_intg_madvr.config import MadVRConfig
from uc_intg_madvr.device import MadVRDevice
from uc_intg_madvr import const

_LOG = logging.getLogger(__name__)


class MadVRRemote(Remote):
    """Complete madVR Envy remote control with full IP control command set."""

    def __init__(self, config: MadVRConfig, device: MadVRDevice):
        self._config = config
        self._device = device

        entity_id = f"remote.{config.host.replace('.', '_')}"

        super().__init__(
            identifier=entity_id,
            name=config.name,
            features=[Features.ON_OFF, Features.SEND_CMD],
            attributes={Attributes.STATE: States.UNKNOWN},
            ui_pages=self._create_ui_pages(),
            cmd_handler=self.command_handler,
        )

        _LOG.info(f"Created remote entity: {entity_id}")

    async def command_handler(
        self, entity: Remote, cmd_id: str, params: dict[str, Any] | None = None
    ) -> StatusCodes:
        """Handle remote commands."""
        _LOG.info(f"Remote command: {cmd_id}, params: {params}")

        try:
            if cmd_id == Commands.ON:
                result = await self._device.send_command(const.CMD_STANDBY)
            elif cmd_id == Commands.OFF:
                result = await self._device.send_command(const.CMD_POWER_OFF)
            
            elif cmd_id == Commands.SEND_CMD:
                if not params or "command" not in params:
                    _LOG.error("send_cmd received without command parameter")
                    return StatusCodes.BAD_REQUEST
                
                command = params["command"]
                result = await self._device.send_command(command)
            
            else:
                _LOG.warning(f"Unknown command: {cmd_id}")
                return StatusCodes.NOT_IMPLEMENTED

            await asyncio.sleep(const.COMMAND_DELAY)

            return StatusCodes.OK if result["success"] else StatusCodes.SERVER_ERROR

        except Exception as e:
            _LOG.error(f"Command failed: {e}", exc_info=True)
            return StatusCodes.SERVER_ERROR

    def _create_ui_pages(self) -> list[UiPage]:
        """Create all remote UI pages."""
        return [
            self._create_power_page(),
            self._create_menu_navigation_page(),
            self._create_aspect_ratio_page(),
            self._create_picture_settings_page(),
            self._create_test_patterns_page(),
            self._create_info_page(),
            self._create_utility_page(),
        ]

    def _create_power_page(self) -> UiPage:
        """Power control page."""
        items = [
            create_ui_text("Power Control", 0, 0, size=Size(4, 1)),
            create_ui_text("Standby", 0, 1, cmd=EntityCommand("send_cmd", {"command": const.CMD_STANDBY})),
            create_ui_text("Power Off", 1, 1, cmd=EntityCommand("send_cmd", {"command": const.CMD_POWER_OFF})),
            create_ui_text("Restart", 2, 1, cmd=EntityCommand("send_cmd", {"command": const.CMD_RESTART})),
            create_ui_text("Reload SW", 3, 1, cmd=EntityCommand("send_cmd", {"command": const.CMD_RELOAD_SOFTWARE})),
        ]
        return UiPage(page_id="power", name="Power", grid=Size(4, 6), items=items)

    def _create_menu_navigation_page(self) -> UiPage:
        """Menu navigation and D-Pad control page."""
        items = [
            create_ui_text("Menu Navigation", 0, 0, size=Size(4, 1)),
            
            create_ui_text("Info", 0, 1, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_OPEN_MENU} {const.MENU_INFO}"})),
            create_ui_text("Settings", 1, 1, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_OPEN_MENU} {const.MENU_SETTINGS}"})),
            create_ui_text("Config", 2, 1, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_OPEN_MENU} {const.MENU_CONFIGURATION}"})),
            create_ui_text("Profiles", 3, 1, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_OPEN_MENU} {const.MENU_PROFILES}"})),
            
            create_ui_text("D-Pad Control", 0, 2, size=Size(4, 1)),
            create_ui_text("↑", 1, 3, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_KEY_PRESS} {const.KEY_UP}"})),
            create_ui_text("←", 0, 4, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_KEY_PRESS} {const.KEY_LEFT}"})),
            create_ui_text("OK", 1, 4, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_KEY_PRESS} {const.KEY_OK}"})),
            create_ui_text("→", 2, 4, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_KEY_PRESS} {const.KEY_RIGHT}"})),
            create_ui_text("↓", 1, 5, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_KEY_PRESS} {const.KEY_DOWN}"})),
            create_ui_text("Back", 3, 4, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_KEY_PRESS} {const.KEY_BACK}"})),
            create_ui_text("Close", 3, 5, cmd=EntityCommand("send_cmd", {"command": const.CMD_CLOSE_MENU})),
        ]
        return UiPage(page_id="menu", name="Menu", grid=Size(4, 6), items=items)

    def _create_aspect_ratio_page(self) -> UiPage:
        """Aspect ratio control page."""
        items = [
            create_ui_text("Aspect Ratio", 0, 0, size=Size(4, 1)),
            
            create_ui_text("Auto", 0, 1, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_SET_ASPECT_RATIO_MODE} {const.AR_AUTO}"})),
            create_ui_text("Hold", 1, 1, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_SET_ASPECT_RATIO_MODE} {const.AR_HOLD}"})),
            
            create_ui_text("Common Ratios", 0, 2, size=Size(4, 1)),
        ]
        
        ratios = [
            ("4:3", const.AR_4_3), ("16:9", const.AR_16_9),
            ("1.85:1", const.AR_1_85), ("2.00:1", const.AR_2_00),
            ("2.35:1", const.AR_2_35), ("2.40:1", const.AR_2_40),
            ("2.55:1", const.AR_2_55), ("2.76:1", const.AR_2_76),
        ]
        
        row, col = 3, 0
        for label, ratio in ratios:
            items.append(create_ui_text(
                label, col, row,
                cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_SET_ASPECT_RATIO_MODE} {ratio}"})
            ))
            col += 1
            if col >= 4:
                col, row = 0, row + 1
        
        return UiPage(page_id="aspect", name="Aspect", grid=Size(4, 6), items=items)

    def _create_picture_settings_page(self) -> UiPage:
        """Picture settings and tone mapping page."""
        items = [
            create_ui_text("Picture Settings", 0, 0, size=Size(4, 1)),
            
            create_ui_text("ToneMap", 0, 1, size=Size(2, 1), cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_TOGGLE} {const.TOGGLE_TONE_MAP}"})),
            create_ui_text("TM On", 0, 2, cmd=EntityCommand("send_cmd", {"command": const.CMD_TONE_MAP_ON})),
            create_ui_text("TM Off", 1, 2, cmd=EntityCommand("send_cmd", {"command": const.CMD_TONE_MAP_OFF})),
            
            create_ui_text("Highlight", 2, 2, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_TOGGLE} {const.TOGGLE_HIGHLIGHT_RECOVERY}"})),
            create_ui_text("Shadow", 3, 2, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_TOGGLE} {const.TOGGLE_SHADOW_RECOVERY}"})),
            create_ui_text("Contrast", 0, 3, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_TOGGLE} {const.TOGGLE_CONTRAST_RECOVERY}"})),
            create_ui_text("3DLUT", 1, 3, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_TOGGLE} {const.TOGGLE_3DLUT}"})),
            create_ui_text("Histogram", 2, 3, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_TOGGLE} {const.TOGGLE_HISTOGRAM}"})),
            create_ui_text("Debug", 3, 3, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_TOGGLE} {const.TOGGLE_DEBUG_OSD}"})),
        ]
        return UiPage(page_id="picture", name="Picture", grid=Size(4, 6), items=items)

    def _create_test_patterns_page(self) -> UiPage:
        """Test patterns and color buttons page."""
        items = [
            create_ui_text("Test Patterns", 0, 0, size=Size(4, 1)),
            create_ui_text("Open", 0, 1, size=Size(2, 1), cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_OPEN_MENU} {const.MENU_TEST_PATTERNS}"})),
            
            create_ui_text("Color Buttons", 0, 2, size=Size(4, 1)),
            create_ui_text("Red", 0, 3, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_KEY_PRESS} {const.KEY_RED}"})),
            create_ui_text("Green", 1, 3, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_KEY_PRESS} {const.KEY_GREEN}"})),
            create_ui_text("Blue", 2, 3, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_KEY_PRESS} {const.KEY_BLUE}"})),
            create_ui_text("Yellow", 3, 3, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_KEY_PRESS} {const.KEY_YELLOW}"})),
            create_ui_text("Magenta", 0, 4, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_KEY_PRESS} {const.KEY_MAGENTA}"})),
            create_ui_text("Cyan", 1, 4, cmd=EntityCommand("send_cmd", {"command": f"{const.CMD_KEY_PRESS} {const.KEY_CYAN}"})),
        ]
        return UiPage(page_id="test", name="Test", grid=Size(4, 6), items=items)

    def _create_info_page(self) -> UiPage:
        """Device information query page."""
        items = [
            create_ui_text("Device Info", 0, 0, size=Size(4, 1)),
            create_ui_text("Signal", 0, 1, size=Size(2, 1), cmd=EntityCommand("send_cmd", {"command": const.CMD_GET_SIGNAL_INFO})),
            create_ui_text("Aspect", 2, 1, size=Size(2, 1), cmd=EntityCommand("send_cmd", {"command": const.CMD_GET_ASPECT_RATIO})),
            create_ui_text("Temp", 0, 2, size=Size(2, 1), cmd=EntityCommand("send_cmd", {"command": const.CMD_GET_TEMPERATURES})),
            create_ui_text("MAC", 2, 2, size=Size(2, 1), cmd=EntityCommand("send_cmd", {"command": const.CMD_GET_MAC_ADDRESS})),
            create_ui_text("Masking", 0, 3, size=Size(2, 1), cmd=EntityCommand("send_cmd", {"command": const.CMD_GET_MASKING_RATIO})),
        ]
        return UiPage(page_id="info", name="Info", grid=Size(4, 6), items=items)

    def _create_utility_page(self) -> UiPage:
        """Utility and diagnostic commands page."""
        items = [
            create_ui_text("Utility", 0, 0, size=Size(4, 1)),
            create_ui_text("Force 1080p60", 0, 1, size=Size(2, 1), cmd=EntityCommand("send_cmd", {"command": const.CMD_FORCE_1080P60})),
            create_ui_text("Hotplug", 2, 1, size=Size(2, 1), cmd=EntityCommand("send_cmd", {"command": const.CMD_HOTPLUG})),
            create_ui_text("Refresh Lic", 0, 2, size=Size(2, 1), cmd=EntityCommand("send_cmd", {"command": const.CMD_REFRESH_LICENSE})),
        ]
        return UiPage(page_id="utility", name="Utility", grid=Size(4, 6), items=items)