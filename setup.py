from cx_Freeze import setup, Executable
import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Используется для GUI-приложений


setup(
    name="YouTube Video Downloader",
    version="1.0",
    
    description="Приложение для загрузки видео с YouTube",
    executables=[Executable("point.py")],
    options={
        "build_exe": {
            "packages": ["os", "tkinter", "yt_dlp", "requests", "bs4", "speedtest"],
            "includes": ["speedtest"],

            
        }
    }
)


