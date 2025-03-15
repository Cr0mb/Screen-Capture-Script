import pyautogui
import tkinter as tk
from tkinter import Canvas
from PIL import Image
import time

class ScreenCaptureApp:
    def __init__(self, capture_type):
        self.capture_type = capture_type
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.root.configure(bg='gray')
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.canvas = Canvas(self.root, cursor="cross", bg='gray')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.selection_rect = None
        self.frames = []
        self.capture_duration = 3
        self.frame_rate = 10
        self.root.mainloop()

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
        self.selection_rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_drag(self, event):
        self.end_x, self.end_y = event.x, event.y
        self.canvas.coords(self.selection_rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_release(self, event):
        self.end_x, self.end_y = event.x, event.y
        self.root.destroy()
        if self.capture_type == 'screenshot':
            self.capture_screenshot()
        elif self.capture_type == 'gif':
            self.capture_gif()

    def capture_screenshot(self):
        x1, y1, x2, y2 = min(self.start_x, self.end_x), min(self.start_y, self.end_y), max(self.start_x, self.end_x), max(self.start_y, self.end_y)
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        screenshot.save("screenshot.png")
        print("Screenshot saved as screenshot.png")

    def capture_gif(self):
        x1, y1, x2, y2 = min(self.start_x, self.end_x), min(self.start_y, self.end_y), max(self.start_x, self.end_x), max(self.start_y, self.end_y)
        
        start_time = time.time()
        while time.time() - start_time < self.capture_duration:
            screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
            self.frames.append(screenshot)
            time.sleep(1 / self.frame_rate)

        self.frames[0].save("capture.gif", save_all=True, append_images=self.frames[1:], duration=1000 / self.frame_rate, loop=0)
        print("GIF saved as capture.gif")


def menu():
    print("Select capture type:")
    print("1. Screenshot")
    print("2. GIF")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == '1':
        ScreenCaptureApp('screenshot')
    elif choice == '2':
        ScreenCaptureApp('gif')
    else:
        print("Invalid choice. Please select 1 or 2.")
        menu()

if __name__ == "__main__":
    menu()
