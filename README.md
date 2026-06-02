# WinNetCommands 🖧
**Windows Network Diagnostic Tool for IT Technicians**

> 96 network commands. One searchable interface. No installation required.

Built by an IT support technician, for IT support technicians — because switching between browser tabs to look up `netsh`, `nslookup`, and `ipconfig` syntax while a user is waiting behind you is not a workflow.

---

## Download

### [⬇ Download WinNetCommands.exe](https://github.com/Mbensdesign/WinNetCommands/releases/tag/Networking)

Portable — runs on any Windows 10/11 machine with **no installation, no dependencies, no Python required**.

| Version | Platform | Status |
|---------|----------|--------|
| v1.0 | Windows 10 / 11 | ✅ Stable |

---

## What it does

WinNetCommands puts 96 Windows network diagnostic commands into a single dark-themed desktop interface with three ways to run any command:

| Action | How |
|--------|-----|
| **Copy** | Click Copy — command goes to clipboard, paste anywhere |
| **Run** | Click Run — executes directly inside the app, output appears in the built-in panel |
| **PS** | Click PS — opens the command in a new PowerShell window |

Additional features:
- **Search bar** — find any command instantly across all 96
- **Category tabs** — filter by ARP, DNS, Firewall, Ping, WiFi, and more
- **Inline parameter input** — enter host, IP, domain, or username directly in the interface
- **STOP button** — cancel a running command mid-execution
- **Resizable columns** — drag separators to fit your screen

---

## Command categories (96 commands total)

| Category | What's inside |
|----------|--------------|
| **ARP** | Address resolution, ARP cache display and manipulation |
| **DNS** | nslookup, ipconfig /flushdns, /displaydns, /registerdns |
| **Firewall** | netsh advfirewall rules, state, profiles |
| **IP** | ipconfig, IP address info, release/renew |
| **Info** | System and network information |
| **Net** | net use, net view, net share, net session, net user |
| **NetBIOS** | nbtstat commands |
| **Netsh** | Interface, WLAN, TCP global settings |
| **Ping** | ping, ping -t, ping -4/-6, pathping |
| **PowerShell** | PS networking cmdlets |
| **Proxy** | Proxy detection and configuration |
| **Remote** | RDP, remote session management |
| **Route** | route print, add, delete |
| **Stats** | netstat connections, ports, listeners |
| **Trace** | tracert, tracert -d |
| **Web** | curl, wget equivalents |
| **WiFi** | netsh wlan commands, profiles, show signal |

---

## Screenshots

### Main interface — browse and search 96 commands
<img width="3839" height="2052" alt="Screenshot 2026-06-02 042249" src="https://github.com/user-attachments/assets/ae345abe-0b86-47ab-b183-4a8e1b182727" />


### In-app execution — live output without leaving the tool
<img width="3839" height="2052" alt="Screenshot 2026-06-02 042609" src="https://github.com/user-attachments/assets/1530af48-0e6b-4a1c-8a9d-92c5c0f5d754" />

---

## How to use

```
1. Download WinNetCommands.exe from the Releases page
2. Double-click to launch — no setup, no install
3. Search or browse by category tab
4. Enter any required parameters (host, IP, domain) in the input column
5. Click Copy, Run, or PS
```

**Tip for IT technicians:** Pin it to your taskbar. It replaces the "google the command syntax" reflex during live troubleshooting.

---

## Who this is for

- IT helpdesk technicians (N1/N2)
- Network administrators
- System administrators
- Anyone who troubleshoots Windows networks daily and wants commands at their fingertips

---

## Built with

| Tool | Role |
|------|------|
| **Python 3** | Core application logic |
| **Tkinter** | Desktop GUI framework |
| **PyInstaller** | Compiled to standalone `.exe` |
| **Batch (build.bat)** | Automated build script |

---

## Roadmap — v2 ideas

- [ ] Custom command editor — add your own commands to the list
- [ ] Command history panel
- [ ] Export output to `.txt` file
- [ ] Dark / light theme toggle
- [ ] Linux equivalent (bash commands)
- [ ] French / Arabic language support

---

## Author

**Mohamed Ben Slimane**  
IT Support Technician | Networks & Infrastructure | Marrakesh, Morocco

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mohamed_Ben_Slimane-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mohbens)
[![GitHub](https://img.shields.io/badge/GitHub-Mbensdesign-181717?style=flat&logo=github&logoColor=white)](https://github.com/Mbensdesign)

---

## License

[GPL-3.0](LICENSE) — free to use, share, and modify with attribution.

---

*If this tool saved you time on a ticket, leave a ⭐ — it helps other technicians find it.*
