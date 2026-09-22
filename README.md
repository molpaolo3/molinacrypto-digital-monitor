# MolinaCrypto Digital Monitor v1.0

**Closed-source desktop release for Linux.**

MolinaCrypto Digital Monitor is the desktop intelligence client of the MolinaCrypto / Molina Security Lab ecosystem. Version 1.0 brings the information flows of the Molina Cyberdeck into a lightweight native Linux interface.

## Modules

- Command Deck
- Threat Telemetry
- Cyber Attack Map with animated source → target arcs
- Attack Wire
- Exploit & Zero-Day
- IOC Vault
- Cyber Intel
- OSINT Scope
- Intel Deck
- Web3 Mesh
- AI Watch
- Crypto Market
- Bitcoin Network
- Risk Scan
- Diagnostics

## Privacy gate

At startup the application shows a privacy and usage notice before any live module becomes available. If the notice is declined, the application closes. If accepted, the interface and live first-party feeds become available.

## Data model

Cyber intelligence is primarily read through first-party endpoints under `molinacrypto.eu`. The desktop client displays normalized public information and does not represent individual telemetry events as forensic proof of a real-world attack.

Crypto Market uses Kraken public market data. Bitcoin Network data is read through the MolinaCrypto first-party proxy used by the Cyberdeck.

## Distribution model

The v1.x source code is **not distributed** in this repository or in official release assets. Official v1.x downloads contain only the compiled Linux application package, release documentation and SHA-256 checksums.

The historical v0.8 open-source snapshot remains available on the `legacy-v0.8-open-source` branch under the license that applied to that release.

## Linux

The official v1.x package targets 64-bit Linux systems. The distributed archive contains the compiled application and supporting release files; Python source files are not included.

## Security

Verify the published SHA-256 checksum before running a downloaded package. Download only from official MolinaCrypto channels.

## Disclaimer

Information is provided for educational, informational and security-awareness purposes. It is not financial, investment, legal, tax or professional cybersecurity advice.

Official site: https://www.molinacrypto.eu/
