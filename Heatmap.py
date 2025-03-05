import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def compute_vfe_block(block: np.ndarray, F: float = 1.0) -> float:
    if block.ndim != 3:
        raise ValueError("Input block must be a 3D array [H, W, C].")
    h, w, c = block.shape
    vfe_vals = []
    for ch in range(c):
        channel = block[:, :, ch].astype(np.float32)
        diff_x = (channel[:, 1:] - channel[:, :-1]) ** 2
        diff_y = (channel[1:, :] - channel[:-1, :]) ** 2
        vfe_vals.append(diff_x.sum() + diff_y.sum())
    vfe_raw = float(np.mean(vfe_vals))
    vfe_normalized = (vfe_raw / (h * w)) * F
    return vfe_normalized

def compute_vfe_map(image: np.ndarray, block_size: int = 16, F: float = 1.0) -> np.ndarray:
    h, w, c = image.shape
    grid_h = h // block_size
    grid_w = w // block_size
    vfe_map = np.zeros((grid_h, grid_w), dtype=np.float32)
    for i in range(grid_h):
        for j in range(grid_w):
            r0 = i * block_size
            c0 = j * block_size
            block = image[r0 : r0 + block_size, c0 : c0 + block_size, :]
            vfe_map[i, j] = compute_vfe_block(block, F=F)
    return vfe_map

def plot_vfe_heatmap(vfe_map: np.ndarray, block_size: int, save_dir: str, save_name: str):
    plt.rcParams.update({'font.size': 16})
    plt.figure(figsize=(12, 6))
    val_min = np.percentile(vfe_map, 5)
    val_max = np.percentile(vfe_map, 95)
    if val_min == val_max:
        val_min = 0
        val_max = np.max(vfe_map)
    heatmap = plt.imshow(vfe_map, cmap='coolwarm', origin='upper',
                         vmin=val_min, vmax=val_max)
    plt.xticks([])
    plt.yticks([])
    plt.title(f"VFE Heatmap (Block={block_size})", fontsize=18, pad=10)
    cbar = plt.colorbar(heatmap, fraction=0.046, pad=0.04)
    cbar.set_label("VFE Value", fontsize=16)
    tick_count = 5
    cbar_ticks = np.linspace(val_min, val_max, tick_count)
    cbar.set_ticks(cbar_ticks)
    cbar.ax.tick_params(labelsize=14)
    out_path = os.path.join(save_dir, save_name)
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Heatmap saved to: {out_path}")

def main():
    img_path = "输入图片路径"
    save_dir = "输出文件夹路径"
    save_name = "vfe_map_car_coolwarm.png"
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image not found: {img_path}")
    os.makedirs(save_dir, exist_ok=True)
    image_bgr = cv2.imread(img_path, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    BLOCK_SIZE = 16
    F_FACTOR = 1.0
    vfe_map = compute_vfe_map(image_rgb, block_size=BLOCK_SIZE, F=F_FACTOR)
    # print("vfe_map shape:", vfe_map.shape)
    plot_vfe_heatmap(vfe_map, BLOCK_SIZE, save_dir, save_name)
    avg_vfe = float(np.mean(vfe_map))
    # print(f"Average block-level VFE after scale (F={F_FACTOR}) = {avg_vfe:.2f}")

if __name__ == "__main__":
    main()
