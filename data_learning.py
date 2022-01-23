# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 19:41:49 2022

@author: auuch
"""

import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
    tokenized_sentence = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32())
    for index, word in enumerate(all_words):
        if word in tokenized_sentence:
            bag[index] = 1.0
    return bag


