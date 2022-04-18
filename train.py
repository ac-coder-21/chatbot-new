# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 20:02:10 2022

@author: auuch
"""
import nltk
nltk.download('punkt')

from data_learning import tokenize, stem, bag_of_words
from model import NeuralNet

import numpy as np
import torch
import torch.nn as nn
import json
from torch.utils.data import Dataset, DataLoader

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
    
class Chat_Data(Dataset):
    def __init__(self):
        self.n_samples = len(words_list)
        self.words_data = words_list
        self.tag_data = tag_list
        
    def __getitem__(self, i):
        return self.words_data[i], self.tag_data[i] #error possiblity
    
    def __len__(self):
        return self.n_samples
    
batch_size = 8    
hidden_size = 8
learning_rate = 0.001
num_epochs = 1000
output_size = len(tags)
input_size = len(words_list[0])
print(input_size, len(all_words))
print(output_size, tags)

dataset = Chat_Data()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)
criterion = nn.CrossEntropyLoss()
optimiser = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device)
        outputs = model(words)
        labels = labels.type(torch.LongTensor)
        loss = criterion(outputs, labels)
        optimiser.zero_grad()
        loss.backward()
        optimiser.step()
    
    if (epoch + 1) % 100 == 0:
        print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}')
    print(f'final loss, loss={loss.item():.4f}')
    
data = {
        "model_state": model.state_dict(),
        "input_size": input_size,
        "output_size": output_size,
        "hidden_size": hidden_size,
        "all_words": all_words,
        "tags": tags
}
FILE = "data.pth"
torch.save(data, FILE)
print(f'training complete. File saved to {FILE}')