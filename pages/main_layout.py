from dash import html, dcc , dash_table
    
champ_texte = dcc.Input(id = "mots_clefs", type="text", placeholder="", debounce=True)

tableau = dash_table.DataTable(
    id = 'tableau',
    editable=False,
    sort_action='native',
    filter_action='native',
    page_size=10,
    style_header={
        'font-size': 18,
        'background-color': '#a4c3b2',
        'font-weight': 'bold',
        'font-family' : 'PT Sans',
        'font-style' : 'regular 400',
        'border': '1px solid #6b9080',
        'textAlign': 'center'
    },
    style_data={
        'font-family' : 'PT Sans',
        'font-style' : 'regular 400',
        'border': '2px solid gray',
        'border-radius': '5px',
        'whiteSpace': 'normal',
        'height': 'auto'
    }
)

main_layout = html.Div([
    html.I("Entrez vos mots-clés"),
    html.Br(),
    champ_texte,
    html.Br(),
    tableau,
    html.Div(id="output")
])