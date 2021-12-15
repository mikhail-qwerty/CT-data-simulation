import random
import os
import numpy as np
import matplotlib.pyplot as plt
from ct_segnet import viewer

def seed_everything(seed: int):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)


def show_mid_volume(volume, figsize=(12, 4)):
    fig, ax = plt.subplots(1,3, figsize=figsize)
    viewer.view_midplanes(vol = volume, ax = ax)