import Levenshtein
import difflib

a = '12345'
b = '13567'

L = Levenshtein.distance(a, b) / (len(a) + len(b))
D = difflib.SequenceMatcher(a=a, b=b).ratio()

print(L, " ", D)