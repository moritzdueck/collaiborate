from tqdm import tqdm
import torch
import math
import numpy as np
import os
import matplotlib.pyplot as plt
import random
import pandas as pd
import sklearn.metrics
import seaborn as sb

import torch.nn as nn
import scipy


def get_df_intermediate_representation(layer, subset):
    results = []
    for idx in tqdm(subset):
        x = val_data[idx][0]
        intermediate = model[:layer](torch.tensor(x).unsqueeze(1))
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
        overlaps.append([idx, [ii1, ii2] ])
    df = pd.DataFrame(overlaps, columns=["idx", "overlap"])
    df = df.set_index("idx")
    return df


if __name__ == '__main__':
    val_data = np.load("val_data.npy", allow_pickle=True)
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

    checkpoint = torch.load('./model_lessCapacity.pth', map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint)
    model.eval()

    subset_idx = np.random.choice(len(val_data), 100000, replace=False)

    for i in range(0,2):
        print("\n\n\n\n\nITERATION " + str(i) + "\n\n\n\n")
        df1 = get_df_intermediate_representation(i, subset_idx)
        df2 = get_df_intermediate_representation(i+1, subset_idx)
        df_diff = get_diff(df1, df2, 1000)
        df_diff.to_csv('diff100000-' + str(i) + '-' + str(i) + '.csv')
