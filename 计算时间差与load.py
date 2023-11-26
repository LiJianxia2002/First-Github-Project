import pandas as pd

# 从 Excel 文件中读取数据
df = pd.read_excel(r"C:\Users\一清\Desktop\CPU_Test1110\1124测试数据\tmp.xlsx")

# 如果存在 "hesai_lidar_nod" 的文件名，按照 "PID" 进行分组并保持原始顺序
if 'hesai_lidar_nod' in df['File_Name'].unique():
    nod_grouped = df[df['File_Name'] == 'hesai_lidar_nod'].groupby('PID', sort=False)

    # 遍历分组，给 "hesai_lidar_nod" 的分组分配序号
    for i, (_, group) in enumerate(nod_grouped, start=1):
        df.loc[group.index, 'File_Name'] = f'hesai_lidar_nod{i}'

# 删除 "File_Name" 为 "localization" 且其 "PID" 值在 "File_Name" 为 "localization_sw" 的行的 "PID" 列中的行
df = df[~((df['File_Name'] == 'localization') & df['PID'].isin(df[df['File_Name'] == 'localization_sw']['PID']))]

# 将 Time 和 TIME+ 列转换为 datetime 类型
df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S.%f", errors='coerce')

# 分隔 TIME+ 列，将其变成分钟和秒
df[['TIME_minute', 'TIME_second']] = df['TIME+'].str.split(':', expand=True)

# 将分和秒转为数字
df['TIME_minute'] = pd.to_numeric(df['TIME_minute'], errors='coerce')
df['TIME_second'] = pd.to_numeric(df['TIME_second'], errors='coerce')

# 将时间转为秒
df['TIME_seconds'] = df['TIME_minute'] * 60 + df['TIME_second']

# 保留三位小数
df['Time_seconds'] = df['Time'].dt.hour * 3600 + df['Time'].dt.minute * 60 + df['Time'].dt.second + df['Time'].dt.microsecond / 1e6
df['Time_seconds'] = df['Time_seconds'].round(3)

# 根据不同的 "File_Name" 内容进行分类，使用 shift(-1) 计算 CPU%
df['CPU%'] = df.groupby('File_Name')['TIME_seconds'].diff(-1) / df.groupby('File_Name')['Time_seconds'].diff(-1).shift(1)
df['CPU%'] = (df['CPU%'] * 100).round(1)  # 将结果乘以 100

# 格式化 Time 列，保留时分秒
df['Time'] = df['Time'].dt.strftime('%H:%M:%S')

# 计算每个时间点的数据总和
sum_data = df.groupby('Time')['CPU%'].sum().reset_index()
sum_data['File_Name'] = 'sum'

# 将总和数据追加到原数据的末尾
df = pd.concat([df, sum_data], ignore_index=True)

# 将处理后的数据保存到新的 Excel 文件
output_file_path = r"C:\Users\一清\Desktop\CPU_Test1110\1124测试数据\processed_data_test.xlsx"
df.to_excel(output_file_path, index=False)

print("前半部分数据处理完成，并已保存到:", output_file_path)

# 以下是新增的功能

# 定义处理 txt 文件的函数
def process_txt(txt_file, selected_data, excel_file_path):
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
        print(f"Error: File not found - {txt_file}")
        return
    except Exception as e:
        print(f"Error processing file {txt_file}: {e}")
        return

    # Create a DataFrame from the processed data
    df_txt = pd.DataFrame(data)

    # Select the specified data column
    selected_column = f"data{selected_data}"
    df_txt['File_Name'] = 'load_average'
    df_txt['Time'] = pd.to_datetime(df_txt['time']).dt.strftime('%H:%M:%S')
    df_txt['CPU%'] = df_txt[selected_column]
    df_txt = df_txt[['File_Name', 'Time', 'CPU%']]

    # Append the processed txt data to the original Excel DataFrame
    df_combined = pd.concat([df, df_txt], ignore_index=True)

    # Save the combined DataFrame to the original Excel file
    df_combined.to_excel(excel_file_path, index=False)

# 选择要处理的 data 列
selected_data = 1  # 选择 data1，可以修改为 2 或 3
process_txt(r"C:\Users\一清\Desktop\CPU_Test1110\原始数据\sys_monitor_log20231124\load_average.txt", selected_data, output_file_path)

print("处理后的 txt 数据已追加到:", output_file_path)
