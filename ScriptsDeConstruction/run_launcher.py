import os
import sys
import subprocess

# Chemin vers ton launcher.py
launcher_path = os.path.join(os.path.dirname(sys.executable), "Launcher.py")

# Lancer le launcher
subprocess.run([sys.executable, launcher_path])
