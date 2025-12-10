# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 12:01:45 2025

@author: rojan
"""

import csv
import pandas as pd
import networkx as nx
import matplotlib as plt
import urllib
import numpy as np
import os
from dash import Dash, html, dcc
import plotly.express as px
import plotly.io as pio
import dash_cytoscape as cyto
import plotly.express as px
import plotly.graph_objects as go
import random
from dash.dependencies import Input, Output



data = pd.read_csv('Relationships.csv', encoding='utf-8')

data1 = pd.read_csv('Victims.csv',sep=';', encoding='windows-1252')


idlist = data1['ID'].unique().tolist()
namelist = data1['Name'].tolist()
iddict = {}
for i in zip(idlist,namelist):
    iddict[str(i)] = []
    
idlist1 = list(iddict.keys()) #Det her er str, idlist er int
did1 = data['ID1']
did2 = data['ID2']
rdid1 = data['General relationship type']
rdid2 = data['Detailed relationship type']

did1 = list(did1)
did2 = list(did2)
rdid1 = list(rdid1)
rdid2 = list(rdid2)

#zip gør, at den looper i hver af de variabler i parantesen. 
for rel1, rel2, reltype1, reltype2 in zip(did1,did2, rdid1, rdid2):
    arel1 = str(rel1)
    arel2 = str(rel2)
    ardid1 = (rdid1)
    ardid2 = (rdid2)
    if arel1 in iddict:
        iddict[arel1].append(ardid1)
        iddict[arel1].append(ardid2)
        iddict[arel1].append(arel2)


tuples = []
for rel1, rel2, reltype1, reltype2 in zip(did1,did2, rdid1, rdid2):
    arel1 = str(rel1)
    arel2 = str(rel2)
    relationship_label = str(reltype2) 
    tuples.append((arel1, arel2, relationship_label))

#Havde lidt svært ved at rode mig ud af mine variabler, så fandt jeg ud af, man
#kan indhente data på den her måde
reledge = pd.DataFrame(
    tuples, 
    columns=['ID1', 'ID2', 'Detailed relationship type']
)
G = nx.DiGraph()
G = nx.from_pandas_edgelist(
    reledge, 
    source='ID1', 
    target='ID2',
    edge_attr=True 
)
nx.draw_spring(G, with_labels=True) #uden with_labels=True er ID ikke med

# G.add_nodes_from(iddict)
# G.add_edges_from(data)




# app = Dash(__name__)

# app.layout = html.Div([
#     html.P("Dash Cytoscape:"),
#     cyto.Cytoscape(
#         id='cytoscape',
#         elements=[
#             {'data': {'id': 'ca', 'label': 'Canada'}},
#             {'data': {'id': 'on', 'label': 'Ontario'}},
#             {'data': {'id': 'qc', 'label': 'Quebec'}},
#             {'data': {'source': 'ca', 'target': 'on'}},
#             {'data': {'source': 'ca', 'target': 'qc'}}
#         ],
#         layout={'name': 'breadthfirst'},
#         style={'width': '400px', 'height': '500px'}
#     )
# ])


# app.run(debug=True)
            
# for j in idlist:
#     for k in data['ID1']:
#         if j == k:
#             if j == iddict[j]:
#               iddict[j].append(data['ID2'[k]])






# nx.draw_spring(G, with_labels=True)


# nodelist = g.add_nodes_from(nodes_for_adding, attr)
# edgelist = g.add_edges_from([data[0, 1]])

# edge_list = [names1[2], names1[4]]
# network = nx.MultiDiGraph()
# network.add_nodes_from(names)
# network.add_edge(names1[2], names1[4])

# nx.draw_spring(network, with_labels=True)

