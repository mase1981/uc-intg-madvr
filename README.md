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
- **madVR Forums**: [madVR community support](https://www.madvr.com/forum/)
- **Developer**: [Meir Miyara](https://www.linkedin.com/in/meirmiyara)

---

**Made with ❤️ for the Unfolded Circle and madVR Communities**

**Thank You**: Meir Miyara
