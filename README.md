# Aura

Aura is a simple weather widget that runs on ESP32-2432S028R ILI9341 devices with a 2.8" screen. These devices are sometimes called a "CYD" or Cheap Yellow Display.

This is just the source code for the project. This project includes a case design and assembly instructions. The complete instructions are available
here: https://makerworld.com/en/models/1382304-aura-smart-weather-forecast-display

## Features

- **Weather Display**: Current temperature, feels like, 7-day forecast, hourly forecast
- **TfL Integration**: Real-time London bus and Underground arrivals
- **Multi-language**: English, Spanish, German, French, Turkish, Swedish, Italian
- **Night Mode**: Automatic screen dimming at night
- **Customizable**: Temperature units (°C/°F), 12/24hr clock, brightness

### License

You can use the code here under the terms of the GPL 3.0 license.

The icons are not included in that license. See "Thanks" below for details on the icons.

---

## How to Compile

### Option 1: PlatformIO (Recommended)

PlatformIO handles all dependencies automatically.

1. Install [PlatformIO](https://platformio.org/install)
2. Clone this repository
3. Build and upload:

```bash
# Build
pio run

# Upload to device
pio run --target upload

# Monitor serial output
pio device monitor
```

### Option 2: Arduino IDE

1. Configure Arduino IDE 
    1. for "esp32" board with a device type of "ESP32 Dev Module" and
    1. set "Tools -> Partition Scheme" to "Huge App (3MB No OTA/1MB SPIFFS)"
2. Install the libraries below in Arduino IDE
3. Copy files from `aura/` folder to your Arduino project
    1. Note the included config files for lvgl and TFT_eSPI need to be dropped in their respective library folders
4. Install and run

#### Libraries required (Arduino IDE):

- ArduinoJson 7.4.1
- TFT_eSPI 2.5.43
- WifiManager 2.0.17
- XPT2046_Touchscreen 1.4
- lvgl 9.2.2

---

## Project Structure

```
Aura/
├── platformio.ini      # PlatformIO configuration
├── src/                # Source files
│   ├── main.cpp        # Main application
│   ├── icon_*.c        # Weather icon assets
│   ├── image_*.c       # Weather image assets
│   └── lv_font_*.c     # Custom Latin fonts
├── include/            # Header files
│   ├── lv_conf.h       # LVGL configuration
│   └── translations.h  # Multi-language strings
├── lib/                # Project-specific libraries
├── aura/               # Legacy Arduino IDE files
├── lvgl/               # Legacy LVGL config
└── TFT_eSPI/           # Legacy TFT_eSPI config
```

---

## Configuration

### TfL Bus & Underground

1. Tap the screen to open Settings
2. Tap the blue "TfL" button
3. Enter your Bus Stop ID (e.g., `490008660N`)
4. Enter your Tube Station ID (e.g., `940GZZLUOXC`)
5. Find stop IDs at [tfl.gov.uk](https://tfl.gov.uk)

### Weather Location

1. Tap the screen to open Settings
2. Tap "Location" button
3. Search for your city
4. Select from results and save

---

## Thanks & Credits

- Weather icons from https://github.com/mrdarrengriffin/google-weather-icons/tree/main/v2
- Thanks to [lvgl](https://lvgl.io/), a great library for UIs on ESP32 devices that made this much easier
- Thanks to [witnessmenow](https://github.com/witnessmenow/)'s [CYD Github repo](https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display) for dev board reference information
- Double thanks to [witnessmenow](https://github.com/witnessmenow/) for the [ESP32 web flashing tutorial](https://github.com/witnessmenow/ESP-Web-Tools-Tutorial)
- Thanks to [Random Nerd Tutorials](https://randomnerdtutorials.com/) for helpful ESP32 / CYD information, especially with [setting up LVGL](https://randomnerdtutorials.com/esp32-cyd-lvgl-line-chart/)
- Thanks to these sweet libraries that made this possible:
  - [ArduinoJson](https://arduinojson.org/)
  - [TFT_eSPI](https://github.com/Bodmer/TFT_eSPI)
  - [WifiManager](https://github.com/tzapu/WiFiManager)
  - [XPT2046_Touchscreen](https://github.com/PaulStoffregen/XPT2046_Touchscreen)
  - [lvgl](https://lvgl.io/)
