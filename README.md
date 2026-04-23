# Rivals - Professional OSINT Intelligence Tool

[![Go Version](https://img.shields.io/badge/Go-1.21+-00ADD8?logo=go)](https://golang.org)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🚀 Features

- 🔍 Multi-platform username enumeration (20+ platforms)
- 📸 Image metadata extraction (EXIF, GPS)
- 🌐 Proxy support (HTTP/SOCKS5)
- ⚡ Concurrent scanning (configurable threads)
- 📊 Multiple output formats (JSON/CSV/TXT)
- 🐧 Cross-platform (Windows, Linux, macOS)

## 📦 Installation

```bash
git clone https://github.com/KercX/rivals.git
cd rivals
chmod +x shell/*.sh
./shell/install.sh
```

🎯 Usage

```bash
# Basic scan
./shell/run.sh -u johndoe

# Advanced scan with proxy and custom output
./shell/run.sh -u johndoe -p proxies.txt -o results.json -t 30

# Using Make
make run ARGS="-u johndoe"
```

📁 Output Example

```json
{
  "username": "johndoe",
  "timestamp": "2024-01-15T10:30:00Z",
  "platforms": [
    {
      "name": "GitHub",
      "url": "https://github.com/johndoe",
      "exists": true,
      "status_code": 200
    }
  ]
}
```

⚖️ Legal Notice

Use for legitimate security research and authorized testing only.
