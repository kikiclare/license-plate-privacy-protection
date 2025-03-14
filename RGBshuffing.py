import os
import cv2
import numpy as np

input_dir = '输入文件夹路径'
output_dir = '输出文件夹路径'
os.makedirs(output_dir, exist_ok=True)
fixed_channel_order = [2, 0, 1] 
for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image = cv2.imread(file_path)
        
        if image is not None:
            image_reordered = image[:, :, fixed_channel_order]
            output_path = os.path.join(output_dir, filename)
            cv2.imwrite(output_path, image_reordered)
            print(f"处理并保存文件: {filename}")
        else:
            print(f"无法读取文件: {filename}")
