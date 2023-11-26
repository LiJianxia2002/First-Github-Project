import pandas as pd

file_path = r'D:\lijianxia\project\ACU_CPU\sys_monitor_log20231026\load_average.txt'
data = []

try:
    with open(file_path, 'r') as file:
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
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred: {str(e)}")

df = pd.DataFrame(data)
excel_file = r'D:\lijianxia\project\ACU_CPU\10.16CPU测试尝试\1026test.xlsx'
df.to_excel(excel_file, index=False)

print("Data written to Excel file:", excel_file)

