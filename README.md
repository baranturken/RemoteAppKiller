# RemoteAppKiller ☁️⏹️  
*Cloud-triggered process termination via OneDrive monitoring*

## Features
- Monitors OneDrive for specified trigger files
- Terminates multiple target applications simultaneously
- Automatic cleanup of trigger files post-action
- Configurable sync delay for cloud operations

## Requirements
- Python 3.8+
- Windows 10/11 (OneDrive desktop client)
- Administrator privileges (recommended)

## Installation
```bash
git clone https://github.com/baranturken/RemoteAppKiller.git
cd RemoteAppKiller
pip install watchdog psutil