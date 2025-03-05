import os
import numpy as np
from PIL import Image
from segment_anything import sam_model_registry, SamPredictor
import torch
import cv2
original_image_path ='图片路径'
privacy_images = ['图片路径']
sam_checkpoint_path = "./StableSAM/sam_vit_b_01ec64.pth"
yolov7_weights_path = "./yolov7/yolov7.pt" 
yolov7_repo_path = "./yolov7"  

import sys
sys.path.append(yolov7_repo_path)
from models.experimental import attempt_load
from utils.general import non_max_suppression
from utils.torch_utils import select_device
def load_yolov7_model(weights_path, device):
    print("Loading YOLOv7 model...")
    model = attempt_load(weights_path, map_location=device)  
    model.eval()
    return model
def load_sam_model(checkpoint_path, device="cpu"):
    sam = sam_model_registry["vit_b"](checkpoint=checkpoint_path)
    sam.to(device)
    return SamPredictor(sam)

def detect_vehicles_yolov7(model, image_path, device, conf_thres=0.25, iou_thres=0.45):
    print("Running YOLOv7 detection...")
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    orig_height, orig_width = img.shape[:2]  
    img_resized = cv2.resize(img_rgb, (640, 640))  
    img_resized = img_resized.transpose(2, 0, 1) / 255.0  
    img_resized = torch.tensor(img_resized, dtype=torch.float32).unsqueeze(0).to(device)
    with torch.no_grad():
        preds = model(img_resized)[0]
    preds = non_max_suppression(preds, conf_thres, iou_thres)
    boxes = []
    for det in preds[0]:  
        cls = int(det[-1])  
        if cls in [2, 7]:  
            x_min, y_min, x_max, y_max = det[:4].cpu().numpy()
            scale_x = orig_width / 640
            scale_y = orig_height / 640
            x_min = int(x_min * scale_x)
            y_min = int(y_min * scale_y)
            x_max = int(x_max * scale_x)
            y_max = int(y_max * scale_y)
            boxes.append([x_min, y_min, x_max, y_max])
    return boxes

def segment_with_sam(image_path, boxes, sam_predictor):
    img = Image.open(image_path).convert("RGB")
    img_np = np.array(img)
    sam_predictor.set_image(img_np)
    combined_mask = np.zeros(img_np.shape[:2], dtype=np.bool_)
    for box in boxes:
        masks, _, _ = sam_predictor.predict(box=np.array(box), multimask_output=False)
        if masks is not None:
            combined_mask = np.logical_or(combined_mask, masks[0]) 
    return combined_mask

def calculate_iou(mask1, mask2):
    intersection = np.logical_and(mask1, mask2).sum()
    union = np.logical_or(mask1, mask2).sum()
    return intersection / union if union != 0 else 0

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    yolov7_model = load_yolov7_model(yolov7_weights_path, device)
    sam_predictor = load_sam_model(sam_checkpoint_path, device)
    original_boxes = detect_vehicles_yolov7(yolov7_model, original_image_path, device)
    original_mask = segment_with_sam(original_image_path, original_boxes, sam_predictor)
    results = {}
    for privacy_image_path in privacy_images:
        if not os.path.exists(privacy_image_path):
            continue
        privacy_boxes = detect_vehicles_yolov7(yolov7_model, privacy_image_path, device)
        privacy_mask = segment_with_sam(privacy_image_path, privacy_boxes, sam_predictor)
        iou = calculate_iou(original_mask, privacy_mask)
        results[os.path.basename(privacy_image_path)] = iou
        print(f"IoU for {privacy_image_path}: {iou:.4f}")

