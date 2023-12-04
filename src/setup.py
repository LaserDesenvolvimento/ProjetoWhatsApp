from cx_Freeze import setup, Executable
import sys

executables = [Executable("whatsApp.py")]

sys.setrecursionlimit(5000)

build_exe_options = {
    "packages": ["tkinter"],
    "includes": ["tkinter"],
    "include_files": [...],
    "excludes": [...],
    "base": "Win32GUI"  # Defina isso para usar uma GUI no Windows
}


setup(
    name="WhatsApp",
    version="1.0",
    description="Processamento do WhatsApp Levy",
    executables=executables
    
)
