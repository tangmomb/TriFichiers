import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os, sys

SCRIPT_TO_RUN = "Launcher.py"  # ton fichier principal

class ReloadHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.run_script()

    def run_script(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen([sys.executable, SCRIPT_TO_RUN])

    def on_modified(self, event):
        # Relancer seulement si le fichier modifié est ton script principal
        if os.path.abspath(event.src_path) == os.path.abspath(SCRIPT_TO_RUN):
            print("🔄 Changement détecté, reload...")
            self.run_script()

if __name__ == "__main__":
    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()
    print(f"Watching {SCRIPT_TO_RUN} for changes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
