from classes.Author import Author
from fonctions.divers import nettoyer_texte, make_clikable_url

import pandas as pd
import pickle
import re

class Corpus:
    chaine_unique = ""
    
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        
    def save(self):
        with open(f"{self.nom}.pkl", "wb") as f:
            pickle.dump(self, f)
            
    def add(self ,index,  doc):
        if doc.auteur not in self.authors:
            self.naut += 1
            self.authors[doc.auteur] = Author(doc.auteur)
        self.authors[doc.auteur].add(index, doc)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))
    
    def search(self, mot_clef):
        if self.chaine_unique == "" :
            textes = [doc.getTexte() for doc in self.id2doc.values()]
            self.chaine_unique = " ".join(textes)
            
        return re.findall(mot_clef, self.chaine_unique)
    
    def concorde(self, taille_contexte, mot_clef):
        if self.chaine_unique == "" :
            textes = [doc.getTexte() for doc in self.id2doc.values()]
            self.chaine_unique = " ".join(textes)
            
        index = re.finditer(mot_clef, self.chaine_unique)
        avant = []
        mot = []
        apres = []
        for match in index:
            start = match.span()[0]
            end = match.span()[1]
            string = self.chaine_unique[start-taille_contexte:end+taille_contexte]            
            string_split = string.split(mot_clef)
            avant.append(string_split[0])
            apres.append(string_split[1])
            mot.append(mot_clef)
        df = pd.DataFrame({"contexte gauche" : avant, 
                           "motif trouvé" : mot, 
                           "contexte droit" : apres})
        return df
    
    def stats(self, n):
        if self.chaine_unique == "" :
            textes = [doc.getTexte() for doc in self.id2doc.values()]
            self.chaine_unique = " ".join(textes)
            
        self.chaine_unique = nettoyer_texte(self.chaine_unique)
        words = re.split(r'\t|\s', self.chaine_unique)
        words = [word for word in words if word != '']
        set_w = set(words)
        dict_w = {i:w for i, w in enumerate(set_w)}

        df = pd.DataFrame({"word" : words})
        freq = pd.crosstab(index = df["word"], columns="freq")
        
        doc_freq = []
        for index, row in freq.iterrows():
            cpt = 0
            for doc in self.id2doc.values():
                if f'{index}' in doc.texte:
                    cpt+=1
            doc_freq.append(cpt)
        
        freq["document frequency"] = doc_freq
        print(freq.sort_values(by="freq", ascending=False).head(n))
        print("nombre de mots différents : " + str(len(dict_w)))
        return freq
        
    def get_data(self):
        auteurs = list()
        dates = list()
        textes = list()
        titres = list()
        url = list()   
        
        for doc in self.id2doc.values():
            auteurs.append(doc.auteur)
            dates.append(doc.date)
            titres.append(doc.titre)
            textes.append(doc.texte)
            url.append(doc.url)
            
        data = {"titre" : titres, "auteur" : auteurs, "date" : dates, "texte" : textes, "lien" : url}
        df = pd.DataFrame.from_dict(data)
        df['lien'] = df['lien'].apply(make_clikable_url)
        return df
        