<div align="center">

# 🕵️ Rivals

### Advanced OSINT Intelligence Platform

[![Go Version](https://img.shields.io/badge/Go-1.21+-00ADD8?style=for-the-badge&logo=go&logoColor=white)](https://golang.org)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Shell](https://img.shields.io/badge/Shell-Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)](https://www.gnu.org/software/bash/)
[![Batch](https://img.shields.io/badge/Batch-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)

[![Maintainer](https://img.shields.io/badge/Maintainer-KercX-ff69b4?style=for-the-badge)](https://github.com/KercX)
[![GitHub Release](https://img.shields.io/github/v/release/KercX/Rivals?style=for-the-badge&logo=github&color=blue)](https://github.com/KercX/Rivals/releases)
[![Stars](https://img.shields.io/github/stars/KercX/Rivals?style=for-the-badge&logo=github&color=yellow)](https://github.com/KercX/Rivals/stargazers)
[![Forks](https://img.shields.io/github/forks/KercX/Rivals?style=for-the-badge&logo=github&color=orange)](https://github.com/KercX/Rivals/network)
[![Issues](https://img.shields.io/github/issues/KercX/Rivals?style=for-the-badge&logo=github&color=red)](https://github.com/KercX/Rivals/issues)

[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/KercX/Rivals/actions)
[![Code Style](https://img.shields.io/badge/Code%20Style-Go%20Standard-00ADD8?style=for-the-badge&logo=go&logoColor=white)](https://golang.org/doc/effective_go)
[![Security](https://img.shields.io/badge/Security-Audited-brightgreen?style=for-the-badge&logo=security&logoColor=white)](https://github.com/KercX/Rivals/security)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/kercx/rivals)

[![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)](https://github.com/KercX)
[![Coffee](https://img.shields.io/badge/Built%20with-Coffee-6F4E37?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white)](https://buymeacoffee.com/kercx)

</div>

---

## 📋 Table of Contents
- [✨ Features](#-features)
- [🖥️ Supported Platforms](#️-supported-platforms)
- [📦 Installation](#-installation)
- [🚀 Quick Start](#-quick-start)
- [📖 Usage Guide](#-usage-guide)
- [🔧 Configuration](#-configuration)
- [📁 Output Examples](#-output-examples)
- [🛠️ Development](#️-development)
- [🤝 Contributing](#-contributing)
- [📞 Contact](#-contact)
- [⚠️ Legal Notice](#️-legal-notice)
- [📄 License](#-license)

---

## ✨ Features

| Feature | Description | Status |
|---------|-------------|--------|
| 🔍 **Multi-Platform Scanning** | 20+ social media & professional networks | ✅ |
| ⚡ **Concurrent Requests** | Configurable thread pool for speed | ✅ |
| 🌐 **Proxy Support** | HTTP/HTTPS/SOCKS5 proxy rotation | ✅ |
| 📸 **Image Forensics** | EXIF/GPS metadata extraction | ✅ |
| 📊 **Multiple Output Formats** | JSON, CSV, TXT export | ✅ |
| 🐧 **Cross-Platform** | Windows, Linux, macOS support | ✅ |
| 🔄 **Rate Limiting** | Smart delays to avoid blocking | ✅ |
| 🛡️ **User-Agent Rotation** | Random realistic User-Agents | ✅ |
| 🔐 **Tor Support** | Anonymous scanning via Tor | 🚧 |
| 📧 **Email OSINT** | Email breach checking | 🚧 |

---

## 🖥️ Supported Platforms

<details>
<summary><b>Click to see 20+ platforms</b></summary>

| Platform | Check Type | API Support |
|----------|------------|-------------|
| GitHub | Profile existence | ✅ |
| Twitter/X | User profile | ✅ |
| Instagram | Account page | ⚠️ |
| Reddit | User profile | ✅ |
| LinkedIn | Professional profile | ⚠️ |
| YouTube | Channel page | ✅ |
| Facebook | User profile | ⚠️ |
| TikTok | @username page | ✅ |
| Telegram | Public channel | ✅ |
| Pinterest | Profile | ✅ |
| Snapchat | Username check | ❌ |
| Medium | @username | ✅ |
| Dev.to | Blog profile | ✅ |
| HackerNews | User ID | ✅ |
| Keybase | Identity proof | ✅ |
| Spotify | Artist/User | 🚧 |
| Twitch | Streamer page | 🚧 |
| Discord | User lookup | 🚧 |

</details>

---

## 📦 Installation

### 🔧 Prerequisites

```bash
# Required
- Go 1.21+
- Python 3.9+
- Git
- Make (optional)

# For image analysis
- libjpeg-dev (Linux)
- zlib1g-dev (Linux)
```

🐧 Linux / macOS

```bash
# Clone repository
git clone https://github.com/KercX/Rivals.git
cd Rivals

# Make scripts executable
chmod +x shell/*.sh

# Run automatic installer
./shell/install.sh

# Or use make
make install
```

🪟 Windows

```powershell
# Clone repository
git clone https://github.com/KercX/Rivals.git
cd Rivals

# Run installer
.\shell\install.bat

# Or using winget
winget install GoLang.Go
winget install Python.Python.3.9
```

🐳 Docker

```bash
# Build image
docker build -t rivals:latest .

# Run container
docker run -it --rm rivals:latest -u username
```

---

🚀 Quick Start

Basic Usage

```bash
# Simple username scan
./shell/run.sh -u johndoe

# Scan with custom output
./shell/run.sh -u johndoe -o results.json

# Verbose mode
./shell/run.sh -u johndoe --verbose
```

Advanced Usage

```bash
# With proxy list
./shell/run.sh -u johndoe -p proxies.txt

# High performance scan
./shell/run.sh -u johndoe -t 50 -T 3

# Full OSINT investigation
./shell/run.sh -u johndoe -o full_report.json --image-analysis
```

---

📖 Usage Guide

Command Line Options

```bash
Usage: rivals [OPTIONS] USERNAME

Options:
  -u, --username USER    Target username
  -p, --proxy FILE       Proxy list file (one per line)
  -o, --output FILE      Output file (default: results.json)
  -t, --threads NUM      Concurrent threads (default: 20)
  -T, --timeout SEC      HTTP timeout (default: 5)
  -v, --verbose          Verbose output
  -h, --help             Show help message
  
Examples:
  rivals -u johndoe
  rivals -u johndoe -o report.json -t 30
  rivals -u johndoe -p proxies.txt --verbose
```

Output Formats

```bash
# JSON (default) - machine readable
./shell/run.sh -u johndoe -o results.json

# CSV - spreadsheet compatible
./shell/run.sh -u johndoe -o results.csv

# TXT - human readable
./shell/run.sh -u johndoe -o results.txt
```

---

🔧 Configuration

Proxy File Format

```text
# proxies.txt - one proxy per line
http://user:pass@192.168.1.1:8080
https://192.168.1.2:3128
socks5://192.168.1.3:1080
```

Config File (config.yaml)

```yaml
scan:
  threads: 20
  timeout: 5
  retries: 3
  delay: 0.5

output:
  format: json
  directory: ./results
  verbose: false

proxy:
  enabled: false
  rotation: round-robin
  file: proxies.txt

platforms:
  - github
  - twitter
  - instagram
  - reddit
```

---

📁 Output Examples

JSON Output

```json
{
  "username": "johndoe",
  "timestamp": "2024-01-15T10:30:00Z",
  "scan_duration_sec": 2.34,
  "summary": {
    "total": 15,
    "found": 8,
    "not_found": 5,
    "errors": 2
  },
  "platforms": [
    {
      "name": "GitHub",
      "url": "https://github.com/johndoe",
      "exists": true,
      "status_code": 200,
      "response_time_ms": 234
    }
  ]
}
```

Console Output

```bash
🚀 Rivals OSINT Scanner v1.0
================================
Target: johndoe
Threads: 20 | Timeout: 5s

✓ GitHub: https://github.com/johndoe
✓ Twitter: https://twitter.com/johndoe
✗ Instagram: Not found
✓ Reddit: https://reddit.com/user/johndoe

📊 Scan Summary
==============
Total checked: 15
Found: 8
Not found: 5
Errors: 2

✅ Scan completed! Results saved to: results.json
```

---

🛠️ Development

Project Structure

```
Rivals/
├── cmd/           # Main entry points
├── internal/      # Private packages
├── pkg/           # Public libraries
├── scripts/       # Python helpers
├── shell/         # Shell scripts
├── config/        # Configuration files
├── Makefile       # Build automation
└── README.md      # Documentation
```

Building from Source

```bash
# Clone and build
git clone https://github.com/KercX/Rivals.git
cd Rivals
make build

# Run tests
make test

# Clean artifacts
make clean
```

Contributing Code

```bash
# Fork the repository
# Create feature branch
git checkout -b feature/amazing-feature

# Commit changes
git commit -m 'Add amazing feature'

# Push to branch
git push origin feature/amazing-feature

# Open Pull Request
```

---

🤝 Contributing

Contributions are welcome! Please read our Contributing Guidelines.

Ways to Contribute

· 🐛 Report bugs
· 💡 Suggest features
· 📝 Improve documentation
· 🔧 Submit pull requests

---

📞 Contact

Maintainer: KercX

https://img.shields.io/badge/GitHub-KercX-181717?style=flat-square&logo=github
https://img.shields.io/badge/Twitter-@KercX-1DA1F2?style=flat-square&logo=twitter
https://img.shields.io/badge/Telegram-@KercX-26A5E4?style=flat-square&logo=telegram
https://img.shields.io/badge/Email-kercx@proton.me-D14836?style=flat-square&logo=protonmail

---

⚠️ Legal Notice

```
THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY.

By using Rivals, you agree to:
1. Comply with all applicable laws and regulations
2. Not use this tool for malicious purposes
3. Respect privacy and data protection laws
4. Obtain proper authorization before scanning
5. Use only on accounts you own or have permission to test

The author (KercX) assumes no liability for misuse of this software.
```

---

📄 License

```
MIT License

Copyright (c) 2024 KercX

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...

Full license text available in [LICENSE](LICENSE) file.
```

---

<div align="center">⭐ Show Your Support

If you found Rivals helpful, please give it a star on GitHub!

https://img.shields.io/badge/Star%20on-GitHub-181717?style=for-the-badge&logo=github&logoColor=white

Made with ❤️ by KercX

https://img.shields.io/badge/Buy%20Me%20A-Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black

</div>

