from app import run_app
import callback
from fonctions.scrapping import reddit_scrapping, arxiv_scrapping
from classes.Corpus import Corpus
from classes.Document import DocumentGenerator
import pickle



"""donnees = reddit_scrapping() + arxiv_scrapping()
    
with open("donnees/donnees.pkl", "wb") as f:
    pickle.dump(donnees, f)"""
    
with open("donnees/donnees.pkl", "rb") as f:
    donnees = pickle.load(f)

corpus = Corpus("Mon corpus")
    
for i, doc in enumerate(donnees):
    corpus.add(i, DocumentGenerator.factory(doc[0], doc[1]))
    
if __name__ == '__main__':
    run_app()