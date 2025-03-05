import os
import cv2
import numpy as np
from PIL import Image
from segment_anything import sam_model_registry, SamPredictor
import torch
image_path ='输入图片路径'
output_path = '输出图片路径'
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
    print("Loading SAM model...")
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

def segment_vehicles_sam(image_path, boxes, sam_predictor, output_path, alpha=0.8):
    img = Image.open(image_path).convert("RGB")
    img_np = np.array(img)
    sam_predictor.set_image(img_np)
    segmented_image = img_np.copy()
    overlay = np.zeros_like(segmented_image) 

    for box in boxes:
        x_min, y_min, x_max, y_max = box
        masks, _, _ = sam_predictor.predict(box=np.array([x_min, y_min, x_max, y_max]), multimask_output=False)
        if masks is not None:
            mask = masks[0]
            overlay[mask] = [255, 105, 180]  
    segmented_image = cv2.addWeighted(overlay, alpha, segmented_image, 1 - alpha, 0)
    cv2.imwrite(output_path, cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR))
    print(f"Segmented image saved to: {output_path}")

if __name__ == "__main__":
    device = select_device("cpu")
    yolov7_model = load_yolov7_model(yolov7_weights_path, device)
    sam_predictor = load_sam_model(sam_checkpoint_path, device)
    vehicle_boxes = detect_vehicles_yolov7(yolov7_model, image_path, device)
    segment_vehicles_sam(image_path, vehicle_boxes, sam_predictor, output_path, alpha=0.5)
