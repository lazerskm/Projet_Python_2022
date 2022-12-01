# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 16:36:46 2022

@author: Lazer
"""

import pickle
    
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)