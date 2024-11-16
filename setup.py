from cx_Freeze import setup, Executable
import sys

# Указываем базу для создания GUI приложения
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Указываем имя скрипта, который нужно собрать
executables = [Executable("point.py", base=base, target_name="start.exe")]

setup(
    name="YouTube Downloader",
    version="1.0",
    description="Скачивание видео с YouTube",
    executables=executables,
)
