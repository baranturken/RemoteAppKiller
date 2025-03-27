import time
import os
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
ONE_DRIVE_PATH = r"path\to\OneDrive"  # Change this to your OneDrive path
TARGET_FILE = "shutdown.txt"
ACTION_DELAY = 5
TARGET_PROCESSES = ["targetapp.exe" , "apptarget.exe"]  # Add your target apps here

def close_apps():
    """Force close all target processes"""
    closed = []
    for proc in psutil.process_iter(['name']):
        process_name = proc.info['name'].lower()
        if process_name in [p.lower() for p in TARGET_PROCESSES]:
            try:
                proc.kill()
                closed.append(process_name)
                print(f"Successfully closed {process_name}")
            except Exception as e:
                print(f"Error closing {process_name}: {e}")
    
    if not closed:
        print("No target apps were running")
    else:
        print(f"Closed {len(closed)} applications: {', '.join(closed)}")

class OneDriveHandler(FileSystemEventHandler):
    def on_created(self, event):
        self.check_file(event)
    
    def on_modified(self, event):
        self.check_file(event)
    
    def check_file(self, event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path).lower()
            if file_name == TARGET_FILE.lower():
                print(f"Detected {TARGET_FILE} - Taking action...")
                time.sleep(ACTION_DELAY)
                close_apps()
                # Remove trigger file after action
                self.cleanup_file(event.src_path)
    
    def cleanup_file(self, path):
        try:
            if os.path.exists(path):
                os.remove(path)
                print("Trigger file removed successfully")
        except Exception as e:
            print(f"Error removing file: {e}")

if __name__ == "__main__":
    event_handler = OneDriveHandler()
    observer = Observer()
    observer.schedule(event_handler, ONE_DRIVE_PATH, recursive=True)
    observer.start()

    try:
        print(f"Monitoring {ONE_DRIVE_PATH} for {TARGET_FILE}...")
        print("Target applications:", TARGET_PROCESSES)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()