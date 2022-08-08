# Alan (Wentao Li), Imperial College London
# AICore 2022, all rights reserved

'''
This file is a Python implementation of the 'Rock, Paper & Scissors' game (without camera)
'''

import random
import cv2
from keras.models import load_model
import numpy as np

action = ['rock', 'paper', 'scissors'] # This should be a global variable really...