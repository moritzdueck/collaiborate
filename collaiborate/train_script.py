
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


def download_quickdraw_dataset(root="./data", class_names: List[str]=None):
    root = Path(root)
    root.mkdir(exist_ok=True, parents=True)
    url = 'https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/'

    print("Downloading Quickdraw Dataset...")
    for class_name in tqdm(class_names, leave=True):
        fpath = root / f"{class_name}.npy"
        if not fpath.exists():
            urllib.request.urlretrieve(f"{url}{urllib.parse.quote(class_name, safe='')}.npy", fpath)


def load_quickdraw_data(root="./data", max_items_per_class=5000):
    all_files = Path(root).glob('*.npy')

    x = np.empty([0, 784], dtype=np.uint8)
    y = np.empty([0], dtype=np.long)
    class_names = []

    print(f"Loading {max_items_per_class} examples for each class from the Quickdraw Dataset...")
    for idx, file in enumerate(tqdm(sorted(all_files))):
        data = np.load(file, mmap_mode='r')
        data = data[0: max_items_per_class, :]
        labels = np.full(data.shape[0], idx)
        x = np.concatenate((x, data), axis=0)
        y = np.append(y, labels)

        class_names.append(file.stem)

    return x, y, class_names


class QuickDrawDataset(torch.utils.data.Dataset):
    def __init__(self, root, max_items_per_class=5000, class_limit=None):
        super().__init__()
        self.root = root
        self.max_items_per_class = max_items_per_class
        self.class_limit = class_limit

        self.X, self.Y, self.classes = load_quickdraw_data(self.root, self.max_items_per_class)

    def __getitem__(self, idx):
        x = (self.X[idx] / 255.).astype(np.float32).reshape(1, 28, 28)
        y = self.Y[idx]

        return torch.from_numpy(x), y.item()

    def __len__(self):
        return len(self.X)

    def collate_fn(self, batch):
        x = torch.stack([item[0] for item in batch])
        y = torch.LongTensor([item[1] for item in batch])
        return {'pixel_values': x, 'labels': y}
    
    def split(self, pct=0.1):
        num_classes = len(self.classes)
        indices = torch.randperm(len(self)).tolist()
        n_val = math.floor(len(indices) * pct)
        train_ds = torch.utils.data.Subset(self, indices[:-n_val])
        val_ds = torch.utils.data.Subset(self, indices[-n_val:])
        return train_ds, val_ds
    
    def draw_image(self, idx):
        plt.figure()
        plt.imshow(self[0][0].reshape(28,28,1), cmap='Greys')
        plt.title(self.classes[self[0][1]])
        plt.show()
        
    def draw_mean_image(self, label):
        images = []
        for idx, drawing in enumerate(self):
            if drawing[1] == label:
                images.append(drawing[0].numpy())

        mean_img = np.mean(np.array(images), axis=0)
        plt.figure()
        plt.imshow(mean_img.reshape(28,28,1), cmap='Greys')
        plt.title(self.classes[label])
        plt.show()

def main(experiment_name, classes, epochs, learning_rate, batch_size, max_items_per_class=5000, train_val_split = 0.2):
    download_quickdraw_dataset(root="./data", class_names = classes)
    dataset = QuickDrawDataset(root = './data', max_items_per_class=max_items_per_class)

    for c in dataset.classes:
        print(f"{c} : {dataset.classes.index(c)}")

    writer = SummaryWriter()

    train_ds, val_ds = dataset.split(train_val_split)
    train_dataloader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    validation_dataloader = DataLoader(val_ds, batch_size=batch_size, shuffle=True)

    criterion = torch.nn.CrossEntropyLoss() 
    model = nn.Sequential(
        nn.Conv2d(1, 16, 3, padding='same'),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding='same'),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(32, 32, 3, padding='same'),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Flatten(),
        nn.Linear(288, 128),
        nn.ReLU(),
        nn.Linear(128, len(dataset.classes)),
    )

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in tqdm(range(epochs)):  # loop over the dataset multiple times
        train_loss = 0.0
        valid_loss = 0.0

        for i, batch in enumerate(train_dataloader, 0):
            x, y = batch
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
            writer.add_scalar("Loss/train_iteration", loss.item(), epoch * len(train_dataloader) + i)

        model.eval()

        for i, batch in enumerate(validation_dataloader, 0):
            x, y = batch
            x = x.to(device)
            y = y.to(device)
            logits = model(x)

            loss = criterion(logits.to(device), y.to(device))

            valid_loss += loss.item() * batch_size

        model.train()


        writer.add_scalar("Loss/train", train_loss/len(train_dataloader.sampler), epoch)
        writer.add_scalar("Loss/test", valid_loss/len(validation_dataloader.sampler), epoch)
        writer.flush()


        torch.save(model.state_dict(), './model_'+experiment_name+'.pth')
        writer.close()



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

