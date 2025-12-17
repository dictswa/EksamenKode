# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 08:57:00 2025

@author: dicte
"""

import pandas as pd
from dash import Dash, html, Input, Output, callback
import dash_cytoscape as cyto

file = pd.read_csv('Relationships.csv', dtype=str)

elements = []

for item in pd.concat([file['ID1'], file['ID2']]).unique():
    elements.append({'data': {'id': item}})

for _, row in file.iterrows():
    elements.append({'data': {'source': row['ID1'], 'target': row['ID2'], 
                              'general':row['General relationship type'],
                              'detailed':row['Detailed relationship type']}})

app = Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        layout={'name': 'cose'},
        style={'width': '100%', 'height': '600px'},
    ),
    html.Div(id='cytoscape-tapNodeData-output'),
    html.Div(id='cytoscape-tapEdgeData-output')
])

@callback(
    Output('cytoscape-tapNodeData-output', 'children'),
    Input('cytoscape', 'tapNodeData')
)

def displayTapNodeData(data):
    if data is None:
        return ""
    return f"You tapped the id: {data['id']}"

@callback(
     Output('cytoscape-tapEdgeData-output', 'children'),
     Input('cytoscape', 'tapEdgeData')
)

def displayTapEdgeData(data):
    if data is None:
        return ""
    if 'source' not in data or 'target' not in data:
        return ""
    return f"The relation is {data['general']} and {data['detailed']}"

app.run(debug=True, port=8040)
