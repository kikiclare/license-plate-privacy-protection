import Levenshtein
import difflib


result  = './tmp/output/results.csv'
resultK = './tmp/output/resultsK.csv' 

R = open(result, 'r', encoding = 'utf-8')
K = open(resultK, 'r', encoding = 'utf-8')

RlpLines = R.readlines()
KlpLines = K.readlines()

averageL = [0, 0, 0, 0, 0, 0]
averageD = [0, 0, 0, 0, 0, 0]
count    = [0, 0, 0, 0, 0, 0]

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

        if KcarS > 600:
            averageL[5] += L
            averageD[5] += D
            count[5]    += 1
        elif KcarS > 400:
            averageL[4] += L
            averageD[4] += D
            count[4]    += 1
        elif KcarS > 300:
            averageL[3] += L
            averageD[3] += D
            count[3]    += 1
        elif KcarS > 200:
            averageL[2] += L
            averageD[2] += D
            count[2]    += 1
        elif KcarS > 100:
            averageL[1] += L
            averageD[1] += D
            count[1]    += 1
        else:
            averageL[0] += L
            averageD[0] += D
            count[0]    += 1

    #     print('%d\t%-20s\t%-20s\t%-20.2f\t%-20.2f' % (i, Rlp, Klp, L, D))

    # print()

for i in range(6):
    if count[i] <= 0:
        averageL[i] = 0
        averageD[i] = 0
    else:
        averageL[i] = averageL[i] / count[i]
        averageD[i] = averageD[i] / count[i]
    if i == 5:
        print('For pixels > 600:')
    else:
        print('For pixels > %s:' % (i * 100))
    print('\tAverageL: %.3f\tAverageD: %.3f' % (averageL[i], averageD[i]))