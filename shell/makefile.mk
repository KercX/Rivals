.PHONY: build run clean test install

BINARY_NAME=rivals
BUILD_DIR=bin

build:
	@echo "Building Rivals..."
	@mkdir -p $(BUILD_DIR)
	@go build -o $(BUILD_DIR)/$(BINARY_NAME) cmd/rivals/*.go

run: build
	@./$(BUILD_DIR)/$(BINARY_NAME) $(ARGS)

clean:
	@echo "Cleaning..."
	@rm -rf $(BUILD_DIR)
	@rm -rf venv
	@rm -f results.json image_analysis.json

test:
	@echo "Running tests..."
	@go test -v ./...

install:
	@./shell/install.sh

help:
	@echo "Available commands:"
	@echo "  make build    - Build the binary"
	@echo "  make run      - Run with ARGS='-u username'"
	@echo "  make clean    - Remove build artifacts"
	@echo "  make test     - Run tests"
	@echo "  make install  - Install dependencies"
