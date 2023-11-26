import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('File Path Selector')

        # 创建标签
        self.input_label = QLabel('Input Folder Path:')
        self.output_label = QLabel('Output File Path:')

        # 创建按钮
        self.input_button = QPushButton('Select Input Folder')
        self.output_button = QPushButton('Select Output File')

        # 创建确认按钮
        self.confirm_button = QPushButton('Run Code')

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_button)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

        # 为按钮添加点击事件
        self.input_button.clicked.connect(self.select_input_folder)
        self.output_button.clicked.connect(self.select_output_file)
        self.confirm_button.clicked.connect(self.run_code)

    def select_input_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Input Folder')
        self.input_label.setText(f'Input Folder Path: {folder_path}')

    def select_output_file(self):
        output_path, _ = QFileDialog.getSaveFileName(self, 'Select Output File', filter='Excel Files (*.xlsx)')
        self.output_label.setText(f'Output File Path: {output_path}')

    def run_code(self):
        input_folder = self.input_label.text().split(': ')[-1]
        output_file = self.output_label.text().split(': ')[-1]

        # 使用你提供的代码来处理数据
        data = pd.DataFrame(columns=['Time', 'PID', 'TIME+', 'File_Name'])

        for filename in os.listdir(input_folder):
           if filename.endswith('.txt') and 'load' not in filename and 'idle' not in filename:

                file_path = os.path.join(input_folder, filename)
                try:
                    df = pd.read_csv(file_path, sep=' ', names=['Time', 'PID', 'TIME+'])
                    file_name = os.path.splitext(filename)[0]
                    df['File_Name'] = file_name
                    data = pd.concat([data, df], ignore_index=True)
                except Exception as e:
                    print(f"Error processing file {filename}: {str(e)}")

        data.to_excel(output_file, index=False)
        print(f"Data saved to {output_file}")


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


