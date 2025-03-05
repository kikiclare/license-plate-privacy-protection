import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from concurrent.futures import ProcessPoolExecutor

original_folder = '文件夹路径'
processed_folder = '文件夹路径'

image_names = os.listdir(original_folder)
def process_image(image_name):
    original_path = os.path.join(original_folder, image_name)
    processed_path = os.path.join(processed_folder, image_name)
    original_image = cv2.imread(original_path)
    processed_image = cv2.imread(processed_path)
    if original_image.shape != processed_image.shape:
        print(f"图像尺寸不匹配：{image_name}")
        return None
    mse = np.mean((original_image - processed_image) ** 2)
    if mse == 0:
        current_psnr = float('inf')
    else:
        PIXEL_MAX = 255.0
        current_psnr = 20 * np.log10(PIXEL_MAX / np.sqrt(mse))
    image_height, image_width = original_image.shape[:2]
    min_dim = min(image_height, image_width)
    win_size = min(7, min_dim)
    if win_size % 2 == 0:
        win_size -= 1
    if win_size < 3:
        win_size = 3  
    current_ssim = ssim(
        original_image,
        processed_image,
        channel_axis=-1,
        win_size=win_size,
        data_range=processed_image.max() - processed_image.min()
    )

    print(f"{image_name} - PSNR: {current_psnr:.2f}, SSIM: {current_ssim:.4f}")

    return current_psnr, current_ssim

with ProcessPoolExecutor() as executor:
    results = list(executor.map(process_image, image_names))
results = [result for result in results if result is not None]
psnr_values = [result[0] for result in results]
ssim_values = [result[1] for result in results]
average_psnr = np.mean(psnr_values)
average_ssim = np.mean(ssim_values)
print(f"\n平均PSNR: {average_psnr:.2f}")
print(f"平均SSIM: {average_ssim:.4f}")