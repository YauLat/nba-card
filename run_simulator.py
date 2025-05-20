import time
import sys
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_simulator()

    def start_simulator(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        print("\n" + "="*50)
        print("🚀 啟動 NBA 球星卡抽卡模擬器...")
        print("="*50 + "\n")
        self.process = subprocess.Popen([sys.executable, "nba_card_simulator.py"])

    def on_modified(self, event):
        if event.src_path.endswith("nba_card_simulator.py"):
            print("\n" + "="*50)
            print("🔄 檢測到程式碼變更，重新啟動模擬器...")
            print("="*50 + "\n")
            self.start_simulator()

def main():
    # 創建事件處理器
    event_handler = CodeChangeHandler()
    
    # 創建觀察者
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        if event_handler.process:
            event_handler.process.terminate()
        observer.stop()
        print("\n" + "="*50)
        print("👋 程式已關閉")
        print("="*50 + "\n")
    
    observer.join()

if __name__ == "__main__":
    main() 