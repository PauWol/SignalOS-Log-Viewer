# SignalOS Log Viewer

SignalOS Log Viewer is a simple and efficient log file viewer designed for SignalPi. It allows users to open, read, and analyze log files with an easy-to-use graphical interface.

## Features
- Open and view log files in a user-friendly interface.
- Simple and clean UI for better readability.
- Select log files directly from the application.
- Lightweight and fast.

## Installation & Setup
You have two options to install SignalOS Log Viewer:

### Option 1: Download Precompiled Executable
1. Download the latest precompiled `.exe` from the [Releases](https://github.com/pauwol/SignalPi/releases).
2. Run the executable (`LogViewer.exe`). No installation required!

### Option 2: Compile From Source
To build SignalOS Log Viewer from source, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/pauwol/SignalPi.git
   ```
2. Navigate into the project directory:
   ```sh
   cd SignalPi/logviewer
   ```
3. Install PyInstaller if you haven’t already:
   ```sh
   pip install pyinstaller
   ```
4. Build the executable:
   ```sh
   pyinstaller --name "LogViewer" --onefile --windowed --icon=icon.ico --add-data "icon.ico;." --version-file version.txt logviewer.py
   ```
5. The compiled `.exe` will be in the `dist/` folder.

## Usage
- Run the application and select a log file to view its contents.
- Scroll and analyze logs with ease.

## License
This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. See the [LICENSE](https://github.com/pauwol/SignalOS-log-viewer/LICENSE) file for details.

