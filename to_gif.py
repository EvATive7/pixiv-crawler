from PIL import Image
import hashlib
import os
from concurrent.futures import ThreadPoolExecutor

def md5(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()

def detect_format(file_path: str) -> str:
    try:
        with Image.open(file_path) as img:
            format_map = {
                "JPEG": "Jpeg",
                "PNG": "Png",
                "BMP": "Bmp",
                "GIF": "Gif",
                "WEBP": "WebP",
            }
            return format_map.get(img.format, "Unknown")
    except Exception:
        return "Unknown"

def get_image_size(file_path: str) -> tuple[int, int]:
    try:
        with Image.open(file_path) as img:
            return img.width, img.height
    except Exception:
        return 0, 0

def any2gif(file_path: str, save_path: str, force_size: int = 0) -> bool:
    try:
        with Image.open(file_path) as img:
            max_dim = max(img.width, img.height)
            if force_size > 0 and max_dim != force_size:
                scale = force_size / max_dim
                new_size = (int(img.width * scale), int(img.height * scale))
                img = img.resize(new_size, Image.LANCZOS)
            img.save(save_path, format="GIF")
        return True
    except Exception:
        return False

def any2gif2(file_path: str, save_path: str, force_size: int = 0) -> bool:
    return any2gif(file_path, save_path, force_size)

def batch_convert_png_to_gif(source_folder: str, target_folder: str, force_size: int = 0):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    png_files = [f for f in os.listdir(source_folder) if f.lower().endswith(".png")]
    
    with ThreadPoolExecutor() as executor:
        for png_file in png_files:
            source_path = os.path.join(source_folder, png_file)
            target_path = os.path.join(target_folder, os.path.splitext(png_file)[0] + ".gif")
            executor.submit(any2gif, source_path, target_path, force_size)

# Example usage
if __name__ == "__main__":
    batch_convert_png_to_gif(".ready", ".gifed", 200)
