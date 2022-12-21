import random 
import numpy as np
import string
from pympler.asizeof import asizeof
from utils import *
import matplotlib.pyplot as plt
import os

class AntiplagiarismSimulator:

    def __init__(self, filename = 'commedia.txt', sentence_size = 6, system = 'bloom_filter' ):
      self.filename = filename
      self.sentence_size = sentence_size
      self.system = system
      self.words = list()
      self.sentences = list()
      self.sentence_set = set()
      self.sentence_hash_set = set()
    
    def preprocess(self, line):
        for word in line.split():
            if word != '': # capire se è possibile rimuover le stringhe vuote
                my_punctuation = string.punctuation
                word = word.translate(str.maketrans('', '', my_punctuation))
                #make the word in lowercase
                word = word.lower()
                #save the word
                self.words.append(word)
    
    def store_sentences(self):
        for i in range(0,len(self.words)):
                if i < self.sentence_size or i > len(self.words) - self.sentence_size:
                    continue
                sentence = []
                for j in range(self.sentence_size,0,-1):
                    sentence.append(self.words[i-j])
                self.sentences.append(sentence)

    def compute_average_sentence_size(self):
        '''
        this function first compute the average size of sentences 
        and stores all the sentence in a set
        '''
        total_sentences = len(self.sentences)
        sentence_weigth = 0
        for sentence in self.sentences:
            clause = ''
            for word in sentence:
                clause = word + ' ' + clause 
            sentence_weigth += asizeof(clause)
            self.sentence_set.add(clause)
            
        average_sentence_size = sentence_weigth/total_sentences
        return average_sentence_size
        
    
    
    def minimum_numer_of_bits(self):
        i = 1
        collision = True
        while collision == True:
            sentence_hash_set = set()
            n = 2**i
            for sentence in self.sentence_set:
                # bisogna capire quale n è corretto.
                hash_ = compute_fingerprint(n, sentence)
                if hash_ in sentence_hash_set:
                    i = i + 1
                    break
                else:
                    sentence_hash_set.add(hash_)
                if len(sentence_hash_set) == len(self.sentence_set):
                    self.sentence_hash_set = sentence_hash_set
                    collision = False 
        return i 
    
    def compute_false_positive_probability(self, memory):
        prob = (len(self.sentence_hash_set)/memory)
        return prob
    
    def compute_thoeretical_false_positive_probability(self, memory):
        prob = (len(self.sentence_hash_set)/memory)
        return prob
    


    def fingerprint_set_experiment(self):
        with open(self.filename, 'r', encoding = "UTF-8") as f:
            for line in f:
                if line in ["LA DIVINA COMMEDIA\n", "di Dante Alighieri\n", "INFERNO\n", "PURGATORIO\n", "PARADISO\n", "\n"]:
                    continue
                elif line.startswith("Inferno:") or line.startswith("Purgatorio:") or  line.startswith("Paradiso:"):
                    continue
                self.preprocess(line)
        self.store_sentences()
        print('average size of each sentence: ', self.compute_average_sentence_size())
        print('total memory occupancy of the set of sentences: ', asizeof(self.sentence_set))
        
        #Bexp is on because the returned i is the number of BITS that is less than the size in bites of the sentences set
        Bexp = self.minimum_numer_of_bits()
        print('Bexp: ', Bexp, 'which corresponds to', 2**Bexp, 'Bytes')
        # Bteo is the theoretical number of bits that i need to store hash encoding of the sentences 
        # with probability of collision of 50%
        Bteo = 1.25*np.sqrt(len(self.sentence_set))
        print('with p of collision = 0.5, Bteo: ', Bteo)
        #prob_fp = compute_false_positive_probability() 

    def bitstring_array_experiment(self, M):
        probs = list()
        for memory in M:
            prob = simulator.compute_false_positive_probability(memory)
            probs.append(prob)

        _, ax = plt.subplots(1,1)
        plot_metric(ax, M, probs, 'graphs/memory VS False Positive Probabilities', 'memory(bit)', 'probability')

        theos = list()
        for memory in M:
            prob = self.compute_thoeretical_false_positive_probability(memory)
            theos.append(prob)
        _, ax = plt.subplots(1,1)
        plot_metric(ax, M, theos, 'graphs/memory VS theoretical False Positive Probabilities', 'memory(bit)', 'probability')
        
    def bloom_filter_experiment(self, M):
        # Compute analytically the optimal number of hash functions in function of memory X, for X in the set 
        # [2^{19}, 2^{20}, 2^{21}, 2^{22}, 2^{23}] bits, and plot the corresponding graph.  See the above comment for X.
        # for this we have to compute k_opt = (n/m)*log(2) where n is the bit_size and m is the number of elements
        ks_opt = list()
        for memory in M:
            k_opt = int(np.ceil((memory/len(self.sentence_hash_set))*np.log(2)))
            ks_opt.append(k_opt)
        _,ax = plt.subplots(1,1)
        plot_metric(ax, M, ks_opt, 'graphs/memory VS optimal number of arrays', 'memory(bit)', 'optimal number of arrays')

        #By theory, evaluate the probability of false positive in function of X, using the optimal 
        # number of hash functions.
        # this is the theoretical result
        # The optimal number of filters is evaluated by computing the derivative of the function
        # given in the slides, to give a practical result we can provide a graph fixing
        # some values of k
        probs_k = list()
        
        for k in ks_opt:
            probs_m = list()
            for memory in M:
                prob = (1-(np.exp(-k*len(self.sentence_hash_set)/memory)))**k
                probs_m.append(prob)
            probs_k.append(probs_m)

        _, ax = plt.subplots(1,1)
        for lst in probs_k:
            plot_metric(ax, M, lst, 'graphs/memory VS probability of false positive', 'memory (bit)', 'probability', x_log_scale_flag=True, save_flag=False)
        plt.savefig('graphs/memory VS probability of false positive')

        # Describe how you implemented the different hash functions.
        # every time I want to encode a sentence in a bloom filter i can encode the string with a md5 encoding
        # and them the same string can be encoded in another filter by adding a random character and then
        # computing again the md5

        # By simulation, evaluate the probability of false positive in function of X, using the optimal number of hash functions, and plot the corresponding graph.
        # Compare the simulation results with the results obtained by just analytical formulas.
        filters = dict()
        hashes_dict = dict()
        for k,memory in zip(ks_opt, M):
            filters[k] = dict.fromkeys([i for i in range(k)], list())
            for sentence in list(self.sentence_set):
                for i in range(k-1):
                    if sentence not in hashes_dict.keys():
                        h = compute_fingerprint(memory, sentence)
                        filters[k][i].append(h)
                        hashes_dict[sentence] = h
                    else: 
                        filters[k][i] = hashes_dict[sentence]
                    sentence = sentence + 'q'
        #     print(len(filters[k].values())) # è giusto che di valori ce ne siano così tanti visto che k
        # print(len(filters.keys()))
        # print(len(self.sentence_set))
        # print(ks_opt)




        

        


        



            
if not os.path.exists('graphs'):
    os.mkdir('./graphs')
            
M = [2**19, 2**20, 2**21, 2**22, 2**23]

simulator = AntiplagiarismSimulator()
simulator.fingerprint_set_experiment()
simulator.bitstring_array_experiment(M)
simulator.bloom_filter_experiment(M)

