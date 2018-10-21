import subprocess
import sys
import os 

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

if __name__ == '__main__':
    install('dill')
    install('pillow')
    install('PySide2')
    install('numpy')
    install('pyglet')
    install("sti-LabJackPython")
