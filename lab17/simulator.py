import numpy as np
import string
from pympler.asizeof import asizeof
from utils import *
import matplotlib.pyplot as plt
import os
import re

np.random.seed(302179)


class AntiplagiarismSimulator:

    def __init__(self, filename = 'commedia.txt', sentence_size = 6, system = 'bloom_filter' ):
      self.filename = filename
      self.sentence_size = sentence_size
      self.system = system
      self.words = list()
      self.sentences = list()
      self.sentence_set = set()
      self.sentence_hash_set = set()
      self.memory_bit_string = dict()
    
    def preprocess(self, line):
        '''
        for each line of the read .txt file, the word is cleaned from puctuation and lowered. 
        '''
        # remove apostrophies
        line = re.sub(r'[^\w\s]', '', line)
        for word in line.split():
            if word != '':
                my_punctuation = string.punctuation
                # remove punctuation
                word = word.translate(str.maketrans('', '', my_punctuation))
                #make the word in lowercase
                word = word.lower()
                self.words.append(word)
    
    def store_sentences(self):
        '''
        Given the sentence size as attribute of the class, the sentences of length 6 are stored in a list
        '''
        for i in range(0,len(self.words)):
            # prevent OutOfIndex errors which would occurs in the last or in the firsts elements of the list
            if i < self.sentence_size or i > len(self.words) - self.sentence_size:
                continue
            # tokenization
            sentence = []
            for j in range(self.sentence_size,0,-1):
                sentence.append(self.words[i-j])
            self.sentences.append(sentence)

    def compute_average_sentence_size(self):
        '''
        first compute the average size of sentences 
        and stores all the sentence in a set
        '''
        total_sentences = len(self.sentences)
        sentence_weigth = 0
        for sentence in self.sentences:
            clause = ''
            for word in sentence:
                # concatenate the words within the sentence collected as a list of strings
                clause = clause  + " " + word
            # compute the cumulative weight of all the sentences
            sentence_weigth += asizeof(clause)
            # create the set of sentences
            self.sentence_set.add(clause)
        average_sentence_size = sentence_weigth/total_sentences
        return average_sentence_size, total_sentences
        
     
    
    def minimum_numer_of_bits(self):
        '''
        Compute the minimum number of bits such that no internal collision occurs. 
        '''
        i = 0
        collision = True
        while collision == True:
            self.sentence_hash_set = set()
            # total number of bits
            n = 2**i
            for sentence in self.sentence_set:
                # compute the hash of the sentence with an md5 encoding
                hash_ = compute_fingerprint(n, sentence)
                # if a collision occurs
                if hash_ in self.sentence_hash_set:
                    # increase the number of available bits
                    i = i + 1
                    break
                else:
                    self.sentence_hash_set.add(hash_)
                # keep increasin until all the sentences are not stored
                if len(self.sentence_hash_set) == len(self.sentence_set):
                    self.sentence_hash_set = self.sentence_hash_set
                    collision = False 
        return i +1
    
    
    def compute_false_positive_probability(self, memory):
        '''
        In the bit string array the FP probability can be easily computed by deviding the number of ones (total stored sentences)
        by the total space available in Bytes
        '''
        prob = (sum(self.memory_bit_string[memory])/memory)
        return prob
    
    def compute_thoeretical_false_positive_probability(self, memory):
        '''
        Theoretical FP probability is evaluated as 1-p where p is the probability that a certain bit is 0
        and p = (1-1/n)**m where n in the available memory and m is the total number od sentences.
        p is obtained from the Azuma-Hoeffding inequality which provides a quite accurate approximation.
        '''
        prob = (1-((1-1/memory)**sum(self.memory_bit_string[memory])))
        return prob
    
    
    def bit_string_population(self, M):
        for memory in M:
            # initialize an empty array 
            arr_f = np.zeros(memory, dtype=int)
            for sentence in self.sentence_set:
                h = compute_fingerprint(memory, sentence)
                # set to one the bit in the position that corresponds to the hash encoded sentence value
                arr_f[h] = 1
            # each memory value has its own bit string array
            self.memory_bit_string[memory] = arr_f
    


    def fingerprint_set_experiment(self):
        '''
        Use the fingerprint set in order to store all the sentences with 0 internal collisions and compute the 
        minimum number of bits such that the constraints are met. In the end compare the empirical resul with the 
        theoretical one.
        (Keep in min that the theoretical result is obtained with probability of collision equal to 0.5, maybe
        a theoretical proof of the result with p = 0 would be useful)
        '''
        print('=============== SET OF SENTENCES SIMULATION RESULTS ===============')
        with open(self.filename, 'r', encoding = "UTF-8") as f:
            for line in f:
                # remove descriptions, titles and subtitles
                if line in ["LA DIVINA COMMEDIA\n", "di Dante Alighieri\n", "INFERNO\n", "PURGATORIO\n", "PARADISO\n", "\n"]:
                    continue
                elif line.startswith("Inferno:") or line.startswith("Purgatorio:") or  line.startswith("Paradiso:"):
                    continue
                self.preprocess(line)
                # i dediced to remove..
        # store sentences in a list
        self.store_sentences()
        
        average_sentence_size, total_sentences = self.compute_average_sentence_size()
        print('total number of sentences: ', total_sentences)
        print('average size of each sentence: ', average_sentence_size)
        print('total memory occupancy of the set of sentences: ', asizeof(self.sentence_set))

        print('=============== SET OF FINGEPRINT SIMULATION RESULTS ===============')
        Bexp = self.minimum_numer_of_bits()
        print('Bexp: ', Bexp)

        false_pos_prob_emp = 1-(np.exp(-len(self.sentence_set)/(2**Bexp)))
        print(f'empirical fp prob: {false_pos_prob_emp}')
        # Bteo is the theoretical number of bits that i need to store hash encoding of the sentences 
        # with probability of collision of 50%
        Bteo = np.floor(np.log2((total_sentences/1.25)**2))

        false_pos_prob_theo = 1-(np.exp(-len(self.sentence_set)/(2**Bteo)))
        print('with p of collision = 0.5, Bteo: ', Bteo)
        print(f'theoretical fp prob: {false_pos_prob_theo}')

    def bit_string_array_experiment(self, M, M_strings):
        '''
        Use the bit string array to link the available array size with the probability of false positive
        '''
        print('=============== BIT STRING ARRAY SIMULATION RESULTS ===============')
        probs = list()
        theos = list()
        self.bit_string_population(M)
        for memory in M:
            emp_prob1 = self.compute_false_positive_probability(memory)
            probs.append(emp_prob1)
            theo_prob = self.compute_thoeretical_false_positive_probability(memory)
            theos.append(theo_prob)
        print(f'P_fp (for memory {M_strings[1]})/P_fp (for memory {M_strings[0]}): {probs[1]/probs[0]}')
        print(f'P_fp (for memory {M_strings[2]})/P_fp (for memory {M_strings[1]}): {probs[2]/probs[1]}')
        print(f'P_fp (for memory {M_strings[3]})/P_fp (for memory {M_strings[2]}): {probs[3]/probs[2]}')
        print(f'P_fp (for memory {M_strings[4]})/P_fp (for memory {M_strings[3]}): {probs[4]/probs[3]}')
        print(f'P_fp (for memory {M_strings[4]}) : {probs[4]}')
        print(f"'Predicted' P_fp (for memory 2^32): {(0.5**(32-23))*0.011}")

        return probs, theos
    
    def bloom_filter_experiment(self, M, M_strings):
        '''
        Use the bit string array to link the available array size with the probability of false positive by computing
        the optimal number of arrays for each value of available memory (i.e. for each bloom filter). 
        '''
        print('=============== BLOOM FILTER SIMULATION RESULTS ===============')
        ks_opt = list()
        for memory in M:
            # compute the optimal numbe of hash functions for each value of available memory
            k_opt = int(np.ceil((memory/len(self.sentence_hash_set))*np.log(2)))
            ks_opt.append(k_opt)

        
        probs_m = list()
        for memory, k in zip(M,ks_opt):
            # compute the theoretical probability for each value of available memory 
            prob = (1-(np.exp(-k*len(self.sentence_hash_set)/memory)))**k
            probs_m.append(prob)

        emp_prob_fp_bloom = list()
        for k,memory,m_string in zip(ks_opt, M, M_strings):
            hash_collisions = 0
            distinct_elements = 0
            BF = np.zeros(memory)
            # each hash function encoding has its own suffix
            suffixes = [i for i in range(k)]
            for sentence in self.sentence_set:
                indexes = list()
                counter = 0
                for suffix in suffixes:
                    # for each sentence compute the k-th hash dunction
                    new_sentence = sentence + str(suffix)
                    h = compute_fingerprint(memory, new_sentence)
                    indexes.append(h)
                for idx in indexes: 
                    if BF[idx] == 1:
                        # increase the counter of values that are already set to one within the same sentence
                        counter +=1
                    else: 
                        # set to one the corresponding value in the bloom filter
                        BF[idx] = 1
                if counter == len(indexes):
                    hash_collisions += 1
                else:
                    distinct_elements += 1
            # probability of internal hash collision
            # prob = (hash_collisions/self.sentence_set)
            # empirical probability of false positive
            unique_sentences_theo = -(memory/k)*np.log(1-(np.sum(BF)/memory))
            unique_sentences_emp = len(self.sentence_set) - hash_collisions
            print(f'For memory {m_string}, empirical unique sentences: {unique_sentences_emp} ')
            print(f'For memory {m_string}, theoretical unique sentences: {unique_sentences_theo} ')

            real_prob = (sum(BF)/memory)**k
            emp_prob_fp_bloom.append(real_prob)
        
        return probs_m, emp_prob_fp_bloom, ks_opt


def main():
    print('THE WHOLE SIMULATION WILL BE RUN ON A COLLECTION OF CANTI FROM DIVINA COMMEDIA POEM')

    if not os.path.exists('graphs'):
        os.mkdir('./graphs')

    # INPUT PARAMETER
    M_strings = ['2^19', '2^20', '2^21', '2^22', '2^23']            
    M = [2**19, 2**20, 2**21, 2**22, 2**23]

    # MAIN SIMULATOR
    simulator = AntiplagiarismSimulator()

    # fingeprint set experiment
    simulator.fingerprint_set_experiment()
    
    # bit string array experiment
    empirical_probs, theos = simulator.bit_string_array_experiment(M, M_strings)
    _, ax = plt.subplots(1,1)
    plot_metric(ax, M, empirical_probs, 'graphs/memory VS False Positive Probabilities', 'memory(bit)', 'probability', label = 'empirical FP probability', save_flag=False)
    plot_metric(ax, M, theos, 'graphs/memory VS theoretical False Positive Probabilities', 'memory(bit)', 'probability', label = 'theoretical FP probability', marker = None)
    plt.close

    # bloom filter experiment
    theoretical_probs, emp_prob_fp_bloom, ks_opt = simulator.bloom_filter_experiment(M, M_strings)

    _,ax = plt.subplots(1,1)
    plot_metric(ax, M, ks_opt, 'graphs/memory VS optimal number of hash functions', 'memory(bit)', 'optimal number of hash functions', label = 'optimal number of arrays')
    plt.close()

    _, ax = plt.subplots(1,1)
    plot_metric(ax, M, emp_prob_fp_bloom, 'graphs/memory VS probability of false positive (bloom)', 'memory (bit)', 'probability',label = f'theoretical probability', save_flag=False)
    plot_metric(ax, M, theoretical_probs, 'graphs/memory VS probability of false positive (bloom)', 'memory (bit)', 'probability',label = f'empirical probability', marker = None)

if __name__ == "__main__":
    main()