import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# 读取 Excel 文件
excel_file = r'C:\Users\一清\Desktop\CPU_Test1110\1124测试数据\processed_data_test.xlsx'
df = pd.read_excel(excel_file)

# 删除包含 NaN 值的行
df.dropna(subset=['Time', 'CPU%', 'File_Name'], inplace=True)

# 过滤掉时间以10开头的数据
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')

start_time = '16:50:00'
end_time = '17:20:00'

df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')

df = df[(df['Time'].dt.time >= pd.to_datetime(start_time).time()) & 
        (df['Time'].dt.time <= pd.to_datetime(end_time).time())]

#处理数据
# 删除相邻数据相差大于10的数据
df['CPU%'] = df['CPU%'].astype(float)  # 确保 CPU% 列为浮点数
df = df[df['CPU%'].diff().abs() <= 10]

# 计算每个 'File_Name' 分组中的 'CPU%' 列的最大值
max_cpu_per_file = df.groupby('File_Name')['CPU%'].max()

# 选择所有 'File_Name' 分组中 'CPU%' 列最大值小于 10 的 'File_Name'
file_names_to_remove = max_cpu_per_file[max_cpu_per_file < 10].index

# 根据 'File_Name' 列的值，保留那些不在 file_names_to_remove 中的行
df = df[~df['File_Name'].isin(file_names_to_remove)]


# 按 'File_Name' 列分组，计算 CPU% 的平均值和中位数，并按平均值从大到小排序
average_cpu = df.groupby('File_Name')['CPU%'].transform('mean')
median_cpu = df.groupby('File_Name')['CPU%'].transform('median')
variance_cpu = df.groupby('File_Name')['CPU%'].transform('var')
df['Average_CPU'] = average_cpu
df['Median_CPU'] = median_cpu
df['Variance_CPU'] = variance_cpu

# 将 'sum' 数据的 CPU% 除以十cl
df.loc[df['File_Name'] == 'sum', 'CPU%'] /= 10
df.loc[df['File_Name'] == 'load_average', 'CPU%'] *= 5

df = df[(df['Average_CPU'] >= 1)]  # 根据实际情况调整筛选条件
df.sort_values(by='Average_CPU', ascending=False, inplace=True)

# 设置图表分辨率
dpi = 500  # 这里设置为 300 DPI，可以根据需要调整

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
    y_values = group['CPU%']
    
    if label == 'sum':
        ax.plot(x_values, y_values, marker='o', markersize=1, label=f'{label} (Avg: {group["Average_CPU"].iloc[0]:.2f}, Median: {group["Median_CPU"].iloc[0]:.2f}), Variance: {group["Variance_CPU"].iloc[0]:.2f})', linewidth=1.5, color=colors[i % len(colors)])
    elif label == 'load_average':
        ax.plot(x_values, y_values , marker='o', markersize=1, label=f'{label} (Avg: {group["Average_CPU"].iloc[0]:.2f}, Median: {group["Median_CPU"].iloc[0]:.2f}), Variance: {group["Variance_CPU"].iloc[0]:.2f})', linewidth=2, color=colors[i % len(colors)])
    else:
        ax.plot(x_values, y_values, marker='o', markersize=1, label=f'{label} (Avg: {group["Average_CPU"].iloc[0]:.2f}, Median: {group["Median_CPU"].iloc[0]:.2f}), Variance: {group["Variance_CPU"].iloc[0]:.2f})', linewidth=0.5, color=colors[i % len(colors)])  # 使用曲线图，标记点为圆点
    
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
output_file = r'C:\Users\一清\Desktop\CPU_Test1110\1125测试数据\test1125_1.png'
plt.savefig(output_file, dpi=dpi, bbox_inches='tight')  # 使用 bbox_inches='tight' 确保保存整个图表

print(f'Line chart saved as {output_file}')


# 绘制最大方差的图像
# 定义日期变量
date_variable = '1125'  # 你可以设置成你希望的日期



# 找到方差最大的File_Name，绘制曲线图，并保存文件
# 获取方差最大的十个 File_Name，排除 'sum' 和 'load_average'
non_special_file_names = df['File_Name'].unique()[~np.isin(df['File_Name'].unique(), ['sum', 'load_average'])]
max_variance_file_names_top10 = (
    df[df['File_Name'].isin(non_special_file_names)]
    .groupby('File_Name')['Variance_CPU']
    .nlargest(10)
    .reset_index(level=0)
    .sort_values(by='Variance_CPU', ascending=False)
    ['File_Name']
    .unique()
)

# 打印结果
print(max_variance_file_names_top10[:10])

for File_Name in max_variance_file_names_top10[:10]:
    # 提取方差最大的 File_Name 对应的数据
    tmp = df[df['File_Name'] == File_Name]

    # 设置图表分辨率
    dpi = 300  # 这里设置为 300 DPI，可以根据需要调整

    # 绘制曲线图
    fig, ax = plt.subplots(figsize=(50, 5), dpi=dpi)  # 设置图表大小和分辨率

    # 绘制 'sum' 数据的 CPU%
    df = df.sort_values(by='Time')
    ax.plot(df[df['File_Name'] == 'sum']['Time'], df[df['File_Name'] == 'sum']['CPU%'], marker='o', markersize=1, label=f'sum (Avg: {df[df["File_Name"] == "sum"]["Average_CPU"].iloc[0]:.2f}, Median: {df[df["File_Name"] == "sum"]["Median_CPU"].iloc[0]:.2f}, Variance: {df[df["File_Name"] == "sum"]["Variance_CPU"].iloc[0]:.2f})', linewidth=1.5, color=colors[1])

    # 绘制 'load_average' 数据的 CPU%
    df = df.sort_values(by='Time')
    ax.plot(df[df['File_Name'] == 'load_average']['Time'], df[df['File_Name'] == 'load_average']['CPU%'], marker='o', markersize=1, label=f'load_average (Avg: {df[df["File_Name"] == "load_average"]["Average_CPU"].iloc[0]:.2f}, Median: {df[df["File_Name"] == "load_average"]["Median_CPU"].iloc[0]:.2f}, Variance: {df[df["File_Name"] == "load_average"]["Variance_CPU"].iloc[0]:.2f})', linewidth=1.5, color=colors[2])

    # 绘制方差最大的 File_Name 数据
    tmp = tmp.sort_values(by='Time')
    ax.plot(
        tmp['Time'],
        tmp['CPU%'],
        marker='o',
        markersize=1,
        label=f'{File_Name} (Avg: {tmp["Average_CPU"].iloc[0]:.2f}, Median: {tmp["Median_CPU"].iloc[0]:.2f}, Variance: {tmp["Variance_CPU"].iloc[0]:.2f})',
        linewidth=1.5,
        color=colors[0]
    )

    # 设置 x 轴标签和标题
    plt.xlabel('Time')
    plt.ylabel('CPU%')
    plt.title(f'ACU_Test_CPU%_List ({date_variable}) - {File_Name}')

    # 添加图例
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    # 生成文件名，使用给定的日期变量和 File_Name
    output_file = rf'C:\Users\一清\Desktop\CPU_Test1110\1125测试数据\{date_variable}_{File_Name}.png'
    plt.savefig(output_file, dpi=dpi, bbox_inches='tight')  # 使用 bbox_inches='tight' 确保保存整个图表

    print(f'Line chart saved as {output_file}')

#手搓堆叠面积图！！！




# 假设您有一个包含File_Name、Time和CPU%的DataFrame，命名为df
# 假设您已经获得了前十大方差的File_Name列表，命名为max_variance_file_names_top10


# 创建一个 DataFrame 用于保存 CPU% 数据
result_df = pd.DataFrame({'Time': df['Time']})

# 将每个 File_Name 的 CPU% 数据添加到 DataFrame
for file_name in max_variance_file_names_top10:
    subset = df[df['File_Name'] == file_name]
    result_df[file_name] = subset['CPU%'].values

# 保存结果到 Excel 文件
output_file = r'C:\Users\一清\Desktop\CPU_Test1110\1125测试数据\output.xlsx'
result_df.to_excel(output_file, index=False)
print(f'Data saved as {output_file}')