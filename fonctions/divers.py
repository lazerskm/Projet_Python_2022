import re
import math
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from numpy.linalg import norm

def nettoyer_texte(texte):
    texte = texte.lower()
    texte = texte.replace("\n", " ")
    regex = re.compile('[^a-zA-Z ]')
    texte = regex.sub('', texte)
    return texte

def tf(corpus, vocab):
    tf = []
    for doc in corpus.id2doc.values():
        occ_mots = list()
        for mot in vocab:
            nb_occ = doc.texte.count(mot)
            occ_mots.append(nb_occ)
        tf.append(occ_mots)
    return tf

def idf(corpus, vocab):
    liste_idf = []
    for mot in vocab.values():
        if mot['nombre_occurences_doc'] != 0:
            idf = math.log(corpus.ndoc / (mot['nombre_occurences_doc']))
        else:
            idf = 0
        liste_idf.append(idf)
    return liste_idf

def TFxIDF(tf, liste_idf):
    TFxIDF = list()
    for i in range(len(tf)):
        doc_TFxIDF = []
        for j in range(len(tf[i])):
            doc_TFxIDF.append(float(tf[i][j])*float(liste_idf[j]))
        TFxIDF.append(doc_TFxIDF)
    return csr_matrix(TFxIDF)

def make_clikable_url(row):
    return f'[Lien]({row})'

def moteur_recherche(mots_clefs, corpus):
    freq = corpus.stats(10)
    vocab = {}
    for i, mot in enumerate(freq.index):
        vocab[mot] = {"id" : i, "nombre_occurences_total" : int(freq.loc[mot][0]), "nombre_occurences_doc" : int(freq.loc[mot][1])}
    
    mat_tf = tf(corpus, vocab)
    mat_idf = idf(corpus, vocab)
    mat_TFxIDF = TFxIDF(mat_tf, mat_idf)
    
    req = list()
    for mot in vocab:
        if mot in mots_clefs:
            req.append(1)
        else:
            req.append(0)
    req = np.array(req)
    similarity_list = list()
    for i in range(mat_TFxIDF.shape[0]):
        mat = np.array(mat_TFxIDF.getrow(i).toarray()[0])
        cos = np.dot(req, mat) / (norm(req) * norm(mat))
        similarity_list.append(cos)
    
    auteurs = list()
    dates = list()
    textes = list()
    titres = list()
    url = list()
    
    for doc in corpus.id2doc.values():
        auteurs.append(doc.auteur)
        dates.append(doc.date)
        titres.append(doc.titre)
        textes.append(doc.texte)
        url.append(doc.url)
    data = {"titre" : titres, "auteur" : auteurs, "date" : dates, "texte" : textes, "lien" : url}
    df = pd.DataFrame.from_dict(data)
    df["score"] = similarity_list
    df['lien'] = df['lien'].apply(make_clikable_url)
    df = df.loc[df["score"] > 0]
    df = df.sort_values(by="score", ascending=False)
    return df