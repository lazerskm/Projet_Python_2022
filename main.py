# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 10:37:31 2022

@author: Lazer
"""

import pickle


from fonctions.scrapping import reddit_scrapping, arxiv_scrapping
from classes.Document import DocumentGenerator
from classes.Corpus import Corpus
from fonctions.divers import nettoyer_texte
from scipy.sparse import csr_matrix
import math


#donnees = reddit_scrapping() + arxiv_scrapping()

with open("donnees/corpus.pkl", "rb") as f:
    corpus = pickle.load(f) 
    
"""with open("donnees/docs.pkl", "rb") as f:
    docs = pickle.load(f)  """

with open("donnees/donnees.pkl", "rb") as f:
    donnees = pickle.load(f)


corpus = Corpus("Mon corpus")
    
for i, doc in enumerate(donnees):

    corpus.add(i, DocumentGenerator.factory(doc[0], doc[1]))
    
with open("donnees/corpus.pkl", "wb") as f:
    pickle.dump(corpus, f)
with open("donnees/donnees.pkl", "wb") as f:
        pickle.dump(donnees, f)

corpus.search("NBA")
concordancier = corpus.concorde(18,"NBA")
print(concordancier.head())

#corpus.chaine_unique = nettoyer_texte(corpus.chaine_unique)

freq = corpus.stats(10)

vocab = {}

for i, mot in enumerate(freq.index):
    vocab[mot] = {"id" : i, "nombre_occurences_total" : int(freq.loc[mot][0]), "nombre_occurences_doc" : int(freq.loc[mot][1])}
    
tf = []
for doc in corpus.id2doc.values():
    occ_mots = list()
    for mot in vocab:
        nb_occ = doc.texte.count(mot)
        occ_mots.append(nb_occ)
    tf.append(occ_mots)

mat_tf = csr_matrix(tf)

liste_idf = []
for mot in vocab.values():
    if mot['nombre_occurences_doc'] != 0:
        idf = math.log(corpus.ndoc / (mot['nombre_occurences_doc']))
    else:
        idf = 0
    mot["idf"] = idf
    liste_idf.append(idf)
    
TFxIDF = list()
for i in range(len(tf)):
    doc_TFxIDF = []
    for j in range(len(tf[i])):
        doc_TFxIDF.append(float(tf[i][j])*float(liste_idf[j]))
    TFxIDF.append(doc_TFxIDF)
        
mat_TFxIDF = csr_matrix(TFxIDF)
