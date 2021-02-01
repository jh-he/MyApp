
import winreg

key_path = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe')
Chrome_path = winreg.QueryValueEx(key_path, "Path")[0]

key_version = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
Chrome_version = winreg.QueryValueEx(key_version, "Version")[0]


print(Chrome_path, Chrome_version)