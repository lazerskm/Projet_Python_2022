import dash

from app import app
from fonctions.divers import moteur_recherche
from main import corpus

@app.callback(
    [dash.dependencies.Output('tableau', 'data'),
    dash.dependencies.Output('tableau', 'columns'),
    dash.dependencies.Output('tableau', 'hidden_columns')],
    dash.dependencies.Input('mots_clefs', 'value')
)
def update_table(value):
    if value == None or value == "":
        data = corpus.get_data()
        columns=[{"name": colonne, "id": colonne , "type" : "text" , "presentation" : "markdown"} for colonne in data.columns]
        data=data.to_dict('records')
        hidden_columns = ["score", "texte"]

    else :
        mots_clefs = list(value.split(" "))
        data = moteur_recherche(mots_clefs, corpus)
        columns=[{"name": colonne, "id": colonne , "type" : "text" , "presentation" : "markdown"} for colonne in data.columns]
        data=data.to_dict('records')
        hidden_columns = ["score", "texte"]
    
    return [data, columns, hidden_columns]