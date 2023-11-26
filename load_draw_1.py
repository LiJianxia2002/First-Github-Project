import pandas as pd
import matplotlib.pyplot as plt

# 读取Excel文件
file_path = r'D:\lijianxia\project\ACU_CPU\10.16CPU测试尝试\1026test.xlsx'
df = pd.read_excel(file_path)

# 选择要绘制的数据列（data1、data2、data3）
selected_data = "data1"  # 请将此处的"data1"替换为"data2"或"data3"以选择不同的数据列

# 输入时间范围
start_time = "10:00:00"  # 请设置开始时间
end_time = "10:20:00"    # 请设置结束时间

# 过滤数据，选择指定时间范围的数据
filtered_data = df[(df["time"] >= start_time) & (df["time"] <= end_time)]

# 提取时间和选择的数据列
time = filtered_data["time"]
data = filtered_data[selected_data]

# 绘制图表
plt.figure(figsize=(10, 6))
plt.plot(time, data, marker='o', linestyle='-')
plt.xlabel("Time")
plt.ylabel(selected_data)
plt.title(f"{selected_data} vs. Time")
plt.grid(True)

# 保存图表为PNG文件
output_file = r'D:\lijianxia\project\ACU_CPU\10.16CPU测试尝试\test.png'
plt.savefig(output_file)

# 显示图表
plt.show()

print(f"Chart saved as {output_file}")
