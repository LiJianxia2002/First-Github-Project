import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog

# 创建应用程序对象
app = QApplication(sys.argv)

# 创建主窗口
window = QWidget()
window.setWindowTitle("乘法计算器")

# 创建标签
label1 = QLabel("输入第一个数字:")
label2 = QLabel("输入第二个数字:")
output_label = QLabel("输出文件路径:")

# 创建输入框
input1 = QLineEdit()
input2 = QLineEdit()
output_file = QLineEdit()

# 创建标签用于显示结果
result_label = QLabel("乘积: ")

# 创建按钮回调函数
def calculate_product():
    num1 = float(input1.text())
    num2 = float(input2.text())
    product = num1 * num2
    result_label.setText(f"乘积: {product}")

    # 保存结果到指定的文本文件
    output_path = output_file.text()
    if os.path.exists(output_path):
        with open(output_path, "a") as file:
            file.write(f"乘数1: {num1}, 乘数2: {num2}, 乘积: {product}\n")
    else:
        result_label.setText("文件路径无效")

# 创建按钮
calculate_button = QPushButton("计算乘积")
calculate_button.clicked.connect(calculate_product)

# 创建按钮回调函数来选择文件路径
def choose_output_file():
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly  # 只读模式
    file_path, _ = QFileDialog.getSaveFileName(window, "选择输出文件", "", "文本文件 (*.txt)", options=options)
    if file_path:
        output_file.setText(file_path)

# 创建按钮来选择文件路径
choose_file_button = QPushButton("选择输出文件")
choose_file_button.clicked.connect(choose_output_file)

# 创建布局
layout = QVBoxLayout()
layout.addWidget(label1)
layout.addWidget(input1)
layout.addWidget(label2)
layout.addWidget(input2)
layout.addWidget(output_label)
layout.addWidget(output_file)
layout.addWidget(choose_file_button)
layout.addWidget(calculate_button)
layout.addWidget(result_label)

# 设置窗口布局
window.setLayout(layout)

# 显示窗口
window.show()

# 运行应用程序
sys.exit(app.exec_())

#实现了，可以自选路径的功能，选路径，然后输出！！