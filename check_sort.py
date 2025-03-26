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

    # 输出排序后的文件名
    print("按文件名排序:")
    for file in files_by_name:
        print(file[0])

    print("\n按修改时间排序:")
    for file in files_by_time:
        print(file[0])

    # 检查两个排序结果是否相同
    same_order = [file[0] for file in files_by_name] == [
        file[0] for file in files_by_time
    ]

    if same_order:
        print("\n文件名排序和修改时间排序结果相同。")
    else:
        print("\n文件名排序和修改时间排序结果不同。")


# 示例调用
directory = ".sorted"  # 替换成你实际的文件夹路径
check_sort_order(directory)
