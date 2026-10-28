import os
import subprocess
import shutil
from datetime import datetime
import pyautogui
import time
import psutil
import screen_brightness_control as sbc

class FileManager:
    def __init__(self):
        # Base directory for all Sara data
        self.base_dir = "E:\\sara-data"
        self.screenshots_dir = os.path.join(self.base_dir, "screenshots")
        self.notes_dir = os.path.join(self.base_dir, "notes")
        self.folders_dir = os.path.join(self.base_dir, "folders")
        self.music_dir = os.path.join(self.base_dir, "music")
        
        # Create directories if they don't exist
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories"""
        try:
            os.makedirs(self.screenshots_dir, exist_ok=True)
            os.makedirs(self.notes_dir, exist_ok=True)
            os.makedirs(self.folders_dir, exist_ok=True)
            os.makedirs(self.music_dir, exist_ok=True)
            print(f"✅ Sara data directories created at: {self.base_dir}")
        except Exception as e:
            print(f"❌ Error creating directories: {e}")

    def open_folder(self, folder_name):
        """Search and open any folder by name using Windows search"""
        try:
            # Method 1: Use Windows Run dialog with shell command
            try:
                # This method directly opens the folder if it exists in common locations
                subprocess.Popen(f'explorer "{folder_name}"', shell=True)
                return f"📁 Opening folder: {folder_name}"
            except:
                pass
            
            # Method 2: Use Windows File Explorer search
            try:
                pyautogui.hotkey('win', 'e')  # Open File Explorer
                time.sleep(2)
                
                # Focus on search bar
                pyautogui.hotkey('ctrl', 'f')  # Focus search box
                time.sleep(0.5)
                
                # Type folder name
                pyautogui.write(folder_name)
                time.sleep(2)  # Wait for search results
                
                # Press Enter to select first result
                pyautogui.press('enter')
                time.sleep(1)
                
                return f"📁 Searching and opening folder: {folder_name}"
            except:
                pass
            
            # Method 3: Try common folder locations
            common_folders = {
                'documents': 'Documents',
                'downloads': 'Downloads',
                'pictures': 'Pictures',
                'music': 'Music',
                'videos': 'Videos',
                'desktop': 'Desktop',
            }
            
            folder_lower = folder_name.lower()
            for key, folder in common_folders.items():
                if key in folder_lower:
                    try:
                        subprocess.Popen(f'explorer "{folder}"', shell=True)
                        return f"📁 Opening {folder} folder"
                    except:
                        pass
            
            return f"📁 Attempted to open folder: {folder_name}. If not found, please check the name."
            
        except Exception as e:
            return f"❌ Error opening folder: {e}"

    def get_music_files(self):
        """Get list of music files from music directory"""
        try:
            music_files = []
            supported_formats = ['.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac']
            
            for file in os.listdir(self.music_dir):
                if any(file.lower().endswith(ext) for ext in supported_formats):
                    music_files.append(os.path.join(self.music_dir, file))
            
            return music_files
        except Exception as e:
            print(f"❌ Error getting music files: {e}")
            return []

    def set_brightness(self, level):
        """Set screen brightness (0-100)"""
        try:
            level = max(0, min(100, level))
            sbc.set_brightness(level)
            return f"💡 Brightness set to {level}%"
        except Exception as e:
            return f"❌ Error setting brightness: {e}"

    def increase_brightness(self, points=1):
        """Increase screen brightness by specified points"""
        try:
            current = sbc.get_brightness()[0]
            new_level = min(100, current + points)
            sbc.set_brightness(new_level)
            return f"💡 Brightness increased by {points} points to {new_level}%"
        except Exception as e:
            return f"❌ Error increasing brightness: {e}"

    def decrease_brightness(self, points=1):
        """Decrease screen brightness by specified points"""
        try:
            current = sbc.get_brightness()[0]
            new_level = max(0, current - points)
            sbc.set_brightness(new_level)
            return f"💡 Brightness decreased by {points} points to {new_level}%"
        except Exception as e:
            return f"❌ Error decreasing brightness: {e}"

    def get_brightness(self):
        """Get current brightness level"""
        try:
            brightness = sbc.get_brightness()[0]
            return f"💡 Current brightness: {brightness}%"
        except Exception as e:
            return f"❌ Error getting brightness: {e}"

    # ... [Keep all your existing methods below - open_application, close_application, etc.]
    @staticmethod
    def open_application(app_name):
        """Open any application using Windows search"""
        try:
            # Clean the app name
            app_name = app_name.strip()
            
            # Common apps quick access (optional optimization)
            quick_apps = {
                'calculator': 'calc.exe',
                'notepad': 'notepad.exe',
                'paint': 'mspaint.exe',
                'cmd': 'cmd.exe',
                'task manager': 'taskmgr.exe',
                'file explorer': 'explorer.exe',
                'browser': 'start msedge.exe',
                'chrome': 'start chrome.exe',
                'firefox': 'start firefox.exe',
                'powershell': 'powershell.exe',
                'control panel': 'control.exe',
                'settings': 'start ms-settings:',
            }
            
            # Check quick apps first
            app_name_lower = app_name.lower()
            for key, command in quick_apps.items():
                if key in app_name_lower:
                    try:
                        subprocess.Popen(command, shell=True)
                        return f"🚀 Opening {key.title()}"
                    except Exception as e:
                        break  # If common app fails, try search method
            
            # Use Windows search to open any app
            return FileManager._open_via_windows_search(app_name)
            
        except Exception as e:
            return f"❌ Error opening {app_name}: {e}"

    @staticmethod
    def _open_via_windows_search(app_name):
        """Open application using Windows search feature"""
        try:
            # Press Windows key to open start menu/search
            pyautogui.press('win')
            time.sleep(0.5)
            
            # Type the application name
            pyautogui.write(app_name)
            time.sleep(1)  # Wait for search results
            
            # Press Enter to open the top result
            pyautogui.press('enter')
            
            return f"🔍 Opening {app_name.title()} via Windows Search"
            
        except Exception as e:
            # Fallback without pyautogui
            try:
                # Try using Windows start command
                subprocess.Popen(f'start {app_name}', shell=True)
                return f"📋 Attempting to open: {app_name.title()}"
            except:
                return f"🔍 Please manually search for '{app_name}' in Start Menu"

    @staticmethod
    def close_application(app_name):
        """Close application by name"""
        try:
            app_name_lower = app_name.lower().strip()
            
            # Common app process names mapping
            app_processes = {
                'calculator': 'calculator.exe',
                'notepad': 'notepad.exe',
                'paint': 'mspaint.exe',
                'chrome': 'chrome.exe',
                'firefox': 'firefox.exe',
                'edge': 'msedge.exe',
                'word': 'winword.exe',
                'excel': 'excel.exe',
                'powerpoint': 'powerpnt.exe',
                'file explorer': 'explorer.exe',
                'command prompt': 'cmd.exe',
                'powershell': 'powershell.exe'
            }
            
            # Try to find and close the app
            closed_count = 0
            for proc in psutil.process_iter(['name', 'pid']):
                try:
                    process_name = proc.info['name'].lower()
                    
                    # Check if it matches common app names
                    for app_key, process_pattern in app_processes.items():
                        if app_key in app_name_lower and process_pattern in process_name:
                            proc.terminate()
                            closed_count += 1
                            break
                    
                    # Also check if process name contains the app name
                    if app_name_lower in process_name:
                        proc.terminate()
                        closed_count += 1
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            if closed_count > 0:
                return f"❌ Closed {closed_count} process(es) for {app_name.title()}"
            else:
                return f"⚠️ No running processes found for {app_name.title()}. Try closing manually."
                
        except Exception as e:
            return f"❌ Error closing application: {e}"

    def create_folder(self, folder_name):
        """Create a new folder inside sara-data/folders"""
        try:
            # Remove any invalid characters from folder name
            folder_name = "".join(c for c in folder_name if c not in '<>:"/\\|?*')
            folder_path = os.path.join(self.folders_dir, folder_name)
            
            os.makedirs(folder_path, exist_ok=True)
            return f"📁 Folder created: {folder_path}"
        except Exception as e:
            return f"❌ Error creating folder: {e}"

    def take_screenshot(self):
        """Take screenshot and save in sara-data/screenshots"""
        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.screenshots_dir, filename)
            screenshot.save(filepath)
            return f"📸 Screenshot saved as {filepath}"
        except ImportError:
            return "❌ PIL library not available for screenshots. Install with: pip install pillow"
        except Exception as e:
            return f"❌ Error taking screenshot: {e}"

    # ... [Rest of your existing methods remain the same]

    # ... [Rest of your existing methods remain the same]

    def get_file_info(self, path=None):
        """Get information about files in directory"""
        try:
            if path is None:
                path = self.base_dir
            
            files = os.listdir(path)
            file_info = f"📁 Files in {path}:\n\n"
            
            for file in files[:15]:  # Show first 15 files
                full_path = os.path.join(path, file)
                if os.path.isfile(full_path):
                    size = os.path.getsize(full_path)
                    modified_time = datetime.fromtimestamp(os.path.getmtime(full_path))
                    file_info += f"📄 {file}\n   Size: {size} bytes | Modified: {modified_time.strftime('%Y-%m-%d %H:%M')}\n"
                else:
                    file_info += f"📂 {file} (Folder)\n"
            
            if len(files) > 15:
                file_info += f"\n... and {len(files) - 15} more items"
                
            return file_info
        except Exception as e:
            return f"❌ Error reading directory: {e}"
    
    def delete_file(self, file_path):
        """Delete a file"""
        try:
            if os.path.exists(file_path):
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    return f"🗑️ File deleted: {file_path}"
                else:
                    return f"❌ {file_path} is not a file"
            else:
                return f"❌ File not found: {file_path}"
        except Exception as e:
            return f"❌ Error deleting file: {e}"
    
    def get_system_info(self):
        """Get basic system information"""
        try:
            system_info = "💻 SYSTEM QUICK INFO:\n\n"
            
            # Current directory
            current_dir = os.getcwd()
            system_info += f"📁 Current Directory: {current_dir}\n"
            
            # Sara data directory
            system_info += f"📂 Sara Data Location: {self.base_dir}\n"
            
            # Username
            username = os.getenv('USERNAME') or os.getenv('USER')
            system_info += f"👤 User: {username}\n"
            
            # Disk information
            total, used, free = shutil.disk_usage("/")
            total_gb = total // (2**30)
            used_gb = used // (2**30)
            free_gb = free // (2**30)
            system_info += f"💾 Disk: {used_gb}GB / {total_gb}GB used ({free_gb}GB free)\n"
            
            # CPU count
            cpu_count = os.cpu_count()
            system_info += f"⚙️ CPU Cores: {cpu_count}\n"
            
            return system_info
        except Exception as e:
            return f"❌ Error getting system info: {e}"
    
    def search_files(self, search_term, directory=None):
        """Search for files containing search term"""
        try:
            if directory is None:
                directory = self.base_dir
            
            matching_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if search_term.lower() in file.lower():
                        matching_files.append(os.path.join(root, file))
            
            if matching_files:
                result = f"🔍 Found {len(matching_files)} files matching '{search_term}':\n\n"
                for file in matching_files[:10]:  # Show first 10 results
                    result += f"📄 {file}\n"
                if len(matching_files) > 10:
                    result += f"\n... and {len(matching_files) - 10} more files"
                return result
            else:
                return f"🔍 No files found matching '{search_term}'"
        except Exception as e:
            return f"❌ Error searching files: {e}"
    
    def get_folder_size(self, path=None):
        """Calculate total size of folder"""
        try:
            if path is None:
                path = self.base_dir
            
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
            
            size_mb = total_size / (1024 * 1024)
            return f"📊 Folder size: {size_mb:.2f} MB"
        except Exception as e:
            return f"❌ Error calculating folder size: {e}"
    
    def copy_file(self, source, destination):
        """Copy file to destination"""
        try:
            shutil.copy2(source, destination)
            return f"📋 File copied: {source} → {destination}"
        except Exception as e:
            return f"❌ Error copying file: {e}"
    
    def move_file(self, source, destination):
        """Move file to destination"""
        try:
            shutil.move(source, destination)
            return f"🚚 File moved: {source} → {destination}"
        except Exception as e:
            return f"❌ Error moving file: {e}"
    
    def rename_file(self, old_name, new_name):
        """Rename a file"""
        try:
            os.rename(old_name, new_name)
            return f"✏️ File renamed: {old_name} → {new_name}"
        except Exception as e:
            return f"❌ Error renaming file: {e}"
    
    def get_file_count(self, directory=None):
        """Count files and folders in directory"""
        try:
            if directory is None:
                directory = self.base_dir
            
            files = []
            folders = []
            
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path):
                    files.append(item)
                else:
                    folders.append(item)
            
            return f"📊 Directory Statistics:\n📄 Files: {len(files)}\n📂 Folders: {len(folders)}\n📦 Total: {len(files) + len(folders)} items"
        except Exception as e:
            return f"❌ Error counting files: {e}"
    
    def shutdown_computer(self, seconds=60):
        """Shutdown the computer"""
        try:
            os.system(f"shutdown /s /t {seconds}")
            return f"🖥️ Computer will shutdown in {seconds} seconds. Type 'shutdown /a' in cmd to cancel."
        except Exception as e:
            return f"❌ Error initiating shutdown: {e}"
    
    def restart_computer(self, seconds=60):
        """Restart the computer"""
        try:
            os.system(f"shutdown /r /t {seconds}")
            return f"🖥️ Computer will restart in {seconds} seconds. Type 'shutdown /a' in cmd to cancel."
        except Exception as e:
            return f"❌ Error initiating restart: {e}"
    
    def cancel_shutdown():
        """Cancel scheduled shutdown/restart"""
        try:
            os.system("shutdown /a")
            return "✅ Scheduled shutdown/restart cancelled"
        except Exception as e:
            return f"❌ Error cancelling shutdown: {e}"