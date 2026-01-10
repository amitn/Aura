#!/usr/bin/env python3
"""
Download and resize weather images for LVGL.
Converts images from 100x100 to 64x64 to reduce flash usage for OTA support.
"""

import os
import sys
import struct
from pathlib import Path

try:
    from PIL import Image
    import requests
except ImportError:
    print("Installing required packages...")
    os.system(f"{sys.executable} -m pip install Pillow requests")
    from PIL import Image
    import requests

# Image mappings: local name -> GitHub raw URL
GITHUB_BASE = "https://raw.githubusercontent.com/mrdarrengriffin/google-weather-icons/main/v2"

IMAGE_MAPPINGS = {
    "image_blizzard": "blizzard.png",
    "image_blowing_snow": "blowing_snow.png",
    "image_clear_night": "clear_night.png",
    "image_cloudy": "cloudy.png",
    "image_drizzle": "drizzle.png",
    "image_flurries": "flurries.png",
    "image_haze_fog_dust_smoke": "haze_fog_dust_smoke.png",
    "image_heavy_rain": "heavy_rain.png",
    "image_heavy_snow": "heavy_snow.png",
    "image_isolated_scattered_tstorms_day": "isolated_scattered_tstorms_day.png",
    "image_isolated_scattered_tstorms_night": "isolated_scattered_tstorms_night.png",
    "image_mostly_clear_night": "mostly_clear_night.png",
    "image_mostly_cloudy_day": "mostly_cloudy_day.png",
    "image_mostly_cloudy_night": "mostly_cloudy_night.png",
    "image_mostly_sunny": "mostly_sunny.png",
    "image_partly_cloudy": "partly_cloudy.png",
    "image_partly_cloudy_night": "partly_cloudy_night.png",
    "image_scattered_showers_day": "scattered_showers_day.png",
    "image_scattered_showers_night": "scattered_showers_night.png",
    "image_showers_rain": "showers_rain.png",
    "image_sleet_hail": "sleet_hail.png",
    "image_snow_showers_snow": "snow_showers_snow.png",
    "image_strong_tstorms": "strong_tstorms.png",
    "image_sunny": "sunny.png",
    "image_tornado": "tornado.png",
    "image_wintry_mix_rain_snow": "wintry_mix_rain_snow.png",
}

TARGET_SIZE = 64  # New size in pixels


def download_image(url: str, output_path: Path) -> bool:
    """Download an image from URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        output_path.write_bytes(response.content)
        return True
    except Exception as e:
        print(f"  Error downloading {url}: {e}")
        return False


def rgb888_to_rgb565(r: int, g: int, b: int) -> int:
    """Convert RGB888 to RGB565."""
    return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)


def generate_lvgl_c_file(image_name: str, img: Image.Image, output_path: Path):
    """Generate LVGL C source file from PIL Image."""
    width, height = img.size
    
    # Convert to RGBA if not already
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    
    pixels = list(img.getdata())
    
    # Build pixel data: RGB565 (2 bytes) + Alpha (1 byte) per pixel
    pixel_data = []
    for r, g, b, a in pixels:
        rgb565 = rgb888_to_rgb565(r, g, b)
        # RGB565 in little-endian
        pixel_data.append(rgb565 & 0xFF)
        pixel_data.append((rgb565 >> 8) & 0xFF)
    
    # Alpha channel comes after all RGB565 data
    for r, g, b, a in pixels:
        pixel_data.append(a)
    
    # Generate C file content
    var_name = image_name
    c_content = f'''
#ifdef __has_include
    #if __has_include("lvgl.h")
        #ifndef LV_LVGL_H_INCLUDE_SIMPLE
            #define LV_LVGL_H_INCLUDE_SIMPLE
        #endif
    #endif
#endif

#if defined(LV_LVGL_H_INCLUDE_SIMPLE)
    #include "lvgl.h"
#else
    #include "lvgl/lvgl.h"
#endif


#ifndef LV_ATTRIBUTE_MEM_ALIGN
#define LV_ATTRIBUTE_MEM_ALIGN
#endif

#ifndef LV_ATTRIBUTE_{var_name.upper()}
#define LV_ATTRIBUTE_{var_name.upper()}
#endif

static const
LV_ATTRIBUTE_MEM_ALIGN LV_ATTRIBUTE_LARGE_CONST LV_ATTRIBUTE_{var_name.upper()}
uint8_t {var_name}_map[] = {{

'''
    
    # Write pixel data in rows
    bytes_per_row = width * 3  # RGB565 (2) + Alpha (1)
    stride = width * 2  # RGB565 stride
    
    # Write RGB565 data
    rgb565_data = pixel_data[:width * height * 2]
    for row in range(height):
        row_start = row * stride
        row_bytes = rgb565_data[row_start:row_start + stride]
        hex_values = ",".join(f"0x{b:02x}" for b in row_bytes)
        c_content += f"    {hex_values},\n"
    
    # Write alpha data
    alpha_data = pixel_data[width * height * 2:]
    for row in range(height):
        row_start = row * width
        row_bytes = alpha_data[row_start:row_start + width]
        hex_values = ",".join(f"0x{b:02x}" for b in row_bytes)
        c_content += f"    {hex_values},\n"
    
    c_content += f'''
}};

const lv_image_dsc_t {var_name} = {{
  .header.magic = LV_IMAGE_HEADER_MAGIC,
  .header.cf = LV_COLOR_FORMAT_RGB565A8,
  .header.flags = 0,
  .header.w = {width},
  .header.h = {height},
  .header.stride = {stride},
  .header.reserved_2 = 0,
  .data_size = sizeof({var_name}_map),
  .data = {var_name}_map,
  .reserved = NULL,
}};

'''
    
    output_path.write_text(c_content)


def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    src_dir = project_root / "src"
    cache_dir = script_dir / "image_cache"
    cache_dir.mkdir(exist_ok=True)
    
    print(f"Resizing weather images to {TARGET_SIZE}x{TARGET_SIZE}...")
    print(f"Output directory: {src_dir}")
    print()
    
    success_count = 0
    error_count = 0
    
    for image_name, github_filename in IMAGE_MAPPINGS.items():
        print(f"Processing {image_name}...")
        
        # Download if not cached
        cache_path = cache_dir / github_filename
        if not cache_path.exists():
            url = f"{GITHUB_BASE}/{github_filename}"
            print(f"  Downloading from {url}")
            if not download_image(url, cache_path):
                error_count += 1
                continue
        
        # Load and resize
        try:
            img = Image.open(cache_path)
            img = img.resize((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS)
            
            # Generate C file
            output_path = src_dir / f"{image_name}.c"
            generate_lvgl_c_file(image_name, img, output_path)
            
            print(f"  Generated {output_path.name}")
            success_count += 1
            
        except Exception as e:
            print(f"  Error processing: {e}")
            error_count += 1
    
    print()
    print(f"Done! {success_count} images converted, {error_count} errors")
    
    if success_count > 0:
        print()
        print("Now rebuild the project:")
        print("  pio run")


if __name__ == "__main__":
    main()
