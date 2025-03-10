


## 运行 YOLOv7 进行汽车目标检测

确保已下载并准备好 YOLOv7 模型和数据集。

### 命令格式：

```bash
python yolov7/detect.py --weights yolov7/yolov7.pt --source [数据集路径] --save-txt --save-conf --name [保存路径] --class 2
```

### 参数说明：

- **`--weights`**：指定模型权重文件路径 (如 `yolov7.pt`)。
- **`--source`**：指定输入数据集路径。
- **`--save-txt`**：保存检测结果到文本文件。
- **`--save-conf`**：保存每个检测目标的置信度。
- **`--name`**：指定检测结果的输出目录名称。
- **`--class`**：指定检测类别索引（如 `2` 代表汽车）。

---
## 计算mAP指标（Mean Average Precision）

### 命令格式：

```bash
cd mAP
python calmAP.py [检测结果路径] [真实标签路径] [预测标签路径]
```
**示例命令**：

```bash
cd mAP
python calmAP.py path/to/detection_results path/to/ground_truth_labels path/to/predicted_labels
```

**参数说明**：

- **`[检测结果路径]`**：指定模型检测结果所在的主目录路径。
- **`[真实标签路径]`**：指定真实目标标签（Ground Truth Labels）的目录路径。
- **`[预测标签路径]`**：指定模型预测标签（Predicted Labels）的目录路径。

---
## 运行 ED 脚本处理视频数据

### ① 运行 `run.sh` 脚本

**目的**：处理视频数据，输出结果到指定目录，并记录结果到 CSV 文件中。

**命令格式**：

```bash
./run.sh -i [输入目录] -o [输出目录] -c [输出CSV文件路径]
```

**示例命令**：

```bash
./run.sh -i /path/to/input/data -o /path/to/output -c /path/to/output/results.csv
```

**参数说明**：

- **`-i [输入目录]`**：指定要处理的视频数据所在目录。
- **`-o [输出目录]`**：指定结果输出目录。
- **`-c [输出CSV文件路径]`**：指定结果 CSV 文件保存路径。

---

### ② 运行 `test.sh` 脚本

**目的**：测试处理结果，涉及配置文件或密钥文件。

**命令格式**：

```bash
./test.sh -i [输入文件或目录] -o [输出目录] -c [输出CSV文件路径] -k [配置文件或密钥路径]
```

**示例命令**：

```bash
./test.sh -i /path/to/input/data -o /path/to/output -c /path/to/output/results.csv -k /path/to/config_or_key
```

**参数说明**：

- **`-i [输入文件或目录]`**：指定待测试的视频文件或数据目录路径。
- **`-o [输出目录]`**：指定测试结果输出目录。
- **`-c [输出CSV文件路径]`**：指定测试结果的 CSV 文件路径。
- **`-k [配置文件或密钥路径]`**：指定测试所需的配置文件或密钥文件路径。


### 输出结果：

```bash
python calDiff.py
```
---

# 方法

DP、psvfe直接改数据集路径运行即可。
GAN：[text](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)
Mosaic：[text](https://github.com/we0091234/yolov8-plate)
face:[text](https://github.com/hpc203/yolov8-face-landmarks-opencv-dnn)
灭点检测：[text](https://github.com/SymenYang/Vanish-Point-Detection)
