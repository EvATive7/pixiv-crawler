import os
from datetime import datetime

import natsort


def check_sort_order(directory):
    # 获取文件夹中的所有文件
    files = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".png"):
            # 获取文件的修改时间
            mod_time = os.path.getmtime(file_path)
            files.append((filename, mod_time))

    # 按文件名进行自然排序
    files_by_name = natsort.natsorted(files, key=lambda x: x[0])

    # 按修改时间排序
    files_by_time = sorted(files, key=lambda x: x[1])

    same_order = True
    for i in range(len(files_by_name)):
        print(f"{i}: {files_by_name[i][0]} - {files_by_time[i][0]}")
        if files_by_name[i][0] != files_by_time[i][0]:
            same_order = False

    if same_order:
        print("\n文件名排序和修改时间排序结果相同。")
    else:
        print("\n文件名排序和修改时间排序结果不同。")


# 示例调用
directory = ".sorted"  # 替换成你实际的文件夹路径
check_sort_order(directory)
