# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 14:27:26 2022

@author: Lazer
"""

import pandas as pd

df = pd.read_csv("donnees_basketball.csv", sep = "\t")
print(len(df["textes"]))

"""for texte in df["textes"]:
    print(f"nombre de mots : {len(texte.split())}")
    print(f"nombre de phrases : {len(texte.split('.'))}")"""
    
df2 = df.drop(df[df["textes"].map(len) < 20].index)

texte = "²".join(df2["textes"])

print(len(texte.split("²")))

