import Levenshtein
import difflib
import cv2
import sys


result  = './tmp/output/results.csv'
resultK = './tmp/output/resultsK.csv' 
imagePath = './tmp/input/k1'

R = open(result, 'r', encoding = 'utf-8')
K = open(resultK, 'r', encoding = 'utf-8')

RlpLines = R.readlines()
KlpLines = K.readlines()

averageL = [0, 0, 0, 0, 0]
averageD = [0, 0, 0, 0, 0]
count    = [0, 0, 0, 0, 0]

for i in range(len(RlpLines)):
    
    Rlps = RlpLines[i].split(",")
    Klps = KlpLines[i].split(",")
    Pid  = Rlps[0]
    # print("For image " + Pid + ":")
    # print('\t%-20s\t%-20s\t%-20s\t%-20s' % ('Rlp', 'Klp', 'Levenshtein', 'DifflibSMR'))
    # print('\t-------------------------------------------------------------------------------------------')

    for i in range(1, len(Rlps)):
        Rlp = Rlps[i].strip()
        Klp, KcarS = Klps[i].strip().split("_")
        KcarS = int(KcarS)
        IsizeW = cv2.imread(imagePath + '/' + Pid + ".jpg").shape[1]
        KcarS = KcarS / IsizeW
        
        if(Klp == 'NoLPrecognized'):
            Klp = ''
        if(Rlp == 'NoLPrecognized'):
            Rlp = ''

        lenRK = len(Rlp) + len(Klp)

        if(lenRK == 0):
            L = 0
        else:
            L = Levenshtein.distance(Rlp, Klp) / lenRK

        D = difflib.SequenceMatcher(a=Rlp, b=Klp).ratio()

        if KcarS > 0.2:
            averageL[4] += L
            averageD[4] += D
            count[4]    += 1
        elif KcarS > 0.15:
            averageL[3] += L
            averageD[3] += D
            count[3]    += 1
        elif KcarS > 0.1:
            averageL[2] += L
            averageD[2] += D
            count[2]    += 1
        elif KcarS > 0.05:
            averageL[1] += L
            averageD[1] += D
            count[1]    += 1
        else:
            averageL[0] += L
            averageD[0] += D
            count[0]    += 1

    #     print('%d\t%-20s\t%-20s\t%-20.2f\t%-20.2f' % (i, Rlp, Klp, L, D))

    # print()

# for i in range(5):
#     if count[i] <= 0:
#         averageL[i] = 0
#         averageD[i] = 0
#     else:
#         averageL[i] = averageL[i] / count[i]
#         averageD[i] = averageD[i] / count[i]

#     print('For pixels > %.2f:' % (i * 0.05))
#     print('\tAverageL: %.3f\tAverageD: %.3f' % (averageL[i], averageD[i]))
i = int(sys.argv[1])
if count[i] <= 0:
    averageL[i] = 0
    averageD[i] = 0
else:
    averageL[i] = averageL[i] / count[i]
    averageD[i] = averageD[i] / count[i]

with open('./tmp/output/privacy.txt', 'w') as f:
    f.write(str(averageL[i]))