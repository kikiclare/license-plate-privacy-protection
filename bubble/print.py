import numpy as np
import os
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import Multi_Gaussian as gauss


methods = ['PS(ws=4)', 'PS(ws=6)', 'VisualMixer', 'DP',
           'Mosaic', 'GAN', 'RGBLensLock', 'LensLock']

labels = {
    'PS(ws=4)': r'$PS_4$',
    'PS(ws=6)': r'$PS_6$',
    'VisualMixer': r'$VisualMixer$',
    'DP': r'$DP$',
    'Mosaic': r'$Mosaic$',
    'GAN': r'$GAN$',
    'RGBLensLock': r'$RGB\ LensLock$',
    'LensLock': r'$LensLock$'
}


colors = {
    'PS(ws=4)': '#4C78A8', 
    'PS(ws=6)': '#F58518',  
    'VisualMixer': '#E45756',  
    'DP': '#72B7B2',       
    'Mosaic': '#54A24B',   
    'GAN': '#EECA3B',       
    'RGBLensLock': '#B279A2',  
    'LensLock': '#FF9DA6'  
}

basePath = r'./fv292'

results = []
for method in methods:
    path = os.path.join(basePath, method)
    r = []
    with open(os.path.join(path, 'result.txt'), mode='r') as f:
        for line in f:
            mAP, L = map(float, line.split())
            r.append([mAP, L])
    r = np.asarray(r)
    results.append(r)


fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
label_offsets_x = {'PS(ws=6)': -0.04, 'VisualMixer': -0.0,'LensLock': 0.02,}  # 左移标签的偏移量
label_offsets_y = {'Mosaic':0.04,'GAN':0.06,'DP':0.06,'PS(ws=4)':-0.12,'PS(ws=6)':-0.04, 'RGBLensLock': 0.06, 'LensLock': 0.06,'VisualMixer': 0.06}  # 向上向下调整标签的偏移量
MUX = []
MUY = []

for i, result in enumerate(results):
    MU, SIGMA = gauss.multivariate_gaussian_fit(result)
    a, b, ang = gauss.get_Ellipse(SIGMA)
    ell_color = colors[methods[i]]
    ell_cubic = Ellipse(xy=MU, width=a * 0.6, height=b * 0.6, angle=ang, facecolor=ell_color, alpha=0.7)
    ax.add_patch(ell_cubic)
    MUX.append(MU[0])
    MUY.append(MU[1])


my_zorder = range(1, 17)
for i in range(len(methods)):
    plt.scatter([MUX[i]], [MUY[i]], c='white', marker='o', edgecolors='black', linewidths=1, zorder=my_zorder[i]*2+1, s=80)
    x_offset = label_offsets_x.get(methods[i], 0)
    y_offset = label_offsets_y.get(methods[i], 0)
    plt.text(MUX[i] + x_offset, MUY[i] + y_offset, labels[methods[i]], fontsize=26, ha='center', va='bottom', color='black', zorder=my_zorder[i]*2+2)

plt.xlabel('mAP', fontsize=34)
plt.ylabel(r'ED', fontsize=34)
ax.tick_params(axis='both', which='major', labelsize=28)
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.set_xlim(0.65, 1.05)  # Adjust the x-axis range
plt.ylim(None, 1)
plt.grid()
plt.tight_layout()
plt.savefig("./plot.png", format="png", dpi=300)
