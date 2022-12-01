# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 16:18:09 2022

@author: Lazer
"""

class Document :
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        
        f"auteur {auteur}"
        
    def print(self):
        print(
            "titre : " + self.titre +
            "\nauteur : " + self.auteur +
            "\ndate : " + self.date +
            "\nurl : " + self.url +
            "\ntexte : " + self.texte 
            )
        
    def __str__(self):
        return self.titre
    
    def getTexte(self):
        return self.texte
    
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"
    
class RedditDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, nbCom):
        super().__init__(titre, auteur, date, url, texte)
        self.nbCom = nbCom
        
    def getNbCom(self):
        return self.nbCom
    
    def setNbCom(self, nbCom):
        self.nbCom = nbCom
        
    def __str__(self):
        return f"Je suis un document Reddit et mon titre est : {super.__str__()}"
    
class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte):         
        super().__init__(titre, auteur, date, url, texte)
        
    def __str__(self):
        return f"Je suis un document Arxiv et mon titre est : {super.__str__()}"
    
class DocumentGenerator:
    @staticmethod
    def factory(docType, doc):
        if docType == "arxiv":
            return ArxivDocument(doc["title"], doc["author"], doc["published"], doc["link"][0]["@href"], doc["summary"])
        if docType == "reddit":
            return RedditDocument(doc.title, doc.author.name, doc.created, doc.url, doc.selftext, len(doc.comments._comments))
        assert 0, "Erreur : " + docType
    
    