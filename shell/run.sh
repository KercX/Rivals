#!/bin/bash

# Rivals - Professional OSINT Tool Launcher
# Supports Linux and macOS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
cat << "EOF"
   ____       _ _       _
  |  _ \ ___ (_) | ___ | |
  | |_) / _ \| | |/ _ \| |
  |  _ < (_) | | | (_) | |
  |_| \_\___/|_|_|\___/|_|
                           
EOF
echo -e "${NC}"

# Check dependencies
check_dependency() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}✗ $1 not found${NC}"
        return 1
    else
        echo -e "${GREEN}✓ $1 found${NC}"
        return 0
    fi
}

echo -e "${YELLOW}Checking dependencies...${NC}\n"

DEPS_OK=true
check_dependency "go" || DEPS_OK=false
check_dependency "python3" || DEPS_OK=false
check_dependency "pip3" || DEPS_OK=false

if [ "$DEPS_OK" = false ]; then
    echo -e "\n${RED}Missing dependencies. Run: ./shell/install.sh${NC}"
    exit 1
fi

# Install Python dependencies if needed
if [ ! -d "venv" ]; then
    echo -e "\n${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r scripts/requirements.txt
else
    source venv/bin/activate
fi

# Build Go binary
echo -e "\n${YELLOW}Building Rivals binary...${NC}"
go build -o bin/rivals cmd/rivals/*.go

# Parse arguments
USERNAME=$1
PROXY_FILE=""
OUTPUT_FILE="results.json"
THREADS=20
TIMEOUT=5

while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--username)
            USERNAME="$2"
            shift 2
            ;;
        -p|--proxy)
            PROXY_FILE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -t|--threads)
            THREADS="$2"
            shift 2
            ;;
        -T|--timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: ./shell/run.sh [OPTIONS]"
            echo "Options:"
            echo "  -u, --username USER    Target username"
            echo "  -p, --proxy FILE       Proxy list file"
            echo "  -o, --output FILE      Output file (default: results.json)"
            echo "  -t, --threads NUM      Concurrent threads (default: 20)"
            echo "  -T, --timeout SEC      HTTP timeout (default: 5)"
            exit 0
            ;;
        *)
            USERNAME="$1"
            shift
            ;;
    esac
done

if [ -z "$USERNAME" ]; then
    echo -e "${RED}Error: Username required${NC}"
    exit 1
fi

# Run scanner
echo -e "\n${GREEN}Starting Rivals scan for: $USERNAME${NC}\n"
./bin/rivals -u "$USERNAME" -p "$PROXY_FILE" -o "$OUTPUT_FILE" -t "$THREADS" -T "$TIMEOUT"

deactivate
echo -e "\n${GREEN}✅ Scan completed${NC}"
