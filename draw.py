import pandas as pd
import matplotlib.pyplot as plt

# 读取 Excel 文件
excel_file = r'C:\Users\一清\Desktop\CPU_Test1110\test1110.xlsx'
df = pd.read_excel(excel_file)

# 删除包含 NaN 值的行
df.dropna(subset=['Time', 'Data1', 'Data2', 'File_Name'], inplace=True)

# 过滤掉时间以10开头的数据
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')
# df = df[~df['Time'].dt.strftime('%H').str.startswith('15')] #可以实现排除小时的读取

start_time = '15:30:00'
end_time = '15:32:00'

df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')

df = df[(df['Time'].dt.time >= pd.to_datetime(start_time).time()) & 
        (df['Time'].dt.time <= pd.to_datetime(end_time).time())]

# 因为 Pandas 不理解时间字符串的比较。尝试使用 pd.to_datetime 将字符串转换为时间戳，并进行比较

# 删除相邻数据相差大于10的数据
df['Data1'] = df['Data1'].astype(float)  # 确保 Data1 列为浮点数
df = df[df['Data1'].diff().abs() <= 10]

# 按 'File_Name' 列分组，计算 Data1 的平均值和中位数，并按平均值从大到小排序
average_data1 = df.groupby('File_Name')['Data1'].transform('mean')
median_data1 = df.groupby('File_Name')['Data1'].transform('median')
df['Average_Data1'] = average_data1
df['Median_Data1'] = median_data1
df = df[(df['Average_Data1'] >= 5) & (df['Data1'] >= 10)]
df.sort_values(by='Average_Data1', ascending=False, inplace=True)

# 设置图表分辨率
dpi = 500 # 这里设置为 300 DPI，可以根据需要调整

# 绘制曲线图
fig, ax = plt.subplots(figsize=(50, 5), dpi=dpi)  # 设置图表大小和分辨率
max_values = []  # 用于存储每个折线的最大值

# 定义颜色列表
colors = [
    '#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#8B00FF',
    '#800000', '#FF4500', '#FFD700', '#008000', '#000080', '#483D8B', '#9932CC',
    '#8B0000', '#FFA500', '#FFD700', '#006400', '#00008B', '#6A5ACD'
]


for i, (label, group) in enumerate(df.groupby('File_Name')):
    group = group.sort_values(by='Time')  # 按时间排序
    
    x_values = group['Time']
    y_values = group['Data1']
    
    ax.plot(x_values, y_values, marker='o', markersize=1, label=f'{label} (Avg: {group["Average_Data1"].iloc[0]:.2f}, Median: {group["Median_Data1"].iloc[0]:.2f})', linewidth=0.5, color=colors[i % len(colors)])  # 使用曲线图，标记点为圆点
    
    # 标注最大值的点
    max_value_index = y_values.idxmax()
    max_value = y_values[max_value_index]
    max_time = x_values[max_value_index]
    
    # 调整标注的位置，使它们错开
    offset = i * 2.6  # 这里可以根据需要调整偏移量
    ax.annotate(label, xy=(max_time, max_value), xytext=(max_time, max_value + 10 + offset), arrowprops=dict(arrowstyle='->'))

    max_values.append((label, max_time, max_value))

# 设置 x 轴标签和标题
plt.xlabel('Time')
plt.ylabel('CPU%')
plt.title('ACU_Test_CPU%_List')

# 添加图例
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # 将图例移到右上角

# 保存图表为 PNG 文件
output_file = r'C:\Users\一清\Desktop\CPU_Test1110\line_chart.png'
plt.savefig(output_file, dpi=dpi, bbox_inches='tight')  # 使用 bbox_inches='tight' 确保保存整个图表


print(f'Line chart saved as {output_file}')
