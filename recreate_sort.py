import time
from pathlib import Path

from natsort import natsorted


def modify_exif_in_folder(ori_folder_path, dst_folder_path):
    ori_folder_path = Path(ori_folder_path)
    files = natsorted(
        [
            f
            for f in ori_folder_path.iterdir()
            if f.is_file() and f.name.lower().endswith(".png")
        ]
    )

    for _, file in enumerate(files):
        bin_data = file.read_bytes()
        dst_folder_path = Path(dst_folder_path)
        dst_folder_path.mkdir(exist_ok=True)
        (dst_folder_path / file.name).write_bytes(bin_data)

        time.sleep(0.01)
        print(f"{file} recreated")


folder_path = "./.origin"  # 修改为你的文件夹路径
dst_folder_path = "./.sorted"  # 修改为你的文件夹路径
modify_exif_in_folder(folder_path, dst_folder_path)
