#!/bin/bash

# 定义源图片文件夹路径和标签文件夹的基本路径
source_dir="/home/corgi/privacy_protection/evaluate/runs/detect/11.21/气泡/car_3840_2160_30fps"
labels_dir_base="/home/corgi/privacy_protection/evaluate/runs/detect/2.17/气泡/3840/RGBLensLock"

# 定义输出结果文件的存放路径
result_file="/home/corgi/privacy_protection/algorithm/气泡图map-ed/fv292/3840/RGBLensLock/result.txt"

# 创建结果文件的目录（如果不存在）
mkdir -p "$(dirname "$result_file")"
> "$result_file"  # 清空旧的结果文件

# 遍历源文件夹中的每个子文件夹（每张图片对应一个文件夹）
for img_folder in "${source_dir}"/*; do
    img_name=$(basename "$img_folder")
    real_label_path="${img_folder}/labels"
    detect_label_path="${labels_dir_base}/${img_name}/labels"

    # 检查标签文件夹是否存在
    if [[ -d "$real_label_path" && -d "$detect_label_path" ]]; then
        # 调用 calmAP.py 处理当前图片文件夹和其对应的两个标签文件夹
        output=$(python calmAP.py "$img_folder" "$real_label_path" "$detect_label_path")
        
        # 提取 mAP 值，并转换为小数形式
        map_value=$(echo "$output" | grep -oP 'mAP = \K[^\%]*' | awk '{printf "%.4f\n", $1/100}')
        
        # 直接将 mAP 值写入结果文件
        echo "$map_value" >> "$result_file"
    else
        # 如果标签文件夹缺失，则记录缺失信息
        echo "Missing labels for $img_name" >> "$result_file"
    fi
done

echo "Processing complete. Results stored in $result_file"