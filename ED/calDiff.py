import Levenshtein
import difflib


result  = './tmp/output/results.csv'
resultK = './tmp/output/resultsK.csv' 

R = open(result, 'r', encoding = 'utf-8')
K = open(resultK, 'r', encoding = 'utf-8')

RlpLines = R.readlines()
KlpLines = K.readlines()

averageL = 0
averageD = 0
count    = 0

for i in range(len(RlpLines)):
    
    Rlps = RlpLines[i].split(",")
    Klps = KlpLines[i].split(",")
    Pid  = Rlps[0]
    #print("For image " + Pid + ":")
    #print('\t%-20s\t%-20s\t%-20s\t%-20s' % ('Rlp', 'Klp', 'Levenshtein', 'DifflibSMR'))
    #print('\t-------------------------------------------------------------------------------------------')

    for i in range(1, len(Rlps)):
        Rlp = Rlps[i].strip()
        Klp = Klps[i].strip().split('_')[0] # Klps[i].strip().coco-vae气泡图数据集('_')[1]是像素宽度
        
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

        averageL += L
        averageD += D
        count    += 1

        #print('%d\t%-20s\t%-20s\t%-20.2f\t%-20.2f' % (i, Rlp, Klp, L, D))

    #print()

averageL = averageL / count
averageD = averageD / count

result = 'AverageL: %.3f\tAverageD: %.3f' % (averageL, averageD)

print(result)

with open('./tmp/output/privacy.txt', 'w') as f:
    f.write(result)