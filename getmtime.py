import os
import datetime

# 指定要扫描的文件夹
folder_path = "sorted"

# 遍历文件夹中的所有文件
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)

    # 确保是文件，而不是文件夹
    if os.path.isfile(file_path):
        # 获取文件的修改时间（以秒为单位）
        mod_time = os.path.getmtime(file_path)

        # 转换为更精确的时间格式（支持微秒）
        mod_time_ns = os.stat(file_path).st_mtime_ns  # 纳秒级

        # 格式化输出
        print(
            f"{file_name} {datetime.datetime.fromtimestamp(mod_time).strftime('%M:%S.%f')}"
        )
        # print(f"  修改时间（纳秒级）: {mod_time_ns} 纳秒")
