# Makefile for Aura - ESP32 Weather Widget
# Wraps PlatformIO commands for convenience

.PHONY: all build upload monitor clean fullclean compile_commands help

# Default target
all: build

# Build the project
build:
	pio run

# Upload firmware to device
upload:
	pio run --target upload

# Open serial monitor
monitor:
	pio device monitor

# Build and upload
flash: build upload

# Build, upload, and monitor
run: upload monitor

# Clean build files
clean:
	pio run --target clean

# Full clean (remove .pio directory)
fullclean:
	rm -rf .pio

# Generate compile_commands.json for IDE support
compile_commands:
	pio run --target compiledb

# Update library dependencies
update:
	pio pkg update

# List connected devices
devices:
	pio device list

# Check project configuration
check:
	pio check

# Show project info
info:
	pio project config

# Help
help:
	@echo "Aura - ESP32 Weather Widget"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build          Build the project (default)"
	@echo "  upload         Upload firmware to device"
	@echo "  monitor        Open serial monitor"
	@echo "  flash          Build and upload"
	@echo "  run            Build, upload, and monitor"
	@echo "  clean          Clean build files"
	@echo "  fullclean      Remove .pio directory entirely"
	@echo "  compile_commands  Generate compile_commands.json"
	@echo "  update         Update library dependencies"
	@echo "  devices        List connected devices"
	@echo "  check          Run static code analysis"
	@echo "  info           Show project configuration"
	@echo "  help           Show this help message"
