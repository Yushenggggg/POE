import tkinter as tk
import pyautogui
import time
import math
import threading
import keyboard

# 解析度選項
resolutions = {
    "1920x1080": (1920, 1080),
    "1478x831": (1478, 831),
    "1280x720": (1280, 720),
    "1133x638": (1133, 638),
    "1067x600": (1067, 600)
}

# 初始化全局變量
center_x, center_y = 1920 // 2, 1080 // 2
radius = 200
move_interval = 0.01
running = False

def draw_circle():
    global running, center_x, center_y
    while running:
        for angle in range(0, 360, 5):
            if not running:
                break
            radians = math.radians(angle)
            x = int(center_x + radius * math.cos(radians))
            y = int(center_y + radius * math.sin(radians))
            pyautogui.moveTo(x, y, duration=0.01)
            time.sleep(move_interval)

def start_drawing():
    global running
    running = True
    threading.Thread(target=draw_circle, daemon=True).start()

def stop_drawing():
    global running
    running = False

def update_resolution(resolution):
    global center_x, center_y
    width, height = resolutions[resolution]
    center_x, center_y = width // 2, height // 2

def listen_for_escape():
    while True:
        if keyboard.is_pressed('esc'):
            stop_drawing()
        time.sleep(0.1)

# 创建主窗口
root = tk.Tk()
root.title("Mouse Circle Drawer")

# 解析度选择下拉菜单
resolution_var = tk.StringVar(value="1920x1080")
resolution_menu = tk.OptionMenu(root, resolution_var, *resolutions.keys(), command=update_resolution)
resolution_menu.pack(pady=10)

# 创建启动和停止按钮
start_button = tk.Button(root, text="Start", command=start_drawing)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_drawing)
stop_button.pack(pady=10)

# 启动监听ESC键的线程
threading.Thread(target=listen_for_escape, daemon=True).start()

# 运行主循环
root.mainloop()
