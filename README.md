# madVR Envy Integration for Unfolded Circle Remote 2/3

Control your madVR Envy video processor directly from your Unfolded Circle Remote 2 or Remote 3 with comprehensive control over picture settings, aspect ratios, tone mapping, menu navigation, and real-time device status monitoring.

![madVR](https://img.shields.io/badge/madVR-Envy-red)
![License](https://img.shields.io/badge/license-MPL--2.0-blue)
[![Discord](https://badgen.net/discord/online-members/zGVYf58)](https://discord.gg/zGVYf58)
![GitHub Release](https://img.shields.io/github/v/release/mase1981/uc-intg-madvr)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/mase1981/uc-intg-madvr/total)
[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://buymeacoffee.com/meirmiyara)
[![PayPal](https://img.shields.io/badge/PayPal-donate-blue.svg)](https://paypal.me/mmiyara)
[![Github Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-30363D?&logo=GitHub-Sponsors&logoColor=EA4AAA)](https://github.com/sponsors/mase1981/button)

## Features

This integration provides comprehensive control of your madVR Envy video processor with real-time status monitoring, advanced picture controls, and complete menu navigation directly from your Unfolded Circle Remote.

---
## ❤️ Support Development ❤️

If you find this integration useful, consider supporting development:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-pink?style=for-the-badge&logo=github)](https://github.com/sponsors/mase1981)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/meirmiyara)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/mmiyara)

Your support helps maintain this integration. Thank you! ❤️
---

### 🎮 **Remote Control Entity** (Primary Control) (Media Player is for state pulling only and have no other function)

#### **Power Management**
- **Standby** - Enter low-power standby mode (network responsive)
- **Power Off** - Complete power off
- **Restart** - Full device restart
- **Reload Software** - Quick software reload (2-3 seconds)

#### **Menu Navigation**
- **D-Pad Control** - Full directional navigation (Up, Down, Left, Right, OK)
- **Menu Access** - Quick access to Info, Settings, Configuration, Profiles
- **Back/Close** - Navigation controls
- **Test Patterns** - Direct access to test pattern menu

#### **Aspect Ratio Control**
- **Auto Mode** - Automatic aspect ratio detection
- **Hold Mode** - Freeze current aspect ratio
- **8 Preset Ratios** - 4:3, 16:9, 1.85:1, 2.00:1, 2.35:1, 2.40:1, 2.55:1, 2.76:1
- **One-Touch Selection** - Instant aspect ratio switching

#### **Picture Settings**
- **Tone Mapping** - Toggle, On, Off controls
- **Highlight Recovery** - Toggle enhancement
- **Shadow Recovery** - Toggle enhancement
- **Contrast Recovery** - Toggle enhancement
- **3DLUT** - Toggle 3D lookup tables
- **Histogram** - Toggle display
- **Debug OSD** - Toggle debug overlay

#### **Test Patterns**
- **Open Test Patterns Menu** - Direct access
- **Color Buttons** - Red, Green, Blue, Yellow, Magenta, Cyan
- **Quick Access** - Instant test pattern display

#### **Device Information Queries**
- **Signal Info** - Incoming signal details
- **Aspect Ratio** - Current aspect ratio
- **Temperatures** - GPU and CPU temperatures
- **MAC Address** - Device network ID
- **Masking Ratio** - Current masking information

#### **Utility Commands**
- **Force 1080p60** - Force output to 1080p60 (sync recovery)
- **Hotplug** - Issue HDMI hotplug event
- **Refresh License** - Refresh license information

### 📺 **Media Player Entity** (Status Display)

#### **Real-Time Status Monitoring**
- **Power State** - ON, STANDBY, or OFF status
- **Signal Information** - Resolution, frame rate, color space, HDR mode
- **Connection Status** - Device connectivity monitoring
- **Auto-Refresh** - Updates every 10 seconds

#### **Signal Details Display**
- **Resolution** - e.g., "3840x2160"
- **Frame Rate** - e.g., "23.976p"
- **Color Format** - e.g., "2D 422 10bit"
- **HDR Mode** - e.g., "HDR10 2020 TV 16:9"
- **No Signal Detection** - "No Signal (Standby)" status

### 🎯 **Single Device Architecture**

- **One Integration Instance** - Controls single madVR Envy device
- **Two Entities Created**:
  - **Remote Control** - Full device control via 7 UI pages
  - **Media Player** - Status display with power control
- **TCP Communication** - Direct device communication via port 44077
- **Persistent Connection** - Maintained with heartbeat monitoring

### **madVR Envy Requirements**
- **Firmware Version**: Any version with IP control enabled
- **Network Access**: Device must be accessible on local network
- **IP Control**: Enabled by default on port 44077
- **Connection Limit**: Supports up to 16 concurrent connections

### **Network Requirements**
- **Local Network Access** - Integration requires same network as madVR device
- **TCP Port** - Default 44077 (configurable)
- **Firewall Configuration** - Ensure port 44077 is accessible
- **Static IP Recommended** - Assign static IP to madVR device for reliability

## Installation

### Option 1: Remote Web Interface (Recommended)
1. Navigate to the [**Releases**](https://github.com/mase1981/uc-intg-madvr/releases) page
2. Download the latest `uc-intg-madvr-<version>.tar.gz` file
3. Open your remote's web interface (`http://your-remote-ip`)
4. Go to **Settings** → **Integrations** → **Add Integration**
5. Click **Upload** and select the downloaded `.tar.gz` file

### Option 2: Docker (Advanced Users)

The integration is available as a pre-built Docker image from GitHub Container Registry:

**Image**: `ghcr.io/mase1981/uc-intg-madvr:latest`

**Docker Compose:**
```yaml
services:
  uc-intg-madvr:
    image: ghcr.io/mase1981/uc-intg-madvr:latest
    container_name: uc-intg-madvr
    network_mode: host
    volumes:
      - </local/path>:/data
    environment:
      - UC_CONFIG_HOME=/data
      - UC_INTEGRATION_HTTP_PORT=9091
    restart: unless-stopped
```

**Docker Run:**
```bash
docker run -d --name=uc-intg-madvr --network host -v </local/path>:/data -e UC_CONFIG_HOME=/data -e UC_INTEGRATION_HTTP_PORT=9091 --restart unless-stopped ghcr.io/mase1981/uc-intg-madvr:latest
```

## Configuration

### Step 1: Prepare Your madVR Envy Device

**IMPORTANT**: madVR Envy must be powered on and accessible before adding the integration.

#### Verify madVR is Accessible:
1. Ensure madVR Envy is powered on
2. Note the IP address of your madVR device:
   - Check via madVR menu (Settings → Network)
   - Check your router's DHCP client list
   - Use network scanning tool (e.g., Angry IP Scanner)
3. **Assign Static IP** (highly recommended):
   - Configure static IP in router DHCP settings
   - Or set static IP in madVR network configuration

#### Verify IP Control:
- **IP Control Port**: 44077 (default, cannot be changed)
- **Connection Type**: TCP server
- **Test Connection**: Use telnet or TCP client:
  ```bash
  telnet YOUR_MADVR_IP 44077
  # Should see: WELCOME to Envy v1.x.x.x
  ```

### Step 2: Setup Integration

1. After installation, go to **Settings** → **Integrations**
2. The madVR Envy integration should appear in **Available Integrations**
3. Click **"Configure"** and follow the setup wizard:

   **Connection Configuration:**
   - **IP Address**: IP address of madVR Envy (e.g., 192.168.1.100)
   - **Port**: TCP port (default: 44077)
   - **Device Name**: Friendly name for device (e.g., "madVR Envy")
   - Click **Complete Setup**

4. Integration will test connection and create **TWO entities**:
   - **Remote Control**: `remote.[device_name]` - Full device control
   - **Media Player**: `media_player.[device_name]_status` - Status display

## Using the Integration

### Remote Control Entity (Primary Control)

The remote control entity provides complete madVR control across **7 dedicated pages**:

#### **Page 1: Power Control**
- **Standby** - Enter standby mode (still network responsive)
- **Power Off** - Complete power off
- **Restart** - Full device restart
- **Reload SW** - Quick software reload

#### **Page 2: Menu Navigation**
- **Menu Buttons** - Info, Settings, Config, Profiles
- **D-Pad Controls** - Up, Down, Left, Right, OK
- **Back** - Go back in menu
- **Close Menu** - Exit all menus

#### **Page 3: Aspect Ratio**
- **Auto/Hold Modes** - Automatic or manual control
- **8 Preset Ratios** - One-touch aspect ratio selection
- **Common Formats** - 4:3, 16:9, 2.35:1, 2.40:1, etc.

#### **Page 4: Picture Settings**
- **Tone Mapping** - Toggle, On, Off controls
- **Enhancement Toggles** - Highlight, Shadow, Contrast recovery
- **Processing Toggles** - 3DLUT, Histogram, Debug OSD

#### **Page 5: Test Patterns**
- **Open Patterns Menu** - Access test pattern library
- **Color Buttons** - Direct color pattern access
- **Quick Testing** - Instant pattern display

#### **Page 6: Device Info**
- **Signal Info** - Current input signal details
- **Aspect Ratio** - Current aspect ratio query
- **Temperatures** - Device temperature monitoring
- **MAC Address** - Network identification
- **Masking Ratio** - Current masking information

#### **Page 7: Utility**
- **Force 1080p60** - Force safe output mode
- **Hotplug** - Issue HDMI hotplug event
- **Refresh License** - Update license information

### Media Player Entity (Status Display)

The media player entity provides real-time device monitoring:

- **Power State Display**: Shows ON, STANDBY, or OFF
- **Signal Information**: Resolution, frame rate, color space
- **Auto-Update**: Refreshes status every 10 seconds
- **Status-Only**: No playback controls (device is video processor, not media player)
- **Power Controls**: ON/OFF buttons for basic power management

**Important**: The media player entity is for **status display only**. All functional control should be done via the **Remote Control entity**.

## Device Status Understanding

### Power States

The integration reports three distinct power states:

1. **ON** - Device is powered on with active video signal
   - Heartbeat responsive
   - Signal information available
   - Display shows: "3840x2160 23.976p 2D..."

2. **STANDBY** - Device is in low-power standby mode
   - Heartbeat responsive (network active)
   - No active video signal
   - Display shows: "No Signal (Standby)"

3. **OFF** - Device is completely powered off
   - No network response
   - Heartbeat fails
   - Display shows: "Powered Off"

### Signal Information Display

When a video signal is active, the media player displays detailed information:

**Format**: `Resolution FrameRate Dimension ColorSpace BitDepth HDRMode ColorGamut Range`

**Example**: `3840x2160 23.976p 2D 422 10bit HDR10 2020 TV 16:9`
- **3840x2160** - Resolution (4K)
- **23.976p** - Frame rate (film standard)
- **2D** - 2D content (vs 3D)
- **422** - Color sampling (4:2:2)
- **10bit** - Color depth
- **HDR10** - HDR format
- **2020** - Color gamut (Rec. 2020)
- **TV** - Range (TV vs PC)
- **16:9** - Display aspect ratio

## Troubleshooting

### Common Issues:

**1. "Connection Failed" During Setup**
- Verify madVR Envy is powered on
- Check IP address is correct
- Ping device: `ping YOUR_MADVR_IP`
- Test TCP connection: `telnet YOUR_MADVR_IP 44077`
- Confirm device is on same network as UC Remote
- Check firewall allows port 44077

**2. "Entity Unavailable After Reboot"**
- Integration fully supports reboot survival
- Configuration persists automatically
- Wait 30 seconds for device polling to resume
- If issue persists, restart integration from Settings
- Check integration logs for connection errors

**3. "Commands Not Responding"**
- Check device is powered on (not in full power off)
- Verify network connectivity
- Check integration logs for timeout errors
- Try sending Heartbeat command via Info page
- Restart integration if commands consistently fail

**4. "No Signal Information Displayed"**
- Ensure video source is connected and active
- Check HDMI cables are properly connected
- Verify input source is selected on madVR
- Allow 2-3 seconds for signal detection after source change
- Some sources may not provide full metadata

**5. "Status Shows 'Standby' When Device Appears On"**
- This is correct behavior when no video signal is present
- **ON state** = Active video signal processing
- **STANDBY state** = Device powered but no signal
- **OFF state** = Device completely off
- Check video source is actually outputting signal

**6. "Aspect Ratio Commands Not Working"**
- Aspect ratio only applies when video signal is active
- Check device is not in menu mode
- Some sources may override aspect ratio settings
- Try setting aspect ratio from device menu first
- Verify aspect ratio isn't locked in madVR settings

**7. "Temperatures Not Showing"**
- Query temperatures via Info page manually
- Some firmware versions may not report temperatures
- Check madVR menu for temperature display
- Temperatures only update when specifically queried

**8. "Remote Control Buttons Show Errors"**
- All commands should complete without errors
- Check integration logs for specific error messages
- Verify madVR firmware is up to date
- Some commands may not be supported on older firmware

### Debug Information

Enable detailed logging for troubleshooting:

**Docker Environment:**
```bash
# Add to docker-compose.yml environment section
- LOG_LEVEL=DEBUG

# View logs
docker logs uc-intg-madvr
```

**Integration Logs:**
- **Remote Interface**: Settings → Integrations → madVR Envy → View Logs
- Look for connection errors, command timeouts, or device responses
- Check for heartbeat failures indicating network issues

### Testing Connection Manually

**Using Telnet:**
```bash
telnet YOUR_MADVR_IP 44077
# Should see: WELCOME to Envy v1.x.x.x

# Try commands:
Heartbeat
# Should see: OK

GetIncomingSignalInfo
# Should see: Signal information or NoSignal

# Exit:
Bye
```

**Using Python:**
```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("YOUR_MADVR_IP", 44077))

# Read welcome
welcome = sock.recv(1024).decode()
print(welcome)  # Should show: WELCOME to Envy...

# Send heartbeat
sock.send(b"Heartbeat\r\n")
response = sock.recv(1024).decode()
print(response)  # Should show: OK

sock.close()
```

### Known Limitations

- **Single Device Only** - One madVR Envy per integration instance
- **No Audio Control** - madVR Envy is video processor only
- **No Playlist Control** - Not a media player
- **Command Feedback** - Some commands provide no response
- **Firmware Dependent** - Some features require specific firmware versions
- **Network Latency** - Commands may take 0.5-2 seconds to execute

## Advanced Configuration

### Custom Polling Intervals

Edit `madvr_config.json` in integration config directory:

```json
{
  "host": "192.168.1.100",
  "port": 44077,
  "name": "madVR Envy"
}
```

Polling interval is fixed at 10 seconds for optimal performance and minimal network traffic.

### Static IP Assignment

**Highly Recommended** for reliability:

**Option 1: Router DHCP Reservation**
1. Log into router admin interface
2. Find madVR device in DHCP client list
3. Create DHCP reservation for device MAC address
4. Reboot madVR device

**Option 2: madVR Static Configuration**
1. Access madVR menu: Settings → Network
2. Change from DHCP to Static IP
3. Enter IP address, subnet mask, gateway, DNS
4. Save and reboot device

### Multiple madVR Devices

For multiple madVR Envy devices, install separate integration instances:

**Docker Method:**
```yaml
services:
  madvr-theater:
    image: ghcr.io/mase1981/uc-intg-madvr:latest
    container_name: uc-intg-madvr-theater
    network_mode: host
    volumes:
      - /path/to/theater/config:/data
    environment:
      - UC_CONFIG_HOME=/data
      - UC_INTEGRATION_HTTP_PORT=9091
    restart: unless-stopped

  madvr-livingroom:
    image: ghcr.io/mase1981/uc-intg-madvr:latest
    container_name: uc-intg-madvr-livingroom
    network_mode: host
    volumes:
      - /path/to/livingroom/config:/data
    environment:
      - UC_CONFIG_HOME=/data
      - UC_INTEGRATION_HTTP_PORT=9092
    restart: unless-stopped
```

Each instance:
- Connects to different madVR device
- Uses separate configuration directory
- Uses different integration HTTP port

## For Developers

### Local Development

1. **Clone and setup:**
   ```bash
   git clone https://github.com/mase1981/uc-intg-madvr.git
   cd uc-intg-madvr
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configuration:**
   ```bash
   export UC_CONFIG_HOME=./config
   ```

3. **Run development:**
   ```bash
   python uc_intg_madvr/driver.py
   ```

4. **VS Code debugging:**
   - Open project in VS Code
   - Use F5 to start debugging session
   - Configure integration with real madVR device

### Project Structure

```
uc-intg-madvr/
├── uc_intg_madvr/          # Main package
│   ├── __init__.py         # Package info
│   ├── const.py            # Constants and commands
│   ├── device.py           # madVR device communication
│   ├── config.py           # Configuration management
│   ├── driver.py           # Main integration driver
│   ├── media_player.py     # Media player status entity
│   ├── remote.py           # Remote control entity
│   └── setup.py            # Setup wizard
├── .github/workflows/      # GitHub Actions CI/CD
│   └── build.yml           # Automated build pipeline
├── docker-compose.yml      # Docker deployment
├── Dockerfile              # Container build instructions
├── driver.json             # Integration metadata
├── requirements.txt        # Dependencies
├── pyproject.toml          # Python project config
└── README.md               # This file
```

### Key Implementation Details

#### **TCP Communication Protocol**
- Uses madVR IP Control Protocol (TCP port 44077)
- Text-based command/response protocol
- Commands terminated with `\r\n`
- Responses: `OK`, `ERROR "message"`, or data
- Heartbeat every 20 seconds to maintain connection
- Connection timeout after 60 seconds of inactivity

#### **Command Format**
```
Command [Parameter1] [Parameter2] ...⏎

Examples:
Heartbeat⏎
OpenMenu Settings⏎
KeyPress UP⏎
SetAspectRatioMode 2.35:1⏎
```

#### **Status Polling Architecture**
- **Device-Centric Model** - Single device class handles all communication
- **Event-Driven Updates** - Device emits events on state changes
- **Polling Loop** - Checks status every 10 seconds
- **Heartbeat Monitoring** - Determines device availability
- **Signal Detection** - Differentiates ON vs STANDBY states

#### **Power State Logic**
```python
# Heartbeat succeeds + Signal detected = ON
# Heartbeat succeeds + No signal = STANDBY
# Heartbeat fails = OFF
```

#### **Entity Architecture**
- **Media Player Entity** - Status display with minimal features
- **Remote Entity** - Full control with 7 UI pages
- **Device Class** - `DeviceClasses.RECEIVER` for media player
- **Command Suppression** - Returns `StatusCodes.OK` for all commands

#### **Reboot Survival Pattern**
```python
# Pre-initialize entities if config exists
if config.is_configured():
    asyncio.create_task(_initialize_entities())

# Reload config on reconnect
async def on_connect():
    config.reload_from_disk()
    if not device:
        await _initialize_entities()
```

### madVR IP Control Reference

Essential commands used by this integration:

```python
# Connection
Heartbeat                           # Keep-alive

# Power
PowerOff                            # Full power off
Standby                             # Enter standby mode
Restart                             # Restart device
ReloadSoftware                      # Reload software only

# Menu Navigation
OpenMenu Info                       # Open menu
OpenMenu Settings
OpenMenu Configuration
OpenMenu Profiles
OpenMenu TestPatterns
CloseMenu                           # Close menu
KeyPress UP|DOWN|LEFT|RIGHT|OK|BACK # Navigate

# Aspect Ratio
SetAspectRatioMode Auto             # Auto detect
SetAspectRatioMode Hold             # Hold current
SetAspectRatioMode 2.35:1           # Set specific ratio

# Information Queries
GetIncomingSignalInfo               # Signal details
GetAspectRatio                      # Current AR
GetTemperatures                     # Device temps
GetMacAddress                       # MAC address
GetMaskingRatio                     # Masking info

# Picture Settings
Toggle ToneMap                      # Toggle tone mapping
ToneMapOn                           # Enable tone mapping
ToneMapOff                          # Disable tone mapping
Toggle HighlightRecovery            # Toggle highlight recovery
Toggle ShadowRecovery               # Toggle shadow recovery
Toggle ContrastRecovery             # Toggle contrast recovery
Toggle 3DLUT                        # Toggle 3D LUT
Toggle Histogram                    # Toggle histogram
Toggle DebugOSD                     # Toggle debug OSD

# Utility
Force1080p60Output                  # Force safe mode
Hotplug                             # HDMI hotplug
RefreshLicenseInfo                  # Refresh license
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test with real madVR device
4. Commit changes: `git commit -m 'Add amazing feature'`
5. Push to branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

### Code Style

- Follow PEP 8 Python conventions
- Use type hints for all functions
- Async/await for all I/O operations
- Comprehensive docstrings
- Descriptive variable names
- Use absolute imports only

## Credits

- **Developer**: Meir Miyara
- **madVR Labs**: Advanced video processing technology
- **Unfolded Circle**: Remote 2/3 integration framework (ucapi)
- **Community**: Testing and feedback from UC community

## License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0) - see LICENSE file for details.

## Support & Community

- **GitHub Issues**: [Report bugs and request features](https://github.com/mase1981/uc-intg-madvr/issues)
- **UC Community Forum**: [General discussion and support](https://unfolded.community/)
- **madVR Forums**: [madVR community support](https://www.madVR.com/forum/)
- **Developer**: [Meir Miyara](https://www.linkedin.com/in/meirmiyara)

---

**Made with ❤️ for the Unfolded Circle and madVR Communities**

**Thank You**: Meir Miyara