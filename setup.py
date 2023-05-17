from cx_Freeze import setup, Executable
import sys

executables = [Executable("whatsApp.py")]

sys.setrecursionlimit(5000)

setup(
    name="WhatsApp",
    version="1.0",
    description="Processamento do WhatsApp Levy",
    executables=executables
    
)
