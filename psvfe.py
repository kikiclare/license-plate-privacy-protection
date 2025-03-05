import cv2
import numpy as np
import os
import time  

def compute_vfe_block(block: np.ndarray, F: float = 1.0) -> float:
    h, w, c = block.shape
    vfe_vals = []
    for ch in range(c):
        channel = block[:, :, ch].astype(np.float32)
        diff_x = (channel[:, 1:] - channel[:, :-1]) ** 2
        diff_y = (channel[1:, :] - channel[:-1, :]) ** 2
        vfe_vals.append(diff_x.sum() + diff_y.sum())
    return (np.mean(vfe_vals) / (h * w)) * F

def compute_vfe_map(image: np.ndarray, block_size: int = 4, F: float = 1.0) -> np.ndarray:
    h, w = image.shape[:2]
    return np.array([[compute_vfe_block(image[i*block_size:(i+1)*block_size, 
                                           j*block_size:(j+1)*block_size], F)
                     for j in range(w//block_size)] 
                    for i in range(h//block_size)])

def shuffle_block(block: np.ndarray, window_size: int) -> np.ndarray:
    h, w, c = block.shape
    sub_blocks = [block[i*window_size:(i+1)*window_size, 
                        j*window_size:(j+1)*window_size] 
                 for i in range(h//window_size) 
                 for j in range(w//window_size)]
    np.random.shuffle(sub_blocks)
    return np.vstack([np.hstack(sub_blocks[i* (w//window_size): (i+1)*(w//window_size)]) 
                     for i in range(h//window_size)])

def process_image(img_path: str, output_dir: str, block_size: int = 4):
    start_time = time.time()  
    image = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
    h, w = image.shape[:2]
    vfe_map = compute_vfe_map(image, block_size)
    avg_vfe = np.mean(vfe_map)
    processed = np.zeros_like(image)
    for i in range(vfe_map.shape[0]):
        for j in range(vfe_map.shape[1]):
            y = i * block_size
            x = j * block_size
            block = image[y:y+block_size, x:x+block_size]
            ws = 2 if vfe_map[i, j] > avg_vfe else 4
            processed[y:y+block_size, x:x+block_size] = shuffle_block(block, ws)
    output_path = os.path.join(output_dir, os.path.basename(img_path))
    cv2.imwrite(output_path, cv2.cvtColor(processed, cv2.COLOR_RGB2BGR))
    elapsed_time = time.time() - start_time 
    print(f"Processed {os.path.basename(img_path)} in {elapsed_time:.2f} seconds.")

def batch_processing(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            process_image(os.path.join(input_dir, filename), output_dir)

if __name__ == "__main__":
    input_dir = "输入文件夹路径"
    output_dir = "输出文件夹路径"
    batch_processing(input_dir, output_dir)
