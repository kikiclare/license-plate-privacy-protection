import cv2
import numpy as np
from numba import njit, prange
from pathlib import Path
import time

def get_window_size(height):
    if 0 <= height < 10:
        return 1
    elif 10 <= height < 20:
        return 2
    elif 20 <= height < 30:
        return 3
    elif 30 <= height < 40:
        return 4
    elif 40 <= height < 50:
        return 5
    elif 50 <= height < 60:
        return 6
    elif 60 <= height < 70:
        return 7
    elif 70 <= height < 80:
        return 8
    elif 80 <= height < 90:
        return 9
    else:
        return 0  

@njit(parallel=True)
def shuffle_pixels(image, start_y, end_y, window_size, width, channels):
    for i in range(start_y, end_y, window_size): 
        for j in range(0, width, window_size):   
            window_height = min(window_size, end_y - i)
            window_width = min(window_size, width - j)
            window = image[i:i+window_height, j:j+window_width].copy().reshape(-1, channels)
            np.random.shuffle(window)
            image[i:i+window_height, j:j+window_width] = window.reshape(window_height, window_width, channels)

def visual_mixer(image, zones, heights):
    height, width, channels = image.shape
    mixed_image = np.ascontiguousarray(image.copy()) 
    for idx, zone in enumerate(zones):
        window_size = get_window_size(heights[idx])
        start_y = height - zone[1]
        end_y = height - zone[0]
        if window_size == 0:
            print(f"Skipping zone {zone} with height {heights[idx]} due to zero window size.")
            continue
        shuffle_pixels(mixed_image, start_y, end_y, window_size, width, channels)
    return mixed_image

def process_images(input_dir, output_dir, zones, heights):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    for image_file in input_path.iterdir():
        if image_file.is_file() and image_file.suffix in ['.jpg', '.png', '.jpeg']:
            img = cv2.imread(str(image_file))
            if img is not None:
                start_time = time.time()
                mixed_image = visual_mixer(img, zones, heights)
                elapsed_time = time.time() - start_time
                output_file_path = output_path / image_file.name
                cv2.imwrite(str(output_file_path), mixed_image)
                print(f"Processed {image_file.name} in {elapsed_time:.2f} seconds, saved to {output_file_path}")


if __name__ == '__main__':
    input_dir = '输入文件夹路径'
    output_dir = '输出文件夹路径'
    zones = [] # 切分条带区域
    heights = [] #对应车牌宽度
    process_images(input_dir, output_dir, zones, heights)