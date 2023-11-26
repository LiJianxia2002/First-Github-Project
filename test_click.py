import pyautogui
import time

def get_mouse_position():
    try:
        x, y = pyautogui.position()
        print(f"X: {x}, Y: {y}")
    except Exception as e:
        print("Error: Unable to get mouse position.")
        print(e)

while True:
    get_mouse_position()
    time.sleep(0.1)  # 每隔1秒输出一次鼠标位置






