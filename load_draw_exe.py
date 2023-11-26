import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QComboBox

# 创建应用程序对象
app = QApplication(sys.argv)

# 创建主窗口
window = QWidget()
window.setWindowTitle("数据解析和绘图工具")
window.setGeometry(100, 100, 500, 400)

# 创建标签和输入框
txt_label = QLabel("txt文件路径:")
txt_input = QLineEdit()
time1_label = QLabel("时间间隔1:")
time1_input = QLineEdit()
time2_label = QLabel("时间间隔2:")
time2_input = QLineEdit()
output_label = QLabel("输出图像路径:")
output_input = QLineEdit()

# 创建数据列选择框
data_label = QLabel("选择数据列:")
data_combo = QComboBox()
data_combo.addItem("1min数据", "data1")
data_combo.addItem("5min数据", "data2")
data_combo.addItem("15min数据", "data3")

# 创建宽度选择框
width_label = QLabel("选择图像宽度:")
width_combo = QComboBox()
width_combo.addItem("默认 (10)")
width_combo.addItem("5")
width_combo.addItem("10")
width_combo.addItem("15")
width_combo.addItem("20")
width_combo.addItem("25")
width_combo.addItem("30")
width_combo.addItem("35")
width_combo.addItem("40")
width_combo.addItem("45")
width_combo.addItem("50")

# 创建按钮回调函数来选择文件路径
def choose_txt_file():
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(window, "选择txt文件", "", "文本文件 (*.txt)", options=options)
    if file_path:
        txt_input.setText(file_path)

# 创建按钮回调函数来选择输出图像路径
def choose_output_file():
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly  # 只读模式
    file_path, _ = QFileDialog.getSaveFileName(window, "选择输出图像文件", "", "图像文件 (*.png)", options=options)
    if file_path:
        output_input.setText(file_path)

# 创建按钮回调函数来执行数据解析和绘图
def execute_data_processing():
    txt_file = txt_input.text()
    time1 = time1_input.text()
    time2 = time2_input.text()
    output_file = output_input.text()
    selected_data = data_combo.currentData()  # 获取当前选择的数据列
    width = width_combo.currentText().split()[0]  # 获取当前选择的宽度

    # 解析数据，将数据保存到中间 xlsx 文件
    xlsx_file = "temp.xlsx"
    data = []
    try:
        with open(txt_file, 'r') as file:
            for i, line in enumerate(file):
                if i >= 10000:
                    break
                line = line.replace(" load average:", " ")
                parts = line.split(" ", 1)
                if len(parts) == 2:
                    time = parts[0]
                    data_parts = parts[1].split(",")
                    if len(data_parts) == 3:
                        data1 = float(data_parts[0])
                        data2 = float(data_parts[1])
                        data3 = float(data_parts[2])
                        data.append({"time": time, "data1": data1, "data2": data2, "data3": data3})
    except FileNotFoundError:
        print(f"File not found: {txt_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    df = pd.DataFrame(data)
    df.to_excel(xlsx_file, index=False)

    # 绘图
    df = pd.read_excel(xlsx_file)

    filtered_data = df[(df["time"] >= time1) & (df["time"] <= time2)]

    time = filtered_data["time"]
    data = filtered_data[selected_data]

    plt.figure(figsize=(int(width), 6))
    plt.plot(time, data, marker='o', linestyle='-')
    plt.xlabel("Time")
    plt.ylabel(selected_data)
    plt.title(f"{data_combo.currentText()} vs. Time")  # 显示选择的标签
    plt.grid(True)
    
    # 添加 X 轴刻度
    plt.xticks(rotation=45)
    x_ticks = filtered_data[::120]['time']  # 每隔4分钟添加一个坐标
    plt.xticks(x_ticks, rotation=45)
    
    # 添加平均值和中位数统计，并放大三倍
    avg_data = data.mean()
    median_data = data.median()
    plt.text(time.min(), data.max(), f"Avg: {avg_data:.2f}", ha='left', va='bottom', color='blue', fontsize=12 * 3)  # 放大字号
    plt.text(time.min(), data.min(), f"Median: {median_data:.2f}", ha='left', va='top', color='blue', fontsize=12 * 3)  # 放大字号

    plt.savefig(output_file)

    # 删除中间 xlsx 文件
    os.remove(xlsx_file)

    print(f"Chart saved as {output_file}")

# 创建选择文件按钮
choose_txt_button = QPushButton("选择txt文件")
choose_txt_button.clicked.connect(choose_txt_file)

choose_output_button = QPushButton("选择输出图像文件")
choose_output_button.clicked.connect(choose_output_file)

# 创建执行按钮
execute_button = QPushButton("执行数据解析和绘图")
execute_button.clicked.connect(execute_data_processing)

# 创建布局
layout = QVBoxLayout()
layout.addWidget(txt_label)
layout.addWidget(txt_input)
layout.addWidget(time1_label)
layout.addWidget(time1_input)
layout.addWidget(time2_label)
layout.addWidget(time2_input)
layout.addWidget(data_label)
layout.addWidget(data_combo)
layout.addWidget(width_label)
layout.addWidget(width_combo)
layout.addWidget(output_label)
layout.addWidget(output_input)
layout.addWidget(choose_txt_button)
layout.addWidget(choose_output_button)
layout.addWidget(execute_button)

# 设置窗口布局
window.setLayout(layout)

# 显示窗口
window.show()

# 运行应用程序
sys.exit(app.exec_())
