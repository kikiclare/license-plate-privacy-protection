import os
import cv2
import numpy as np
import time

def add_laplace_noise_to_image(image, epsilon, sensitivity):
    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale, size=image.shape)
    noisy_image = image.astype(np.float32) + noise
    noisy_image = np.clip(noisy_image, 0, 255)  
    return noisy_image.astype(np.uint8)

def process_images_in_folder(folder_path, output_folder_path, epsilon, sensitivity):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)
                start_time = time.time()
                noisy_image = add_laplace_noise_to_image(image, epsilon, sensitivity)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"处理 {file} 用时 {elapsed_time:.2f} 秒")
                relative_path = os.path.relpath(root, folder_path)
                output_directory = os.path.join(output_folder_path, relative_path)
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                
                output_image_path = os.path.join(output_directory, file)
                cv2.imwrite(output_image_path, noisy_image)

def main(input_folder_path, output_folder_path):
    epsilon = 0.8 
    sensitivity = 150  
    process_images_in_folder(input_folder_path, output_folder_path, epsilon, sensitivity)
    print(f"Processed images with privacy protection are saved in {output_folder_path}.")

if __name__ == "__main__":
    input_folder_path = "输入文件夹路径" 
    output_folder_path = "输出文件夹的名字" 
    main(input_folder_path, output_folder_path)