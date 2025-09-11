"""
Application Scanner Module for A.R.I.S.E. AI Assistant

This module scans the system for installed applications and saves their
executable paths to a JSON file for automation purposes.

Author: A.R.I.S.E. AI Team
Date: September 2025
"""

import os
import json
import platform
import winreg
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ApplicationScanner:
    """
    Scans the system for installed applications and manages their paths.
    """
    
    def __init__(self, output_file: str = "applications.json"):
        """
        Initialize the Application Scanner.
        
        Args:
            output_file (str): Path to save the applications JSON file
        """
        self.output_file = output_file
        self.applications = {}
        self.system = platform.system()
        
    def scan_windows_registry(self) -> Dict[str, str]:
        """
        Scan Windows registry for installed applications.
        
        Returns:
            Dict[str, str]: Dictionary of application names and their paths
        """
        apps = {}
        
        # Registry keys to scan for installed applications
        registry_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        ]
        
        for hkey, subkey_path in registry_keys:
            try:
                with winreg.OpenKey(hkey, subkey_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                    
                                    if install_location and os.path.exists(install_location):
                                        # Look for executable files in the installation directory
                                        exe_path = self._find_main_executable(install_location, display_name)
                                        if exe_path:
                                            apps[display_name] = exe_path
                                            
                                except FileNotFoundError:
                                    # Try to get executable path directly
                                    try:
                                        exe_path = winreg.QueryValueEx(subkey, "DisplayIcon")[0]
                                        if exe_path.endswith('.exe') and os.path.exists(exe_path):
                                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                            apps[display_name] = exe_path
                                    except FileNotFoundError:
                                        continue
                                        
                        except (OSError, FileNotFoundError):
                            continue
                            
            except FileNotFoundError:
                logger.warning(f"Registry key not found: {subkey_path}")
                continue
                
        return apps
    
    def scan_windows_store_apps(self) -> Dict[str, str]:
        """
        Scan for Windows Store (UWP) applications.
        
        Returns:
            Dict[str, str]: Dictionary of Windows Store apps and their paths
        """
        apps = {}
        
        if self.system != "Windows":
            return apps
            
        try:
            # Common Windows Store apps with their package names
            store_apps = {
                "Microsoft Store": "Microsoft.WindowsStore_8wekyb3d8bbwe",
                "Calculator": "Microsoft.WindowsCalculator_8wekyb3d8bbwe",
                "Mail": "microsoft.windowscommunicationsapps_8wekyb3d8bbwe",
                "Calendar": "microsoft.windowscommunicationsapps_8wekyb3d8bbwe",
                "Photos": "Microsoft.Windows.Photos_8wekyb3d8bbwe",
                "Camera": "Microsoft.WindowsCamera_8wekyb3d8bbwe",
                "Maps": "Microsoft.WindowsMaps_8wekyb3d8bbwe",
                "Weather": "Microsoft.BingWeather_8wekyb3d8bbwe",
                "News": "Microsoft.BingNews_8wekyb3d8bbwe",
                "Microsoft Edge (UWP)": "Microsoft.MicrosoftEdge_8wekyb3d8bbwe",
                "Notepad": "Microsoft.WindowsNotepad_8wekyb3d8bbwe",
                "Paint 3D": "Microsoft.MSPaint_8wekyb3d8bbwe",
                "Voice Recorder": "Microsoft.SoundRecorder_8wekyb3d8bbwe",
                "Movies & TV": "Microsoft.ZuneVideo_8wekyb3d8bbwe",
                "Groove Music": "Microsoft.ZuneMusic_8wekyb3d8bbwe",
                "Xbox": "Microsoft.XboxApp_8wekyb3d8bbwe",
                "OneNote": "Microsoft.Office.OneNote_8wekyb3d8bbwe",
                "Solitaire Collection": "Microsoft.MicrosoftSolitaireCollection_8wekyb3d8bbwe",
                "Terminal": "Microsoft.WindowsTerminal_8wekyb3d8bbwe",
                "PowerShell": "Microsoft.PowerShell_8wekyb3d8bbwe"
            }
            
            # Try to use PowerShell to get installed packages
            try:
                result = subprocess.run([
                    'powershell', '-Command', 
                    'Get-AppxPackage | Select-Object Name, InstallLocation | ConvertTo-Json'
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0 and result.stdout:
                    packages = json.loads(result.stdout)
                    if not isinstance(packages, list):
                        packages = [packages]
                    
                    for package in packages:
                        if package.get('InstallLocation'):
                            package_name = package.get('Name', '')
                            install_location = package['InstallLocation']
                            
                            # Map package names to friendly names
                            friendly_name = None
                            for app_name, package_id in store_apps.items():
                                if package_id in package_name:
                                    friendly_name = app_name
                                    break
                            
                            if not friendly_name:
                                # Try to extract a friendly name from the package name
                                if 'Microsoft.' in package_name:
                                    friendly_name = package_name.replace('Microsoft.', '').split('_')[0]
                                elif '.' in package_name:
                                    friendly_name = package_name.split('.')[1].split('_')[0]
                                else:
                                    friendly_name = package_name.split('_')[0]
                            
                            # Look for executable in the install location
                            if os.path.exists(install_location):
                                exe_path = self._find_uwp_executable(install_location, friendly_name)
                                if exe_path:
                                    apps[friendly_name] = exe_path
                                    
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError, Exception):
                logger.warning("Could not scan Windows Store apps via PowerShell")
                
            # Fallback: Check common UWP app locations
            uwp_base_paths = [
                r"C:\Program Files\WindowsApps",
                os.path.expanduser(r"~\AppData\Local\Packages")
            ]
            
            for base_path in uwp_base_paths:
                if os.path.exists(base_path):
                    for app_name, package_name in store_apps.items():
                        # Look for directories matching the package name
                        try:
                            for item in os.listdir(base_path):
                                if package_name in item:
                                    app_path = os.path.join(base_path, item)
                                    if os.path.isdir(app_path):
                                        exe_path = self._find_uwp_executable(app_path, app_name)
                                        if exe_path:
                                            apps[app_name] = exe_path
                                            break
                        except (PermissionError, OSError):
                            continue
                            
        except Exception as e:
            logger.warning(f"Error scanning Windows Store apps: {e}")
            
        return apps
    
    def _find_uwp_executable(self, app_path: str, app_name: str) -> Optional[str]:
        """
        Find the executable for a UWP app.
        
        Args:
            app_path (str): Path to the UWP app directory
            app_name (str): Name of the application
            
        Returns:
            Optional[str]: Path to the executable, or None if not found
        """
        try:
            # Look for AppxManifest.xml to find the executable
            manifest_path = os.path.join(app_path, "AppxManifest.xml")
            if os.path.exists(manifest_path):
                try:
                    import xml.etree.ElementTree as ET
                    tree = ET.parse(manifest_path)
                    root = tree.getroot()
                    
                    # Find the Application element
                    ns = {'': 'http://schemas.microsoft.com/appx/manifest/foundation/windows10'}
                    apps = root.findall('.//Application', ns)
                    if not apps:
                        ns = {'': 'http://schemas.microsoft.com/appx/2010/manifest'}
                        apps = root.findall('.//Application', ns)
                    
                    for app in apps:
                        executable = app.get('Executable')
                        if executable and executable.endswith('.exe'):
                            exe_path = os.path.join(app_path, executable)
                            if os.path.exists(exe_path):
                                return exe_path
                                
                except Exception:
                    pass
                    
            # Fallback: look for common executable patterns
            common_patterns = [
                f"{app_name.lower()}.exe",
                f"{app_name.replace(' ', '')}.exe",
                "app.exe",
                "main.exe"
            ]
            
            for root, dirs, files in os.walk(app_path):
                for file in files:
                    if file.lower().endswith('.exe'):
                        if any(pattern in file.lower() for pattern in common_patterns):
                            return os.path.join(root, file)
                        # If no pattern match, return first .exe found in root
                        if root == app_path:
                            return os.path.join(root, file)
                            
        except Exception:
            pass
            
        return None
    
    def scan_office_applications(self) -> Dict[str, str]:
        """
        Dedicated scan for Microsoft Office applications.
        
        Returns:
            Dict[str, str]: Dictionary of Office applications and their paths
        """
        apps = {}
        
        if self.system != "Windows":
            return apps
            
        # Office application executables
        office_apps = {
            "Microsoft Word": "WINWORD.EXE",
            "Microsoft Excel": "EXCEL.EXE", 
            "Microsoft PowerPoint": "POWERPNT.EXE",
            "Microsoft Outlook": "OUTLOOK.EXE",
            "Microsoft OneNote": "ONENOTE.EXE",
            "Microsoft Access": "MSACCESS.EXE",
            "Microsoft Publisher": "MSPUB.EXE",
            "Microsoft Visio": "VISIO.EXE",
            "Microsoft Project": "WINPROJ.EXE"
        }
        
        # Common Office installation paths
        office_paths = [
            r"C:\Program Files\Microsoft Office\root\Office16",
            r"C:\Program Files (x86)\Microsoft Office\root\Office16", 
            r"C:\Program Files\Microsoft Office\Office16",
            r"C:\Program Files (x86)\Microsoft Office\Office16",
            r"C:\Program Files\Microsoft Office\Office15",
            r"C:\Program Files (x86)\Microsoft Office\Office15",
            r"C:\Program Files\Microsoft Office\Office14",
            r"C:\Program Files (x86)\Microsoft Office\Office14",
            # Office 365 Click-to-Run paths
            r"C:\Program Files\Microsoft Office\root\Office16",
            r"C:\Program Files (x86)\Microsoft Office\root\Office16"
        ]
        
        # Also check registry for Office installation paths
        try:
            office_reg_keys = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Office\16.0\Common\InstallRoot"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Office\15.0\Common\InstallRoot"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Office\14.0\Common\InstallRoot"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Office\16.0\Common\InstallRoot"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Office\15.0\Common\InstallRoot")
            ]
            
            for hkey, subkey_path in office_reg_keys:
                try:
                    with winreg.OpenKey(hkey, subkey_path) as key:
                        install_path = winreg.QueryValueEx(key, "Path")[0]
                        if install_path and install_path not in office_paths:
                            office_paths.append(install_path)
                except FileNotFoundError:
                    continue
                    
        except Exception:
            pass
        
        # Check each Office path for applications
        for office_path in office_paths:
            if os.path.exists(office_path):
                for app_name, exe_name in office_apps.items():
                    exe_path = os.path.join(office_path, exe_name)
                    if os.path.exists(exe_path):
                        apps[app_name] = exe_path
                        
        return apps
    
    def scan_common_directories(self) -> Dict[str, str]:
        """
        Scan common installation directories for applications.
        
        Returns:
            Dict[str, str]: Dictionary of application names and their paths
        """
        apps = {}
        
        if self.system == "Windows":
            common_dirs = [
                r"C:\Program Files",
                r"C:\Program Files (x86)",
                os.path.expanduser("~\\AppData\\Local"),
                os.path.expanduser("~\\AppData\\Roaming"),
                os.path.expanduser("~\\AppData\\Local\\Programs"),
                r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
                os.path.expanduser("~\\Desktop"),
                r"C:\Users\Public\Desktop"
            ]
        elif self.system == "Darwin":  # macOS
            common_dirs = [
                "/Applications",
                os.path.expanduser("~/Applications"),
                "/System/Applications"
            ]
        else:  # Linux
            common_dirs = [
                "/usr/bin",
                "/usr/local/bin",
                "/opt",
                os.path.expanduser("~/.local/bin")
            ]
        
        for directory in common_dirs:
            if os.path.exists(directory):
                apps.update(self._scan_directory(directory))
                
        return apps
    
    def _scan_directory(self, directory: str, max_depth: int = 2) -> Dict[str, str]:
        """
        Recursively scan a directory for executable files.
        
        Args:
            directory (str): Directory to scan
            max_depth (int): Maximum recursion depth
            
        Returns:
            Dict[str, str]: Dictionary of application names and their paths
        """
        apps = {}
        
        try:
            if max_depth <= 0:
                return apps
                
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                
                if os.path.isfile(item_path):
                    if self._is_executable(item_path):
                        app_name = os.path.splitext(item)[0]
                        apps[app_name] = item_path
                        
                elif os.path.isdir(item_path) and not item.startswith('.'):
                    # For macOS .app bundles
                    if self.system == "Darwin" and item.endswith('.app'):
                        # Find the executable inside the .app bundle
                        exe_path = self._find_macos_executable(item_path)
                        if exe_path:
                            app_name = item.replace('.app', '')
                            apps[app_name] = exe_path
                    else:
                        # Recursively scan subdirectories
                        sub_apps = self._scan_directory(item_path, max_depth - 1)
                        apps.update(sub_apps)
                        
        except (PermissionError, OSError) as e:
            logger.warning(f"Cannot access directory {directory}: {e}")
            
        return apps
    
    def _find_main_executable(self, install_dir: str, app_name: str) -> Optional[str]:
        """
        Find the main executable file in an installation directory.
        
        Args:
            install_dir (str): Installation directory
            app_name (str): Application name
            
        Returns:
            Optional[str]: Path to the main executable, or None if not found
        """
        if not os.path.exists(install_dir):
            return None
            
        # Common executable names to look for
        common_exes = [
            f"{app_name.lower()}.exe",
            f"{app_name.split()[0].lower()}.exe",
            "main.exe",
            "launcher.exe",
            f"{os.path.basename(install_dir).lower()}.exe"
        ]
        
        # Search for executable files
        for root, dirs, files in os.walk(install_dir):
            for file in files:
                if file.lower().endswith('.exe'):
                    file_path = os.path.join(root, file)
                    
                    # Check if it's one of the common executable names
                    if file.lower() in common_exes:
                        return file_path
                    
                    # If no common name found, return the first .exe file in the root directory
                    if root == install_dir:
                        return file_path
                        
        return None
    
    def _find_macos_executable(self, app_bundle: str) -> Optional[str]:
        """
        Find the executable inside a macOS .app bundle.
        
        Args:
            app_bundle (str): Path to the .app bundle
            
        Returns:
            Optional[str]: Path to the executable, or None if not found
        """
        contents_dir = os.path.join(app_bundle, "Contents")
        macos_dir = os.path.join(contents_dir, "MacOS")
        
        if os.path.exists(macos_dir):
            for file in os.listdir(macos_dir):
                file_path = os.path.join(macos_dir, file)
                if os.access(file_path, os.X_OK):
                    return file_path
                    
        return None
    
    def _is_executable(self, file_path: str) -> bool:
        """
        Check if a file is executable.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            bool: True if the file is executable, False otherwise
        """
        if self.system == "Windows":
            return file_path.lower().endswith(('.exe', '.msi', '.bat', '.cmd'))
        else:
            return os.access(file_path, os.X_OK)
    
    def scan_gaming_platforms(self) -> Dict[str, str]:
        """
        Scan for gaming platforms and installed games.
        
        Returns:
            Dict[str, str]: Dictionary of games and their paths
        """
        games = {}
        
        if self.system != "Windows":
            return games
            
        # Steam games
        steam_paths = [
            r"C:\Program Files\Steam",
            r"C:\Program Files (x86)\Steam"
        ]
        
        for steam_path in steam_paths:
            if os.path.exists(steam_path):
                # Look for Steam games
                steamapps_path = os.path.join(steam_path, "steamapps", "common")
                if os.path.exists(steamapps_path):
                    try:
                        for game_folder in os.listdir(steamapps_path):
                            game_path = os.path.join(steamapps_path, game_folder)
                            if os.path.isdir(game_path):
                                # Look for the main executable
                                exe_path = self._find_game_executable(game_path, game_folder)
                                if exe_path:
                                    games[f"{game_folder} (Steam)"] = exe_path
                    except (PermissionError, OSError):
                        continue
        
        # Epic Games
        epic_path = r"C:\Program Files\Epic Games"
        if os.path.exists(epic_path):
            try:
                for item in os.listdir(epic_path):
                    if item != "Launcher":  # Skip the launcher folder
                        game_path = os.path.join(epic_path, item)
                        if os.path.isdir(game_path):
                            exe_path = self._find_game_executable(game_path, item)
                            if exe_path:
                                games[f"{item} (Epic)"] = exe_path
            except (PermissionError, OSError):
                pass
        
        # Riot Games
        riot_path = r"C:\Riot Games"
        if os.path.exists(riot_path):
            try:
                for item in os.listdir(riot_path):
                    game_path = os.path.join(riot_path, item)
                    if os.path.isdir(game_path):
                        exe_path = self._find_game_executable(game_path, item)
                        if exe_path:
                            games[f"{item} (Riot)"] = exe_path
            except (PermissionError, OSError):
                pass
        
        return games
    
    def _find_game_executable(self, game_path: str, game_name: str) -> Optional[str]:
        """
        Find the main executable for a game.
        
        Args:
            game_path (str): Path to the game directory
            game_name (str): Name of the game
            
        Returns:
            Optional[str]: Path to the game executable
        """
        try:
            # Common game executable patterns
            common_patterns = [
                f"{game_name.lower()}.exe",
                f"{game_name.replace(' ', '')}.exe",
                f"{game_name.replace(' ', '_')}.exe",
                "game.exe",
                "launcher.exe",
                "main.exe"
            ]
            
            # Look for executables in the game directory
            for root, dirs, files in os.walk(game_path):
                for file in files:
                    if file.lower().endswith('.exe'):
                        file_lower = file.lower()
                        
                        # Check against common patterns
                        for pattern in common_patterns:
                            if pattern in file_lower or file_lower == pattern:
                                return os.path.join(root, file)
                        
                        # Skip known non-game executables
                        skip_patterns = ['unins', 'setup', 'install', 'update', 'crash', 'report']
                        if any(skip in file_lower for skip in skip_patterns):
                            continue
                        
                        # If we find an executable in the root directory, prefer it
                        if root == game_path and file_lower.endswith('.exe'):
                            return os.path.join(root, file)
        
        except Exception:
            pass
            
        return None
    
    def scan_popular_applications(self) -> Dict[str, str]:
        """
        Scan for popular applications with known installation paths.
        
        Returns:
            Dict[str, str]: Dictionary of application names and their paths
        """
        apps = {}
        
        if self.system == "Windows":
            popular_apps = {
                # Web Browsers
                "Google Chrome": [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
                ],
                "Mozilla Firefox": [
                    r"C:\Program Files\Mozilla Firefox\firefox.exe",
                    r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
                ],
                "Microsoft Edge": [
                    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                    r"C:\Windows\SystemApps\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\MicrosoftEdge.exe"
                ],
                "Internet Explorer": [
                    r"C:\Program Files\Internet Explorer\iexplore.exe",
                    r"C:\Program Files (x86)\Internet Explorer\iexplore.exe"
                ],
                "Brave": [
                    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                    r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
                    os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe")
                ],
                "Opera": [
                    r"C:\Program Files\Opera\opera.exe", 
                    r"C:\Program Files (x86)\Opera\opera.exe",
                    os.path.expanduser(r"~\AppData\Local\Programs\Opera\opera.exe")
                ],
                
                # Communication Apps
                "WhatsApp": [
                    os.path.expanduser(r"~\AppData\Local\WhatsApp\WhatsApp.exe"),
                    os.path.expanduser(r"~\AppData\Roaming\WhatsApp\WhatsApp.exe")
                ],
                "Discord": [
                    os.path.expanduser(r"~\AppData\Local\Discord\app-*\Discord.exe"),
                    os.path.expanduser(r"~\AppData\Roaming\Discord\app-*\Discord.exe")
                ],
                "Skype": [
                    r"C:\Program Files (x86)\Microsoft\Skype for Desktop\Skype.exe",
                    os.path.expanduser(r"~\AppData\Local\Microsoft\SkypeApp\Skype.exe")
                ],
                "Telegram": [
                    os.path.expanduser(r"~\AppData\Roaming\Telegram Desktop\Telegram.exe")
                ],
                "Zoom": [
                    os.path.expanduser(r"~\AppData\Roaming\Zoom\bin\Zoom.exe")
                ],
                "Microsoft Teams": [
                    os.path.expanduser(r"~\AppData\Local\Microsoft\Teams\current\Teams.exe"),
                    r"C:\Program Files\Microsoft\Teams\current\Teams.exe",
                    r"C:\Program Files (x86)\Microsoft\Teams\current\Teams.exe"
                ],
                
                # Media & Entertainment
                "Spotify": [
                    os.path.expanduser(r"~\AppData\Roaming\Spotify\Spotify.exe")
                ],
                "VLC Media Player": [
                    r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                    r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
                ],
                "Windows Media Player": [
                    r"C:\Program Files\Windows Media Player\wmplayer.exe",
                    r"C:\Program Files (x86)\Windows Media Player\wmplayer.exe"
                ],
                "iTunes": [
                    r"C:\Program Files\iTunes\iTunes.exe",
                    r"C:\Program Files (x86)\iTunes\iTunes.exe"
                ],
                
                # Development Tools
                "Visual Studio Code": [
                    r"C:\Program Files\Microsoft VS Code\Code.exe",
                    r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
                    os.path.expanduser(r"~\AppData\Local\Programs\Microsoft VS Code\Code.exe")
                ],
                "Visual Studio": [
                    r"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe",
                    r"C:\Program Files\Microsoft Visual Studio\2019\Community\Common7\IDE\devenv.exe",
                    r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\Common7\IDE\devenv.exe"
                ],
                "Notepad++": [
                    r"C:\Program Files\Notepad++\notepad++.exe",
                    r"C:\Program Files (x86)\Notepad++\notepad++.exe"
                ],
                "Sublime Text": [
                    r"C:\Program Files\Sublime Text\sublime_text.exe",
                    r"C:\Program Files (x86)\Sublime Text\sublime_text.exe"
                ],
                "Atom": [
                    os.path.expanduser(r"~\AppData\Local\atom\atom.exe")
                ],
                "PyCharm": [
                    r"C:\Program Files\JetBrains\PyCharm*\bin\pycharm64.exe",
                    os.path.expanduser(r"~\AppData\Local\Programs\PyCharm*\bin\pycharm64.exe")
                ],
                
                # Microsoft Office Suite
                "Microsoft Word": [
                    r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
                    r"C:\Program Files\Microsoft Office\Office16\WINWORD.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\Office16\WINWORD.EXE",
                    r"C:\Program Files\Microsoft Office\Office15\WINWORD.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\Office15\WINWORD.EXE"
                ],
                "Microsoft Excel": [
                    r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE",
                    r"C:\Program Files\Microsoft Office\Office16\EXCEL.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\Office16\EXCEL.EXE",
                    r"C:\Program Files\Microsoft Office\Office15\EXCEL.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\Office15\EXCEL.EXE"
                ],
                "Microsoft PowerPoint": [
                    r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE",
                    r"C:\Program Files\Microsoft Office\Office16\POWERPNT.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\Office16\POWERPNT.EXE",
                    r"C:\Program Files\Microsoft Office\Office15\POWERPNT.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\Office15\POWERPNT.EXE"
                ],
                "Microsoft Outlook": [
                    r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE",
                    r"C:\Program Files\Microsoft Office\Office16\OUTLOOK.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\Office16\OUTLOOK.EXE",
                    r"C:\Program Files\Microsoft Office\Office15\OUTLOOK.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\Office15\OUTLOOK.EXE"
                ],
                "Microsoft OneNote": [
                    r"C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\ONENOTE.EXE",
                    r"C:\Program Files\Microsoft Office\Office16\ONENOTE.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\Office16\ONENOTE.EXE"
                ],
                "Microsoft Access": [
                    r"C:\Program Files\Microsoft Office\root\Office16\MSACCESS.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\MSACCESS.EXE",
                    r"C:\Program Files\Microsoft Office\Office16\MSACCESS.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\Office16\MSACCESS.EXE"
                ],
                
                # Windows Built-in Applications
                "Notepad": [
                    r"C:\Windows\System32\notepad.exe",
                    r"C:\Windows\notepad.exe"
                ],
                "Calculator": [
                    r"C:\Windows\System32\calc.exe",
                    r"C:\Windows\calc.exe"
                ],
                "Paint": [
                    r"C:\Windows\System32\mspaint.exe",
                    r"C:\Windows\mspaint.exe"
                ],
                "Command Prompt": [
                    r"C:\Windows\System32\cmd.exe"
                ],
                "PowerShell": [
                    r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
                ],
                "Task Manager": [
                    r"C:\Windows\System32\taskmgr.exe"
                ],
                "Control Panel": [
                    r"C:\Windows\System32\control.exe"
                ],
                "Registry Editor": [
                    r"C:\Windows\System32\regedt32.exe",
                    r"C:\Windows\regedit.exe"
                ],
                "File Explorer": [
                    r"C:\Windows\explorer.exe"
                ],
                "Snipping Tool": [
                    r"C:\Windows\System32\SnippingTool.exe"
                ],
                "Windows Defender": [
                    r"C:\Program Files\Windows Defender\MSASCui.exe"
                ],
                
                # Adobe Products
                "Adobe Photoshop": [
                    r"C:\Program Files\Adobe\Adobe Photoshop*\Photoshop.exe",
                    r"C:\Program Files (x86)\Adobe\Adobe Photoshop*\Photoshop.exe"
                ],
                "Adobe Illustrator": [
                    r"C:\Program Files\Adobe\Adobe Illustrator*\Support Files\Contents\Windows\Illustrator.exe"
                ],
                "Adobe Acrobat": [
                    r"C:\Program Files\Adobe\Acrobat*\Acrobat\Acrobat.exe",
                    r"C:\Program Files (x86)\Adobe\Acrobat*\Acrobat\Acrobat.exe"
                ],
                "Adobe Reader": [
                    r"C:\Program Files\Adobe\Reader*\Reader\AcroRd32.exe",
                    r"C:\Program Files (x86)\Adobe\Reader*\Reader\AcroRd32.exe"
                ],
                
                # Gaming
                "Steam": [
                    r"C:\Program Files\Steam\steam.exe",
                    r"C:\Program Files (x86)\Steam\steam.exe"
                ],
                "Epic Games Launcher": [
                    r"C:\Program Files\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe",
                    r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe"
                ],
                "Origin": [
                    r"C:\Program Files\Origin\Origin.exe",
                    r"C:\Program Files (x86)\Origin\Origin.exe"
                ],
                "Battle.net": [
                    r"C:\Program Files (x86)\Battle.net\Battle.net.exe",
                    r"C:\Program Files\Battle.net\Battle.net.exe"
                ],
                "Valorant": [
                    r"C:\Riot Games\VALORANT\live\VALORANT.exe",
                    r"C:\Program Files\Riot Games\VALORANT\live\VALORANT.exe"
                ],
                "League of Legends": [
                    r"C:\Riot Games\League of Legends\LeagueClient.exe",
                    r"C:\Program Files\Riot Games\League of Legends\LeagueClient.exe"
                ],
                "Minecraft": [
                    os.path.expanduser(r"~\AppData\Roaming\.minecraft\MinecraftLauncher.exe"),
                    r"C:\Program Files (x86)\Minecraft\MinecraftLauncher.exe"
                ],
                
                # Utilities
                "7-Zip": [
                    r"C:\Program Files\7-Zip\7zFM.exe",
                    r"C:\Program Files (x86)\7-Zip\7zFM.exe"
                ],
                "WinRAR": [
                    r"C:\Program Files\WinRAR\WinRAR.exe",
                    r"C:\Program Files (x86)\WinRAR\WinRAR.exe"
                ],
                "CCleaner": [
                    r"C:\Program Files\CCleaner\CCleaner.exe",
                    r"C:\Program Files (x86)\CCleaner\CCleaner.exe"
                ]
            }
        elif self.system == "Darwin":  # macOS
            popular_apps = {
                "Google Chrome": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"],
                "Safari": ["/Applications/Safari.app/Contents/MacOS/Safari"],
                "Firefox": ["/Applications/Firefox.app/Contents/MacOS/firefox"],
                "WhatsApp": ["/Applications/WhatsApp.app/Contents/MacOS/WhatsApp"],
                "Discord": ["/Applications/Discord.app/Contents/MacOS/Discord"],
                "Spotify": ["/Applications/Spotify.app/Contents/MacOS/Spotify"],
                "Visual Studio Code": ["/Applications/Visual Studio Code.app/Contents/MacOS/Electron"]
            }
        else:  # Linux
            popular_apps = {
                "Google Chrome": ["/usr/bin/google-chrome", "/opt/google/chrome/chrome"],
                "Firefox": ["/usr/bin/firefox", "/usr/bin/firefox-esr"],
                "Visual Studio Code": ["/usr/bin/code", "/snap/bin/code"],
                "Discord": ["/usr/bin/discord", "/snap/bin/discord"],
                "Spotify": ["/usr/bin/spotify", "/snap/bin/spotify"]
            }
        
        for app_name, paths in popular_apps.items():
            for path in paths:
                # Handle wildcard paths (for Discord on Windows)
                if '*' in path:
                    import glob
                    matching_paths = glob.glob(path)
                    if matching_paths:
                        apps[app_name] = matching_paths[0]  # Take the first match
                        break
                elif os.path.exists(path):
                    apps[app_name] = path
                    break
                    
        return apps
    
    def scan_all_applications(self) -> Dict[str, str]:
        """
        Perform a comprehensive scan for all applications.
        
        Returns:
            Dict[str, str]: Dictionary of all found applications and their paths
        """
        logger.info("Starting comprehensive application scan...")
        
        all_apps = {}
        
        # Scan popular applications first
        logger.info("Scanning for popular applications...")
        popular_apps = self.scan_popular_applications()
        all_apps.update(popular_apps)
        logger.info(f"Found {len(popular_apps)} popular applications")
        
        # Scan gaming platforms and games
        logger.info("Scanning gaming platforms and games...")
        gaming_apps = self.scan_gaming_platforms()
        all_apps.update(gaming_apps)
        logger.info(f"Found {len(gaming_apps)} games")
        
        # Scan Microsoft Office applications (Windows only)
        if self.system == "Windows":
            logger.info("Scanning Microsoft Office applications...")
            office_apps = self.scan_office_applications()
            all_apps.update(office_apps)
            logger.info(f"Found {len(office_apps)} Microsoft Office applications")
        
        # Scan Windows Store apps (Windows only)
        if self.system == "Windows":
            logger.info("Scanning Windows Store applications...")
            store_apps = self.scan_windows_store_apps()
            all_apps.update(store_apps)
            logger.info(f"Found {len(store_apps)} Windows Store applications")
        
        # Scan common directories
        logger.info("Scanning common installation directories...")
        directory_apps = self.scan_common_directories()
        all_apps.update(directory_apps)
        logger.info(f"Found {len(directory_apps)} applications in common directories")
        
        # Scan Windows registry (Windows only)
        if self.system == "Windows":
            logger.info("Scanning Windows registry...")
            registry_apps = self.scan_windows_registry()
            all_apps.update(registry_apps)
            logger.info(f"Found {len(registry_apps)} applications in registry")
        
        # Remove duplicates and clean up names
        cleaned_apps = self._clean_application_list(all_apps)
        
        logger.info(f"Total applications found: {len(cleaned_apps)}")
        return cleaned_apps
    
    def _clean_application_list(self, apps: Dict[str, str]) -> Dict[str, str]:
        """
        Clean up the application list by removing duplicates and invalid entries.
        
        Args:
            apps (Dict[str, str]): Raw application dictionary
            
        Returns:
            Dict[str, str]: Cleaned application dictionary
        """
        cleaned = {}
        seen_paths = set()
        
        for name, path in apps.items():
            # Skip if path doesn't exist
            if not os.path.exists(path):
                continue
                
            # Skip duplicates (same executable path)
            if path in seen_paths:
                continue
                
            # Clean up the application name
            clean_name = name.strip()
            
            # Skip system files and unimportant executables
            if self._should_skip_application(clean_name, path):
                continue
                
            cleaned[clean_name] = path
            seen_paths.add(path)
            
        return cleaned
    
    def _should_skip_application(self, name: str, path: str) -> bool:
        """
        Determine if an application should be skipped.
        
        Args:
            name (str): Application name
            path (str): Application path
            
        Returns:
            bool: True if the application should be skipped
        """
        skip_keywords = [
            'uninstall', 'update', 'setup', 'installer', 'helper',
            'service', 'daemon', 'background', 'crash', 'error',
            'log', 'temp', 'cache', 'test', 'debug'
        ]
        
        name_lower = name.lower()
        path_lower = path.lower()
        
        # Skip if name or path contains skip keywords
        for keyword in skip_keywords:
            if keyword in name_lower or keyword in path_lower:
                return True
        
        # Don't skip important Windows built-in applications
        important_windows_apps = [
            'notepad.exe', 'calc.exe', 'mspaint.exe', 'cmd.exe', 
            'powershell.exe', 'taskmgr.exe', 'control.exe', 
            'regedt32.exe', 'regedit.exe', 'explorer.exe'
        ]
        
        # Check if this is an important Windows app
        for important_app in important_windows_apps:
            if important_app in path_lower:
                return False
                
        # Skip system directories on Windows (but not the important apps above)
        if self.system == "Windows":
            system_dirs = ['windows\\system32', 'windows\\syswow64']
            for sys_dir in system_dirs:
                if sys_dir in path_lower:
                    return True
                    
        return False
    
    def save_to_json(self, applications: Dict[str, str] = None) -> None:
        """
        Save the applications dictionary to a JSON file.
        
        Args:
            applications (Dict[str, str], optional): Applications to save. 
                                                   If None, uses self.applications
        """
        if applications is None:
            applications = self.applications
            
        try:
            # Create directory if it doesn't exist
            output_path = Path(self.output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Prepare data for JSON
            data = {
                "scan_info": {
                    "system": self.system,
                    "scan_date": str(Path().resolve()),
                    "total_applications": len(applications)
                },
                "applications": applications
            }
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
            logger.info(f"Applications saved to {self.output_file}")
            
        except Exception as e:
            logger.error(f"Error saving applications to JSON: {e}")
            raise
    
    def load_from_json(self) -> Dict[str, str]:
        """
        Load applications from the JSON file.
        
        Returns:
            Dict[str, str]: Dictionary of applications and their paths
        """
        try:
            with open(self.output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('applications', {})
                
        except FileNotFoundError:
            logger.warning(f"JSON file {self.output_file} not found")
            return {}
        except Exception as e:
            logger.error(f"Error loading applications from JSON: {e}")
            return {}
    
    def get_application_path(self, app_name: str) -> Optional[str]:
        """
        Get the path for a specific application.
        
        Args:
            app_name (str): Name of the application
            
        Returns:
            Optional[str]: Path to the application, or None if not found
        """
        # Try exact match first
        if app_name in self.applications:
            return self.applications[app_name]
            
        # Try case-insensitive search
        for name, path in self.applications.items():
            if name.lower() == app_name.lower():
                return path
                
        # Try partial match
        for name, path in self.applications.items():
            if app_name.lower() in name.lower():
                return path
                
        return None
    
    def run_scan(self) -> Dict[str, str]:
        """
        Run a complete application scan and save results.
        
        Returns:
            Dict[str, str]: Dictionary of found applications
        """
        try:
            self.applications = self.scan_all_applications()
            self.save_to_json(self.applications)
            return self.applications
            
        except Exception as e:
            logger.error(f"Error during application scan: {e}")
            raise


def main():
    """
    Main function for standalone execution.
    """
    # Create scanner instance - save to correct path
    scanner = ApplicationScanner("../data/applications.json")
    
    try:
        # Run the scan
        applications = scanner.run_scan()
        
        print(f"\nApplication scan completed!")
        print(f"Found {len(applications)} applications")
        print(f"Results saved to: {scanner.output_file}")
        
        # Display some found applications
        print("\nSome found applications:")
        for i, (name, path) in enumerate(applications.items()):
            if i >= 10:  # Show only first 10
                print(f"... and {len(applications) - 10} more")
                break
            print(f"  {name}: {path}")
            
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    exit(main())