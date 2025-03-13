import os
import threading
import time
import win32api
import win32con
import win32gui

from objects.buttons.button import *

class ShutdownButton(Button):
    """Close all windows and shutdown after 30 seconds"""
    def __init__(self, parent):
        super().__init__(parent, "Shutdown")
        self.time_windows = 20  # time for closing windows
        self.time_shutdown = 30  # time for shutdown
        self.set_tooltip("Shutdown after 30 seconds")

    def execute(self):
        try:
            def enum_handler(hwnd, windows):
                """Enum all windows"""
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if (window_title and 
                        TITLE not in window_title and 
                        "Program Manager" not in window_title and
                        "Windows Input" not in window_title and
                        "Input Method" not in window_title and
                        "Windows 입력 환경" not in window_title and
                        "Install" not in window_title and
                        "Setup" not in window_title and
                        "설치" not in window_title and
                        "JamPostMessageWindow" not in window_title):
                        # Exclude system windows and self's program
                        windows.append((hwnd, window_title))

            def save_and_close_window(hwnd, title):
                try:
                    # Programs that need to be saved
                    need_save_programs = [
                        "Notepad", "메모장",
                        "Excel", "엑셀",
                        "Word", "워드",
                        "PowerPoint", "파워포인트",
                        "Cursor",
                        "Sublime Text"
                    ]
                    
                    # Check if the program needs to be saved
                    if any(prog in title for prog in need_save_programs):
                        # Send Ctrl + S key event
                        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                        win32api.keybd_event(ord('S'), 0, 0, 0)
                        win32api.keybd_event(ord('S'), 0, win32con.KEYEVENTF_KEYUP, 0)
                        win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
                        
                        # Wait for the save dialog to appear
                        time.sleep(0.5)
                        
                        # Send Enter key (save confirmation)
                        win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
                        win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
                        
                        # Wait for the save to complete
                        time.sleep(0.5)
                    
                    # Close the window
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                except:
                    pass

            def close_windows():
                """Close all windows"""
                time.sleep(self.time_windows)

                # Get all windows
                windows = []
                win32gui.EnumWindows(enum_handler, windows)

                threads = []
                for hwnd, title in windows:
                    try:
                        thread = threading.Thread(
                            target=save_and_close_window,
                            args=(hwnd, title),
                            daemon=True  # Exit when the main program exits
                        )
                        threads.append(thread)
                    except Exception:
                        continue

                # Start all threads at once
                for thread in threads:
                    thread.start()

                # Wait for all threads to complete
                for thread in threads:
                    thread.join(timeout=self.time_shutdown-self.time_windows)

            result = QMessageBox.question(
                self.parent,
                "Shutdown",
                "30 seconds after the system will be shutdown. Continue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if result == QMessageBox.StandardButton.Yes:
                os.system(f"shutdown /s /t {self.time_shutdown}")
                threading.Thread(target=close_windows).start()
            
        except Exception as e:
            show_error("Error", f"Error: {str(e)}")
            