# Aura

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PlatformIO](https://img.shields.io/badge/PlatformIO-Ready-orange.svg)](https://platformio.org/)
[![ESP32](https://img.shields.io/badge/ESP32-Supported-green.svg)](https://www.espressif.com/en/products/socs/esp32)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-blueviolet.svg)](https://docs.astral.sh/uv/)

A beautiful, feature-rich weather widget for ESP32-2432S028R (CYD - Cheap Yellow Display) devices with a 2.8" ILI9341 touchscreen.

> 📦 **Complete Project**: This repository contains the source code. For the 3D printable case design and full assembly instructions, visit:
> [MakerWorld - Aura Smart Weather Forecast Display](https://makerworld.com/en/models/1382304-aura-smart-weather-forecast-display)

---

## ✨ Features

### Weather Information
- **Current Conditions** - Temperature, "feels like", and weather icon
- **Sunrise & Sunset** - Today's sun times with localized labels
- **7-Day Forecast** - Daily high/low temperatures with weather icons
- **Hourly Forecast** - Next 7 hours with precipitation amounts (mm/inches)
- **Smart Precipitation Display** - Shows actual rainfall when expected, probability otherwise

### London Transit (TfL)
- **Bus Arrivals** - Real-time arrivals for any London bus stop
- **Underground** - Live tube arrivals for any station
- **Easy Setup** - Enter stop IDs directly in settings

### Customization
- **Multi-Language** - English, Spanish, German, French, Turkish, Swedish, Italian
- **Temperature Units** - Celsius (°C) or Fahrenheit (°F)
- **Clock Format** - 12-hour or 24-hour display
- **Night Mode** - Automatic screen dimming (10pm - 6am)
- **Brightness Control** - Adjustable backlight intensity

---

## 🛠 Hardware Requirements

| Component | Specification |
|-----------|---------------|
| Board | ESP32-2432S028R (CYD) |
| Display | 2.8" ILI9341 320x240 TFT |
| Touch | XPT2046 resistive touchscreen |
| Power | USB-C or 5V supply |

---

## 🚀 Quick Start

### Option 1: Using uv (Recommended)

This project uses [uv](https://docs.astral.sh/uv/) to manage PlatformIO in an isolated Python virtual environment. This ensures consistent builds and avoids conflicts with system Python packages.

```bash
# Clone the repository
git clone https://github.com/yourusername/Aura.git
cd Aura

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies (creates .venv and installs PlatformIO)
uv sync

# Activate the virtual environment
source .venv/bin/activate

# Build the project
pio run

# Upload to device
pio run --target upload

# Monitor serial output (optional)
pio device monitor
```

#### Using the Makefile

For convenience, a Makefile wraps common commands:

```bash
make config         # Create/edit config.h from template
make build          # Build the project
make upload         # Upload firmware to device
make monitor        # Open serial monitor
make flash          # Build and upload
make run            # Build, upload, and monitor
make sync           # Sync Python/uv dependencies
make clean          # Clean build files
make help           # Show all available commands
```

### Option 2: PlatformIO (Global Install)

If you prefer a global PlatformIO installation:

```bash
# Install PlatformIO globally
pip install platformio

# Clone and build
git clone https://github.com/yourusername/Aura.git
cd Aura
pio run
pio run --target upload
```

### Option 3: Arduino IDE

1. **Configure Arduino IDE**
   - Board: `ESP32 Dev Module`
   - Partition Scheme: `Minimal SPIFFS (1.9MB APP with OTA/190KB SPIFFS)`

2. **Install Required Libraries**
   | Library | Version |
   |---------|---------|
   | ArduinoJson | 7.4.1+ |
   | TFT_eSPI | 2.5.43 |
   | WiFiManager | 2.0.17 |
   | XPT2046_Touchscreen | 1.4 |
   | lvgl | 9.2.2+ |

3. **Copy Configuration Files**
   - Copy `lvgl/lv_conf.h` to your LVGL library folder
   - Copy `TFT_eSPI/User_Setup.h` to your TFT_eSPI library folder

4. **Build and Upload**

---

## 📁 Project Structure

```
Aura/
├── platformio.ini        # PlatformIO configuration
├── Makefile              # Build shortcuts
├── pyproject.toml        # Python/uv dependencies
├── src/                  # Source files
│   ├── main.cpp          # Main application logic
│   ├── icon_*.c          # Weather icon assets (24x24)
│   ├── image_*.c         # Weather images (64x64)
│   └── lv_font_*.c       # Custom Latin fonts
├── include/              # Header files
│   ├── lv_conf.h         # LVGL configuration
│   ├── translations.h    # Multi-language strings
│   └── config.h.example  # Configuration template
├── lib/                  # Project-specific libraries
├── aura/                 # Legacy Arduino IDE files
├── lvgl/                 # LVGL config (for Arduino IDE)
└── TFT_eSPI/             # TFT_eSPI config (for Arduino IDE)
```

---

## ⚙️ Configuration

### Compile-Time Configuration (Optional)

You can pre-configure WiFi, location, and transit settings at compile time. This is useful for:
- Faster initial setup (skip the captive portal)
- Flashing multiple devices with the same configuration
- Headless deployment

**Setup:**

```bash
# Create and edit config.h (interactive)
make config

# Or manually:
cp include/config.h.example include/config.h
nano include/config.h
```

**Available options in `config.h`:**

```c
// WiFi credentials (skip captive portal setup)
#define WIFI_SSID "YourNetworkName"
#define WIFI_PASSWORD "YourPassword"

// Location for weather data
#define CONFIG_LATITUDE "51.5074"
#define CONFIG_LONGITUDE "-0.1278"
#define CONFIG_LOCATION "London, England"

// TfL transit (London only)
#define CONFIG_BUS_STOP_ID "490008660N"
#define CONFIG_TUBE_STATION_ID "940GZZLUOXC"

// Display preferences
#define CONFIG_USE_FAHRENHEIT false
#define CONFIG_USE_24_HOUR true
#define CONFIG_USE_NIGHT_MODE true
#define CONFIG_BRIGHTNESS 200
#define CONFIG_LANGUAGE LANG_EN
```

> 🔒 **Security**: `config.h` is gitignored to keep your credentials private.

### First-Time Setup (WiFi)

1. Power on the device
2. Connect to the `Aura` WiFi network from your phone/laptop
3. A captive portal will open (or visit `http://192.168.4.1`)
4. Select your WiFi network and enter the password
5. The device will restart and connect

### Setting Your Location

1. Tap the screen to open **Settings**
2. Tap the **Location** button
3. Search for your city
4. Select from results and tap **Save**

### TfL Bus & Underground

1. Tap the screen to open **Settings**
2. Tap the blue **TfL** button
3. Enter your Bus Stop ID (e.g., `490008660N`)
4. Enter your Tube Station ID (e.g., `940GZZLUOXC`)
5. Tap **Save**

> 💡 Find stop IDs at [tfl.gov.uk](https://tfl.gov.uk) - search for your stop and look for the ID in the URL or stop details.

---

## 🌍 Supported Languages

| Language | Code | Contributor |
|----------|------|-------------|
| 🇬🇧 English | EN | Default |
| 🇪🇸 Spanish | ES | Community |
| 🇩🇪 German | DE | Community |
| 🇫🇷 French | FR | Community |
| 🇹🇷 Turkish | TR | Community |
| 🇸🇪 Swedish | SV | Community |
| 🇮🇹 Italian | IT | Community |

Want to add a language? Edit `include/translations.h` and submit a PR!

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

> ⚠️ **Note**: Weather icons are NOT included in the GPL license. See credits below for icon licensing.

---

## 🙏 Thanks & Credits

### Icons & Assets
- Weather icons from [Google Weather Icons](https://github.com/mrdarrengriffin/google-weather-icons/tree/main/v2) by [@mrdarrengriffin](https://github.com/mrdarrengriffin)

### Tutorials & References
- [witnessmenow](https://github.com/witnessmenow/) - [CYD GitHub repo](https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display) & [ESP32 Web Flashing Tutorial](https://github.com/witnessmenow/ESP-Web-Tools-Tutorial)
- [Random Nerd Tutorials](https://randomnerdtutorials.com/) - [LVGL Setup Guide](https://randomnerdtutorials.com/esp32-cyd-lvgl-line-chart/)

### Libraries
- [LVGL](https://lvgl.io/) - Embedded graphics library
- [ArduinoJson](https://arduinojson.org/) - JSON parsing
- [TFT_eSPI](https://github.com/Bodmer/TFT_eSPI) - Display driver
- [WiFiManager](https://github.com/tzapu/WiFiManager) - WiFi provisioning
- [XPT2046_Touchscreen](https://github.com/PaulStoffregen/XPT2046_Touchscreen) - Touch driver

### Data Providers
- [Open-Meteo](https://open-meteo.com/) - Weather API (free, no API key required)
- [Transport for London](https://api.tfl.gov.uk/) - Transit data API

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs** - Open an issue with steps to reproduce
2. **Add Translations** - Edit `translations.h` and submit a PR
3. **Improve Features** - Fork, develop, and submit a PR
4. **Share** - Star the repo and share with friends!

---

<p align="center">
  Made with ❤️ for the maker community
</p>
