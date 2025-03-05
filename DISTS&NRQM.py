import os
import torch
import pyiqa
from PIL import Image
import torchvision.transforms as transforms
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
def preprocess_image(image_path, resize_dim=(1024, 1024)):
    image = Image.open(image_path).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize(resize_dim), 
        transforms.ToTensor(),
    ])
    return transform(image).unsqueeze(0).to(device, dtype=torch.float16)  

def calculate_dists(reference_image, distorted_image, dists_weights_path):
    dists_metric = pyiqa.create_metric('dists', pretrained_model_path=dists_weights_path).to(device).half()  # 使用半精度
    with torch.no_grad():
        score = dists_metric(reference_image, distorted_image)
    return score.item()

def calculate_nrqm(image, nrqm_weights_path):
    nrqm_metric = pyiqa.create_metric('nrqm', pretrained_model_path=nrqm_weights_path).to(device).half()  # 使用半精度
    with torch.no_grad():
        score = nrqm_metric(image)
    return score.item()

dists_weights_path = './DISTS_weights-f5e65c96.pth'
nrqm_weights_path = './NRQM_model.mat'
original_dir = '文件夹路径'
processed_dir = '文件夹路径'
original_images = sorted([f for f in os.listdir(original_dir) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp'))])
processed_images = sorted([f for f in os.listdir(processed_dir) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp'))])
dists_scores = []
nrqm_scores = []
for orig_img, proc_img in zip(original_images, processed_images):
    orig_path = os.path.join(original_dir, orig_img)
    proc_path = os.path.join(processed_dir, proc_img)
    orig_image = preprocess_image(orig_path)
    proc_image = preprocess_image(proc_path)
    dists_score = calculate_dists(orig_image, proc_image, dists_weights_path)
    dists_scores.append(dists_score)
    nrqm_score = calculate_nrqm(proc_image, nrqm_weights_path)
    nrqm_scores.append(nrqm_score)
    print(f'图像: {proc_img} - DISTS: {dists_score:.4f}, NRQM: {nrqm_score:.4f}')
    torch.cuda.empty_cache()  
average_dists = sum(dists_scores) / len(dists_scores)
average_nrqm = sum(nrqm_scores) / len(nrqm_scores)
print(f'平均 DISTS 分数: {average_dists:.4f}')
print(f'平均 NRQM 分数: {average_nrqm:.4f}')
