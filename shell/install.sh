#!/bin/bash

# Rivals - Automated Installation Script

set -e

echo "Installing Rivals OSINT Tool..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux"
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y golang python3 python3-pip python3-venv git
    elif command -v yum &> /dev/null; then
        sudo yum install -y golang python3 python3-pip git
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS"
    if ! command -v brew &> /dev/null; then
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install go python3 git
fi

# Setup Go modules
go mod init github.com/yourusername/rivals
go get github.com/fatih/color
go get github.com/spf13/cobra
go get gopkg.in/yaml.v3

# Create directories
mkdir -p bin results config

# Make scripts executable
chmod +x shell/*.sh

echo "Installation complete!"
echo "Run: ./shell/run.sh -u [username]"
