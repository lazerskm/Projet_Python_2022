# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 17:50:36 2022

@author: Lazer
"""

import re

def nettoyer_texte(texte):
    texte = texte.lower()
    texte = texte.replace("\n", " ")
    regex = re.compile('[^a-zA-Z ]')
    texte = regex.sub('', texte)
    return texte