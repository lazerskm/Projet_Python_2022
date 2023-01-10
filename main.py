# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 10:37:31 2022

@author: Lazer
"""

import pickle


from fonctions.scrapping import reddit_scrapping, arxiv_scrapping
from classes.Document import DocumentGenerator
from classes.Corpus import Corpus
from fonctions.divers import moteur_recherche

#donnees = reddit_scrapping() + arxiv_scrapping()

with open("donnees/corpus.pkl", "rb") as f:
    corpus = pickle.load(f) 

with open("donnees/donnees.pkl", "rb") as f:
    donnees = pickle.load(f)


corpus = Corpus("Mon corpus")
    
for i, doc in enumerate(donnees):

    corpus.add(i, DocumentGenerator.factory(doc[0], doc[1]))
    
with open("donnees/corpus.pkl", "wb") as f:
    pickle.dump(corpus, f)
with open("donnees/donnees.pkl", "wb") as f:
    pickle.dump(donnees, f)

test = moteur_recherche(["nba", "shoot", "percent"], corpus)
