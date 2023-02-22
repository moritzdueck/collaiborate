from typing import List
import urllib.request
from tqdm import tqdm
from pathlib import Path
import torch
import math
import numpy as np
import matplotlib.pyplot as plt


def download_quickdraw_dataset(root="../data/npy", class_names: List[str]=None):
    root = Path(root)
    root.mkdir(exist_ok=True, parents=True)
    url = 'https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/'

    print("Downloading Quickdraw Dataset...")
    for class_name in tqdm(class_names, leave=True):
        fpath = root / f"{class_name}.npy"
        if not fpath.exists():
            urllib.request.urlretrieve(f"{url}{urllib.parse.quote(class_name, safe='')}.npy", fpath)


def download_quickdraw_dataset_binary(root="./data/binary", class_names: List[str]=None):
    root = Path(root)
    root.mkdir(exist_ok=True, parents=True)
    url = 'https://storage.googleapis.com/quickdraw_dataset/full/binary/'

    print("Downloading Quickdraw Dataset...")
    for class_name in tqdm(class_names, leave=True):
        fpath = root / f"{class_name}.bin"
        if not fpath.exists():
            urllib.request.urlretrieve(f"{url}{urllib.parse.quote(class_name, safe='')}.bin", fpath)

def load_quickdraw_data(root="../data/npy", max_items_per_class=5000):
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

        return torch.from_numpy(x), y.item(), idx

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
        plt.imshow(self[idx][0].reshape(28,28,1), cmap='Greys')
        plt.title(self.classes[self[idx][1]])
        plt.show()
        
    def draw_mean_image(self, label, subplot=None):
        images = []
        for idx, drawing in enumerate(self):
            if drawing[1] == label:
                images.append(drawing[0].numpy())

        mean_img = np.mean(np.array(images), axis=0)
        
        if subplot is not None:
            subplot.imshow(mean_img.reshape(28,28,1), cmap='Greys')
            subplot.title(self.classes[label])
        else: 
            plt.figure()
            plt.imshow(mean_img.reshape(28,28,1), cmap='Greys')
            plt.title(self.classes[label])
            plt.show()