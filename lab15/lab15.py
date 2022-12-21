import string
from pympler import asizeof
import hashlib
from show_results import *
import numpy as np

#read the txt 
words = [ ]
verse_count = 0
S = [4,8]
epsilon = [.5, .1, .05, .01, .005, .001]
with open('commedia.txt','r', encoding = "UTF-8") as file:
    # reading each line    
    for line in file:
        #some data cleaning
        if line in ["LA DIVINA COMMEDIA\n", "di Dante Alighieri\n", "INFERNO\n", "PURGATORIO\n", "PARADISO\n", "\n"]:
            description = ["LA DIVINA COMMEDIA\n", "di Dante Alighieri\n", "INFERNO\n", "PURGATORIO\n", "PARADISO\n", "\n"]
            continue
        elif line.startswith("Inferno:") or line.startswith("Purgatorio:") or  line.startswith("Paradiso:"):
            continue
        else:
            #if the line should not be cleaned, consider it a verse
            verse_count += 1
            #save the words in a string
            for word in line.split():
                #remove punctuation
                my_punctuation = string.punctuation
                word = word.translate(str.maketrans('', '', my_punctuation))
                #make the word in lowercase
                word = word.lower()
                #save the word
                words.append(word)

print("Number of words: ", len(words))
print("Number of verses: ", verse_count)
print("Number of distinct words: ", len(set(words)))

#define senteces as sequences of 4 words; at the moment they'll be put in a list, later we'll use a data struct more suitable
sentences_4 = [ ]
for i in range(0,len(words)):
    if i < 4 or i > len(words) - 4:
        pass
    sentence = []
    for j in range(3,0,-1):
        sentence.append(words[i-j])
    sentences_4.append(sentence)

print("Number of sentences with sencence length = 4: ", len(sentences_4))

sentences_8 = []
for i in range(0,len(words)):
    if i < 8 or i > len(words) - 8:
        continue
    sentence = []
    for j in range(7,0,-1): 
        sentence.append(words[i-j])
    sentences_8.append(sentence)

print("Number of sentences with sencence length = 8: ", len(sentences_8))

# What is the experimental amount of stored data in bytes, independently from the adopted data structure?
print(f'Total amount of memory in bytes: {asizeof.asized(words)}')
print(f'Amount of memory of the distinct words: {asizeof.asized(set(words))}')

# Implement a solution storing the sentence strings in a python set. What is the actual amount of memory occupancy?
sentences_set_4 = set()
for sentence in sentences_4:
    sentence_as_str = str()
    for word in sentence:
        sentence_as_str = sentence_as_str + word + ' '
    sentences_set_4.add(sentence_as_str)

print(f'Total amount of memory in bytes of sentences of length 4: {asizeof.asized(sentences_set_4)}')

sentences_set_8 = set()
for sentence in sentences_8:
    sentence_as_str = str()
    for word in sentence:
        sentence_as_str = sentence_as_str + word + ' '
    sentences_set_8.add(sentence_as_str)

print(f'Total amount of memory in bytes of sentences of length 8: {asizeof.asized(sentences_set_8)}')

print(len(sentences_set_8))
probabilities_4 = list()
probabilities_8 = list()

fingerprint_size_4 = list()
fingerprint_size_8 = list()

theoretical_sizes_4 = list()
theoretical_sizes_8 = list()


# Implement a solution storing the fingerprints in a python set.
# given a fixed epsilon which is the tolerance to the false positive probability
for eps in epsilon:
    print(eps)
    hash_dim_4 = int(len(sentences_4)/eps)
    theoretical_size_4 = np.ceil(len(sentences_4)*np.log2(hash_dim_4))
    theoretical_sizes_4.append(theoretical_sizes_4)


    hash_set_4 = set()
    # compute the hash of a given string using md5 on a range [0,n-1]
    for sentence in sentences_set_4: # string to hash
        sentence_hash_4 = hashlib.md5(sentence.encode('utf-8')) # md5 hash
        sentence_hash_int_4 = int(sentence_hash_4.hexdigest(), 16) # md5 hash in integer format
        h = sentence_hash_int_4 % hash_dim_4 # map into [0,n-1]
        hash_set_4.add(h)
    
    hash_dim_8 = int(len(sentences_8)/eps)
    theoretical_size_8 = np.ceil(len(sentences_8)*np.log2(hash_dim_8))
    theoretical_sizes_8.append(theoretical_sizes_8)

    hash_set_8 = set()
    for sentence in sentences_set_8: # string to hash
        sentence_hash_8 = hashlib.md5(sentence.encode('utf-8')) # md5 hash
        sentence_hash_int_8 = int(sentence_hash_8.hexdigest(), 16) # md5 hash in integer format
        h = sentence_hash_int_8 % hash_dim_8 # map into [0,n-1]
        hash_set_8.add(h)
        
    # Show the formula and the graph with the fingerprint size in function of the 
    # probability of false positive for this specific scenario, in two conditions: S=4, S=8.

    # fingerprint size = y
    # probability of false positive = x



    # false positive probability for S = 4
    false_positive_pr_4 = 1-(1-(1/hash_dim_4))**len(hash_set_4)
    probabilities_4.append(false_positive_pr_4)
    #fingerprint size for S = 8
    size_fingerprint_4 = asizeof.asized(hash_set_4)
    fingerprint_size_4.append(size_fingerprint_4.flat)
    print('size of fingerprint for sentences with length 4: ', size_fingerprint_4)

    
    # false positive probability for S = 8
    false_positive_pr_8 = 1-(1-(1/hash_dim_8))**len(hash_set_8)
    probabilities_8.append(false_positive_pr_8)
    #fingerprint size for S = 8
    size_fingerprint_8 = asizeof.asized(hash_set_8)
    fingerprint_size_8.append(size_fingerprint_8.flat)
    print('size of fingerprint for sentences with length 8: ', size_fingerprint_8)


    # a questo punto al variare di S e quindi al variare della probabilità devo vedere come varia la size?
    # per size si intende la memoria oppure la lunghezza del set?
    # potrebbe essere un'idea raccogliere le frasi non con stride 1 ma con uno stride diverso? 
    # ricorda nel caso di cambiare il primo range aggiungendo uno step diverso quando crei le frasi

fig2, ax2 = plt.subplots(1,1)
plot_metric(fig2, ax2, fingerprint_size_4 , 'sentence size = 4', 'o',  x_label='probability', y_label = 'size in bytes',  x_values = probabilities_4)
ax2.scatter(probabilities_4, theoretical_sizes_4)
plot_metric(fig2, ax2, fingerprint_size_8 , 'sentence size = 8', 'o',  x_label='probability', y_label = 'size in bytes',  x_values = probabilities_4)
ax2.scatter(probabilities_8, theoretical_sizes_8)
ax2.set_title(f'probability vs fingerprint_size', fontsize=14)
fig2.savefig(f'probability vs fingerprint_size')
plt.close()
