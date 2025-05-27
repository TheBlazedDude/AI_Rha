
import sys
import threading
from gui import main_gui

def start_gui():
    main_gui.run_gui()

if __name__ == "__main__":
    threading.Thread(target=start_gui).start()
