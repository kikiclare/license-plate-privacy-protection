import os
import torch
import lpips
from PIL import Image
from torchvision import transforms
lpips_model = lpips.LPIPS(net='alex')  
preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def load_image(image_path):
    image = Image.open(image_path).convert('RGB')
    return preprocess(image).unsqueeze(0)

def calculate_lpips(img1, img2):
    with torch.no_grad():
        return lpips_model(img1, img2).item()

original_dir = '文件夹路径'
privacy_dir = '文件夹路径'
original_images = sorted(os.listdir(original_dir))
privacy_images = sorted(os.listdir(privacy_dir))
lpips_scores = []
for orig_img, priv_img in zip(original_images, privacy_images):
    orig_path = os.path.join(original_dir, orig_img)
    priv_path = os.path.join(privacy_dir, priv_img)
    img1 = load_image(orig_path)
    img2 = load_image(priv_path)
    lpips_score = calculate_lpips(img1, img2)
    lpips_scores.append(lpips_score)
average_lpips = sum(lpips_scores) / len(lpips_scores)
print(f'Average LPIPS: {average_lpips}')

