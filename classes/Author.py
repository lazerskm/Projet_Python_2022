class Author:
    
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = {}
        
    def add(self, idDocument, document):
        self.production[idDocument] = document
        self.ndoc += 1
        
    def __str__(self):
        return self.name
    
    def print(self):
        print(
            "nom : " + self.name +
            "\nombre de document(s) : " + self.ndoc +
            "\production : " + self.production
            )
        
    def getNbProd(self):
        return len(self.production)
    
    def getTailleMoyProd(self):
        sommeMot = 0
        for doc in self.production.values():
            sommeMot += len(doc.texte.split(" "))
        string = f"Moyenne de mots par texte : {round(sommeMot/self.getNbProd(), 2)}"
        return string