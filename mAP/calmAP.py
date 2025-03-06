import os
import sys
import shutil  

from diff import diff
from get_DR import get_DR
from get_GT import get_GT

image_path = sys.argv[1] # 原始图片路径
real_label_path = sys.argv[2] # 真值标签路径
detect_label_path = sys.argv[3] # 检测标签路径

if os.path.exists('GT'):
    shutil.rmtree('GT') 
    print("已重置GT")
if os.path.exists('DR'):
    shutil.rmtree('DR') 
    print("已重置DR")

diff(real_label_path, detect_label_path)
print("-------------get_GTing----------------")
get_GT(image_path, real_label_path)
print("-------------get_DRing----------------")
get_DR(image_path, detect_label_path)
print("-------------get_MAPing----------------")
os.system("python get_map.py -na --source " + image_path)

# k = image_path.split('\\')[-1]

# for i in ['p0', 'p100', 'p200', 'p300', 'p400', 'p600']:

#     if os.path.exists('GT'):
#         shutil.rmtree('GT') 
#         print("已重置GT")
#     if os.path.exists('DR'):
#         shutil.rmtree('DR') 
#         print("已重置DR")

#     real_label_path2 = os.path.join(real_label_path, i)
#     detect_label_path2 = os.path.join(detect_label_path, i)

    # diff(real_label_path2, detect_label_path2)
    # get_GT(image_path, real_label_path2)
    # get_DR(image_path, detect_label_path2)
#     os.system("python get_map.py --source " + image_path + ' --mapto E:/projects/4Ktraffic/lp93/mAP/' + k + i + '.png')
