import re
from pympler.asizeof import asizeof
import hashlib
import matplotlib.pyplot as plt
import numpy as np

#np.random.seed(300751)

# --------- PREPROCESSING -----------
# Import the Divina Commedia and lower all its words
divina_commedia = open("divina_commedia.txt", "r", encoding = "UTF-8").read().lower()
# Remove all the punctuation
divina_commedia = re.sub(r'[^\w\s]', '', divina_commedia)
# Divide all the poem in one string for each line
divina_commedia=divina_commedia.split("\n")
# Delete the titles
divina_commedia=divina_commedia[8:]
divina_commedia_w = []
for line in divina_commedia:
    if line.startswith("Inferno") or line.startswith("Purgatorio") or line.startswith("Paradiso"):
        divina_commedia.remove(line)
    # Divide all the lines in words
    divina_commedia_w.extend(line.split(" "))
# Remove empty strings
for el in divina_commedia_w:
    if el == "":
        divina_commedia_w.remove(el)

# --------- SENTENCES -----------
S = 6
count_sentences = 0
set_6 = set()
tot_sentence_size = 0

for i in range(len(divina_commedia_w)-S):
    if divina_commedia_w[i:i+S] :
        count_sentences += 1
        stringa = " ".join(divina_commedia_w[i:i+S])
        set_6.add(stringa)
        tot_sentence_size += asizeof(stringa)
print(f"Number of sencence of {S} words: {count_sentences}")
print(f"Average size of each sentence: {tot_sentence_size/count_sentences} bytes")
print(f"Memory occupied by the set of sentences: {asizeof(set_6)} bytes")

# --------- FINGERPRINTS - Bexp ---------
completed = False
i = 0

while not completed:
    n = 2**i
    set_hash_6 = set()
    breaked = False
    for el in set_6:
        word_hash = hashlib.md5(el.encode('utf-8')) 
        word_hash_int = int(word_hash.hexdigest(), 16) 
        h = word_hash_int % n
        if h in set_hash_6:
            i += 1
            breaked = True
            break
        else:
            set_hash_6.add(h)
    if not breaked:
        completed = True
        Bexp = i
        print(f"Bexp: {Bexp} bits")

# --------- FINGERPRINTS - Bteo ---------
# assume p = 0.5
# then m = 1.17*sqrt(n)
# dove n è il numero di frasi 
# m è il numro minimo di frasi da codificare affinchè ci sia almeno un conflitto
# E[m] = sqrt((pi/2)*n) = 1.25*sqrt(n)

p = 0.5
m = np.sqrt(2*count_sentences*np.log(1/(1-p)))
#print(f"Number of sentencens to experience a conflict when generating fingerprint: {int(m)}")
Bteo = np.log2(m)
print(f"Bteo: {int(np.ceil(Bteo))} bits")

# --------- FINGERPRINTS - FP Bexp ---------
pr_fp_Bexp = 1-(1-(1/(2**Bexp)))**count_sentences
print(f"Probability of false positive with Bexp: {pr_fp_Bexp}")

# --------- BIT STRING ARRAY - 1 ---------
X = [2**19, 2**20, 2**21, 2**22, 2**23]
pr_fp = {}
for x in X:
    # set_hash_6 = set()
    # conflict = 0
    # for el in set_6:
    #     word_hash = hashlib.md5(el.encode('utf-8')) 
    #     word_hash_int = int(word_hash.hexdigest(), 16) 
    #     h = word_hash_int % x
    #     if h in set_hash_6:
    #         conflict += 1
    #     else:
    #         set_hash_6.add(h)
    # pr_fp[x] = conflict/count_sentences
    pr_fp[x] = count_sentences/x

plt.plot(pr_fp.keys(), pr_fp.values())

# --------- BIT STRING ARRAY - 2 ---------
pr_fp_th = {}
for x in X:
    pr_fp_th[x] = 1-(1-(1/x))**count_sentences

plt.plot(pr_fp_th.keys(), pr_fp_th.values())
plt.legend(labels = ["Empirical", "Theoretical"])
# plt.xticks(X)
# plt.xscale("log")
plt.grid()
plt.title("Probability of false positive")
plt.xlabel("Memory")
plt.ylabel("Probability")
plt.show()
plt.close()

# --------- BLOOM FILTERS - 1 ---------
opt_k = {}
for x in X:
    k = (x/count_sentences)*np.log(2)
    opt_k[x] = np.ceil(k)

plt.plot(opt_k.keys(), opt_k.values(), marker = '*')
# plt.legend(labels = ["Empirical", "Theoretical"])
# plt.xticks(X)
# plt.xscale("log")
plt.grid()
plt.title("Optimal number of hash functions")
plt.xlabel("Memory")
plt.ylabel("#Hash functions")
plt.show()
plt.close()
    
# --------- BLOOM FILTERS - 2 ---------
pr_fp_k_theo = {}
for x in X:
    pr_fp_k_theo[x] = (1-np.exp(-opt_k[x]*count_sentences/x))**opt_k[x]

# plt.plot(pr_fp_k.keys(), pr_fp_k.values())
# # plt.legend(labels = ["Empirical", "Theoretical"])
# # plt.xticks(X)
# # plt.xscale("log")
# plt.grid()
# plt.title("Probability of false positive with the optimal number of hash functions")
# plt.xlabel("Memory")
# plt.ylabel("Probability of false positive")
# plt.show()
# plt.close()

# --------- BLOOM FILTERS - 3 ---------
for x in X:
    BF = np.zeros(10000000)
    for k in range(int(np.ceil(opt_k[x]))):
        tmp = k*" "
        for el in set_6:
            el = el+tmp
            word_hash = hashlib.md5(el.encode('utf-8'))
            word_hash_int = int(word_hash.hexdigest(), 16) 
            h = word_hash_int % x
            BF[h]=1
            print(h)
            break
    break

# --------- BLOOM FILTERS - 4 ---------
# pr_fp_k_th = {}
# for x in X:
#     BF = np.zeros(count_sentences)
#     for k in range(opt_k[x]):
#         for el in set_6:
#             word_hash = hashlib.md5(el.encode('utf-8'))
#             word_hash_int = int(word_hash.hexdigest(), 16) 
#             h = word_hash_int % x
#             BF[h]=1
#             break
#     break


    







# for k in range(int(np.ceil(opt_k[x]))):
#         for el in set_6:
#             word_hash = hashlib.md5(el.encode('utf-8'))
#             word_hash_int = int(word_hash.hexdigest(), 16) 
#             h = word_hash_int % x
#             print(h)
#             break
        
#     break