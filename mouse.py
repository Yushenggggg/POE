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
move_interval = 0.01  # 默認移動間隔
angle_increment = 5   # 默認角度增量
running = False

# 繪製圓形
def draw_circle():
    global running, center_x, center_y, move_interval, angle_increment, radius
    while running:
        for angle in range(0, 360, angle_increment):
            if not running:
                break
            radians = math.radians(angle)
            x = int(center_x + radius * math.cos(radians))
            y = int(center_y + radius * math.sin(radians))
            pyautogui.moveTo(x, y, duration=0.01)
            time.sleep(move_interval)

# 繪製菱形
def draw_diamond():
    global running, center_x, center_y, move_interval, radius
    while running:
        points = [
            (center_x, center_y - radius),  # 上
            (center_x + radius, center_y),  # 右
            (center_x, center_y + radius),  # 下
            (center_x - radius, center_y)   # 左
        ]
        for point in points:
            if not running:
                break
            pyautogui.moveTo(point[0], point[1], duration=0.01)
        # 减少绘制间隔，提升绘制速度
        time.sleep(move_interval / 2)

# 根據選擇的形狀進行繪製
def select_shape(value):
    global draw_function
    if value == "Circle":
        draw_function = draw_circle
    elif value == "Diamond":
        draw_function = draw_diamond

draw_function = draw_circle  # 默認為畫圈

def start_drawing():
    global running
    running = True
    threading.Thread(target=draw_function, daemon=True).start()

def stop_drawing():
    global running
    running = False

def manual_update_resolution():
    global center_x, center_y
    try:
        width = int(width_entry.get())
        height = int(height_entry.get())
        center_x, center_y = width // 2, height // 2
    except ValueError:
        pass

def update_move_interval(value):
    global move_interval
    move_interval = float(value) / 1000.0  # Convert slider value to seconds

def update_angle_increment(value):
    global angle_increment
    angle_increment = int(value)

def update_radius(value):
    global radius
    radius = int(value)

def listen_for_escape():
    while True:
        if keyboard.is_pressed('esc'):
            stop_drawing()
        time.sleep(0.1)

def listen_for_alt_f12():
    while True:
        if keyboard.is_pressed('alt+f12'):
            start_drawing()
        time.sleep(0.1)

# 創建主窗口
root = tk.Tk()
root.title("Mouse Circle Drawer")
root.geometry("300x600+300+300")  # 調整窗口大小

# 解析度輸入框和按鈕
frame_resolution = tk.Frame(root)
frame_resolution.pack(pady=10)

tk.Label(frame_resolution, text="螢幕寬度:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
width_entry = tk.Entry(frame_resolution)
width_entry.grid(row=0, column=1, padx=5, pady=5)
width_entry.insert(0, "1920")  # 默認值

tk.Label(frame_resolution, text="螢幕高度:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
height_entry = tk.Entry(frame_resolution)
height_entry.grid(row=1, column=1, padx=5, pady=5)
height_entry.insert(0, "1080")  # 默認值

manual_update_button = tk.Button(frame_resolution, text="更新解析度", command=manual_update_resolution)
manual_update_button.grid(row=2, columnspan=2, pady=10)

# 移動速度滑塊
frame_speed = tk.Frame(root)
frame_speed.pack(pady=10)

tk.Label(frame_speed, text="移動速度(毫秒):", font=("Arial", 12)).pack(pady=5)
speed_slider = tk.Scale(frame_speed, from_=1, to_=100, orient=tk.HORIZONTAL, command=update_move_interval)
speed_slider.set(10)  # 默認值
speed_slider.pack(pady=5)

# 旋轉角度增量滑塊
frame_angle = tk.Frame(root)
frame_angle.pack(pady=10)

tk.Label(frame_angle, text="移動角度:", font=("Arial", 12)).pack(pady=5)
angle_slider = tk.Scale(frame_angle, from_=1, to_=10, orient=tk.HORIZONTAL, command=update_angle_increment)
angle_slider.set(5)  # 默認值
angle_slider.pack(pady=5)

# 半徑滑塊
frame_radius = tk.Frame(root)
frame_radius.pack(pady=10)

tk.Label(frame_radius, text="半徑:", font=("Arial", 12)).pack(pady=5)
radius_slider = tk.Scale(frame_radius, from_=50, to_=500, orient=tk.HORIZONTAL, command=update_radius)
radius_slider.set(200)  # 默認值
radius_slider.pack(pady=5)

# 形狀選擇
frame_shape = tk.Frame(root)
frame_shape.pack(pady=10)

tk.Label(frame_shape, text="Select Shape:", font=("Arial", 12)).pack(pady=5)
shape_var = tk.StringVar(value="Circle")
shape_menu = tk.OptionMenu(frame_shape, shape_var, "Circle", "Diamond", command=select_shape)
shape_menu.pack()

# 創建啟動和停止按鈕
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

start_button = tk.Button(frame_buttons, text="START", command=start_drawing)
start_button.grid(row=0, column=0, padx=5)

stop_button = tk.Button(frame_buttons, text="STOP", command=stop_drawing)
stop_button.grid(row=0, column=1, padx=5)

# 啟動監聽ESC鍵和ALT+F12鍵的線程
threading.Thread(target=listen_for_escape, daemon=True).start()
threading.Thread(target=listen_for_alt_f12, daemon=True).start()

# 運行主循環
root.mainloop()
