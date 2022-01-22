# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 20:02:10 2022

@author: auuch
"""

import json
from data_learning import tokenize, stem, bag_of_words
import numpy as np

with open('data.json', 'r') as f:
    data = json.load(f)
    
all_words = []
tags = []
word_tag = []
for record in data['data']:
    tag = record['tag']
    tags.append(tag)
    for inp in record['input']:
        iData = tokenize(inp)
        all_words.extend(iData)
        word_tag.append((iData, tag))

ignore_symbols = ['?', '!', '.', ',']
all_words = [stem(wt) for wt in all_words if wt not in ignore_symbols]
all_words = sorted(set(all_words))
tags = sorted(tags)

words_list = []
tag_list = []

for(inp_Data, tag) in word_tag:
    bag = bag_of_words(inp_Data, all_words)
    words_list.append(bag)
    label = tags.index(tag)
    tag_list.append(label)
    
words_list = np.array(words_list)
tag_list = np.array(tag_list)
    
