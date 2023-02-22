
from typing import List, Optional
import urllib.request
from tqdm import tqdm
from pathlib import Path
import requests
import torch
import math
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import random
import argparse
from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.nn.functional as F
import wandb

from utils import *

def main(experiment_name, classes, epochs, learning_rate, batch_size, max_items_per_class=5000, train_val_split = 0.2):
    download_quickdraw_dataset(root="./data", class_names = classes)
    dataset = QuickDrawDataset(root = './data', max_items_per_class=max_items_per_class)

    for c in dataset.classes:
        print(f"{c} : {dataset.classes.index(c)}")

    run = wandb.init(project='collaiborate')

    train_ds, val_ds = dataset.split(train_val_split)
    train_dataloader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    validation_dataloader = DataLoader(val_ds, batch_size=batch_size, shuffle=True)

    criterion = torch.nn.CrossEntropyLoss() 
    model = nn.Sequential(
        nn.Conv2d(1, 32, 3, padding='same'),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(32, 64, 3, padding='same'),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(64, 64, 3, padding='same'),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Flatten(),
        nn.Linear(576, 128),
        nn.ReLU(),
        nn.Linear(128, len(dataset.classes)),
    )

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    print(device)
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in tqdm(range(epochs)):  # loop over the dataset multiple times
        train_loss = 0.0
        valid_loss = 0.0

        for i, batch in enumerate(train_dataloader, 0):
            x, y, idx = batch
            x = x.to(device)
            y = y.to(device)
            logits = model(x)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            loss = criterion(logits.to(device), y.to(device))
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * batch_size
            wandb.log({'Loss/train_iteration': loss.item()})

        model.eval()

        for i, batch in enumerate(validation_dataloader, 0):
            x, y, idx = batch
            x = x.to(device)
            y = y.to(device)
            logits = model(x)

            loss = criterion(logits.to(device), y.to(device))

            valid_loss += loss.item() * batch_size

        model.train()

        wandb.log({'Loss/train': train_loss/len(train_dataloader.sampler)})
        wandb.log({'Loss/test': valid_loss/len(validation_dataloader.sampler)})

    torch.save(model.state_dict(), './model_'+experiment_name+'.pth')



if __name__ == '__main__':
    torch.multiprocessing.set_start_method('spawn')

    parser = argparse.ArgumentParser(description='Train CNN model')
    parser.add_argument('-t', '--tag', dest='tag', help='tag')

    parser.add_argument('-i', '--icons',dest='i', help='icons to use')
    parser.add_argument('-n', '--num_icons_per_class',dest='n', help='number of icons per class', type=int)

    parser.add_argument('-x', '--epochs',dest='epochs', help='Number of epochs', type=int, required=False)
    parser.add_argument('-y', '--learning_rate',dest='learning_rate', help='Learning arte', type=float, required=False)
    parser.add_argument('-z', '--batch_size',dest='batch_size', help='Number of epochs', type=int, required=False)
    

    parser.set_defaults(epochs=300)
    parser.set_defaults(learning_rate=1e-4)
    parser.set_defaults(batch_size=64)

    args = vars(parser.parse_args())

    print('Tagging model with tag: ' + args['tag'])

    print('Using icons: ' + args['i'])

    print('Epochs: ' + str(args['epochs']))
    print('Learning Rate: ' + str(args['learning_rate']))
    print('Batch Size: ' + str(args['batch_size']))

    torch.manual_seed(0)
    random.seed(0)
    np.random.seed(0)

    def seed_worker(worker_id):
        worker_seed = torch.initial_seed() % 2**32
        numpy.random.seed(worker_seed)
        random.seed(worker_seed)

    g = torch.Generator()
    g.manual_seed(0)

    main(args['tag'], args['i'].split(","), args['epochs'], args['learning_rate'], args['batch_size'], args['n'])

