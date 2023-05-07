import sys

from tqdm import tqdm
import torch
import math
import numpy as np
import os
import random
import pandas as pd

import torch.nn as nn
import scipy
from VAE import *
from pathlib import Path
from datetime import datetime
import multiprocessing as mp
from itertools import repeat



def get_df_intermediate_representation(layer, model, data):
    results = []
    for idx in tqdm(range(len(data))):
        x = data[idx][0]
        intermediate = model[:layer](torch.tensor(x).unsqueeze(dim=0))
        results.append([idx, intermediate.detach().numpy()])

    df = pd.DataFrame(results, columns=["idx", "intermediate"])
    df = df.set_index("idx")
    return df


def get_knn_tree(df):
    knn_input = np.stack(df["intermediate"].apply(lambda x: x.flatten()))
    tree = scipy.spatial.cKDTree(knn_input)
    return tree


def get_diff(df1, df2, k):
    overlaps = []
    t1 = get_knn_tree(df1)
    t2 = get_knn_tree(df2)
    for idx in tqdm(df1.index):
        query = df1.loc[idx].intermediate.flatten().reshape(1, -1)
        dd1, ii1 = t1.query(query, k=list(range(k + 1))[1:])
        query = df2.loc[idx].intermediate.flatten().reshape(1, -1)
        dd2, ii2 = t2.query(query, k=list(range(k + 1))[1:])
        overlaps.append([idx] + list(ii1.flatten()) + list(ii2.flatten()))
    df = pd.DataFrame(overlaps,
                      columns=["idx"] + ['a' + str(i) for i in range(k)] + ['b' + str(i) for i in range(k)])
    df = df.set_index("idx")
    return df


def get_cnn(wheights):
    classes = ['airplane',
               'apple',
               'bee',
               'car',
               'dragon',
               'mosquito',
               'moustache',
               'mouth',
               'pear',
               'piano',
               'pineapple',
               'smiley face',
               'train',
               'umbrella',
               'wine bottle']

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
        nn.Linear(128, len(classes)),
    )

    checkpoint = torch.load(wheights, map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint)
    model.eval()

    return model


def get_vae(wheights):
    model = VanillaVAE(3, 128)
    checkpoint = torch.load(wheights, map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint)
    model.eval()

    # reshape model so that layers can be indexed in flat structure
    flat_layers = []
    for name, layer in model.named_modules():
        if not isinstance(layer, torch.nn.Sequential):
            flat_layers.append(layer)

    flat_layers = flat_layers[1:]
    flat_layers = flat_layers[:15] \
                  + [nn.Flatten(start_dim=1)] \
                  + [flat_layers[15]] \
                  + [flat_layers[17]] \
                  + [nn.Unflatten(1, (512, 2, 2))] \
                  + flat_layers[18:]

    flat_model = nn.Sequential(*flat_layers)

    return flat_model


def process_one_layer(i, model, data, k, directory):
    df1 = get_df_intermediate_representation(i, model, data)
    df2 = get_df_intermediate_representation(i + 1, model, data)
    df_diff = get_diff(df1, df2, k)
    df_diff.to_csv(directory + 'diff-' + str(k) + '-' + str(i) + '-' + str(i) + '.csv')

if __name__ == '__main__':

    k = int(sys.argv[2])
    model = None
    if sys.argv[1] == 'cnn':
        model = get_cnn(sys.argv[3])
    elif sys.argv[1] == 'vae':
        model = get_vae(sys.argv[3])
    else:
        print('Please provide with cnn or vae as the model to use')
        sys.exit(-1)

    data = np.load(sys.argv[4], allow_pickle=True)

    directory = f"{datetime.now()}/results/"
    Path(directory).mkdir(exist_ok=True, parents=True)

    with mp.Pool(2) as p:
        p.starmap(process_one_layer, zip(range(32, 34), repeat(model), repeat(data), repeat(k), repeat(dir)))