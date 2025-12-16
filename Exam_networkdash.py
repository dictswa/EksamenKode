import pandas as pd
from dash import Dash, html
import dash_cytoscape as cyto

data = pd.read_csv('Relationships.csv')

people_ids = []
for item in data['ID1']:
    if {'data':{'id': item}} not in people_ids:
        people_ids.append({'data':{'id': str(item)}})
for item in data['ID2']:
    if {'data':{'id': item}} not in people_ids:
        people_ids.append({'data':{'id': str(item)}})

for index, row in data.iterrows():
    people_ids.append({'data':{'source':str(row['ID1']),'target':str(row['ID2'])}})



app = Dash(__name__)

app.layout = html.Div([
    html.P("Relative Cytoscape:"),
    cyto.Cytoscape(
        id='cytoscape',
        elements=people_ids,
        layout={'name': 'cose'},
        style={'width': '1920px', 'height': '1080px'}
    )
])


app.run(debug=True,port=8080)
