# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 11:05:47 2022

@author: auuch
"""

import random
import json
import torch
from model import NeuralNet
from data_learning import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open('data.json', 'r') as f:
    data_json = json.load(f)
    
FILE = "data.pth"
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "LTCE-BOT"
print("I am here to help you")
while True:
    sentence = input("You: ")
    if sentence == "quit":
        break
    sentence = tokenize(sentence)
    word = bag_of_words(sentence, all_words)
    word = word.reshape(1, word.shape[0])
    word = torch.from_numpy(word)
    output = model(word)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    if prob.item() > 0.75:
        for d in data_json["data"]:
            if tag ==d["tag"]:
                print(f"{bot_name}: {random.choice(d['output'])}")
    else:
        print(f"{bot_name}: I do not understand...")