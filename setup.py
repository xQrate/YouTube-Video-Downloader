from cx_Freeze import setup, Executable
import sys

# Настройки сборки
build_options = {
    "packages": ["tkinter", "os", "yt_dlp", "time", "socket", "threading", "sys"],
    "excludes": [],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Используется для GUI-приложений

# Конфигурация
setup(
    name="MyApp",
    version="1.0",
    description="YouTube Video Downloader",
    options={"build_exe": build_options},
    executables=[Executable("point.py", base=base)],  # Укажите ваш главный файл
)
