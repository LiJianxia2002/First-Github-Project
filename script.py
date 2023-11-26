import subprocess
import time
import pyautogui
from pynput.keyboard import Key, Controller

def open_mqtt_sender():
    # 替换为你的MQTT发送软件的可执行文件路径
    mqtt_sender_path = "D:\lijianxia\software\通信猫MQTT调试客户端\MQTT调试客户端.exe"
    
    # 使用subprocess打开MQTT发送软件
    subprocess.Popen([mqtt_sender_path])
    
    time.sleep(1)

def click_and_type(x, y, text):
    pyautogui.click(x, y)
    press_ctrl_and_a()
    pyautogui.typewrite(text)

def press_ctrl_and_a():
    # 创建一个键盘控制器
    keyboard = Controller()

    # 按下Ctrl键
    keyboard.press(Key.ctrl)

    # 按下A键
    keyboard.press('a')

    # 松开A键
    keyboard.release('a')

    # 松开Ctrl键
    keyboard.release(Key.ctrl)

if __name__ == "__main__":
    open_mqtt_sender()
    
    # 替换为你想要订阅的内容和发送的内容
    
    subscription_R = "/tbox/v11/dev/cmd/adv-gt-114/"

    subscription_T = "/tbox/v11/dev/info/adv-gt-114/"

    
    message = "09 00 12 01 76 F0 48 1D 68 02 05 01 01 02 01 03 01 04 01 05 01 AF "

    I_P="120.77.227.61"

    port="1883"


    
    # 替换为你正确输入订阅内容的输入框位置坐标

    subscription_input_x, subscription_input_y = 810, 624
    # 替换为你正确输入发送内容的输入框位置坐标
    message_input_x, message_input_y = 831, 702
    
    # 点击并输入订阅内容
    click_and_type(subscription_input_x, subscription_input_y, subscription_T)
    
    # 点击并输入发送内容

    click_and_type(813,384,I_P)

    click_and_type(937,384,port)

    click_and_type(831,657,subscription_R)

    pyautogui.click(1157, 386)

    time.sleep(1)

    click_and_type(message_input_x, message_input_y, message)

    time.sleep(1)

    pyautogui.click(908, 625) #订阅

    pyautogui.click(1096, 696) #发送指令
 
    time.sleep(2)
    
    pyautogui.click(1096, 696) #发送指令





 #D:\lijianxia\software\通信猫MQTT调试客户端\MQTT调试客户端.exe