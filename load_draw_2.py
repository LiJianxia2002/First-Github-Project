import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取Excel文件
file_path1 = r'D:\lijianxia\project\ACU_CPU\10.16CPU测试尝试\0911test.xlsx'
file_path2 = r'D:\lijianxia\project\ACU_CPU\10.16CPU测试尝试\1026test.xlsx'

df1 = pd.read_excel(file_path1)
df2 = pd.read_excel(file_path2)

# 选择要绘制的数据列（data1、data2、data3）
selected_data = "data1"  # 请将此处的"data1"替换为"data2"或"data3"以选择不同的数据列

# 输入时间范围
start_time1 = "15:48:00"  # 请设置文件1的开始时间
end_time1 = "16:20:00"    # 请设置文件1的结束时间

start_time2 = "10:00:00"  # 请设置文件2的开始时间
end_time2 = "10:30:00"    # 请设置文件2的结束时间

# 过滤数据，选择指定时间范围的数据
filtered_data1 = df1[(df1["time"] >= start_time1) & (df1["time"] <= end_time1)]
filtered_data2 = df2[(df2["time"] >= start_time2) & (df2["time"] <= end_time2)]

# 提取时间和选择的数据列
time1 = filtered_data1["time"]
data1 = filtered_data1[selected_data]

time2 = filtered_data2["time"]
data2 = filtered_data2[selected_data]

# 计算平均值和中位数
avg_data1 = data1.mean()
avg_data2 = data2.mean()
median_data1 = data1.median()
median_data2 = data2.median()

# 绘制图表
plt.figure(figsize=(10, 6))
plt.plot(time1, data1, marker='o', linestyle='-', label="0911")
plt.plot(time2, data2, marker='o', linestyle='-', label="1026")
plt.xlabel("Time")
plt.ylabel(selected_data)
plt.title(f"{selected_data} vs. Time")
plt.grid(True)
plt.xticks(np.arange(0, 1500, 150))
plt.legend()

# 添加平均值和中位数的标注
plt.text(time1.min(), data1.max(), f"Avg Data1: {avg_data1:.2f}", ha='left', va='bottom', color='blue')
plt.text(time2.min(), data2.max(), f"Avg Data2: {avg_data2:.2f}", ha='left', va='bottom', color='orange')
plt.text(time1.min(), data1.min(), f"Median Data1: {median_data1:.2f}", ha='left', va='top', color='blue')
plt.text(time2.min(), data2.min(), f"Median Data2: {median_data2:.2f}", ha='left', va='top', color='orange')

# 保存图表为PNG文件
output_file = r'D:\lijianxia\project\ACU_CPU\10.16CPU测试尝试\test.png'
plt.savefig(output_file)

# 显示图表
plt.show()

print(f"Chart saved as {output_file}")

