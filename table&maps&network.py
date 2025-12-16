import pandas as pd         #read_csv & dataframe operations
import dash                 #dash.Dash
from dash import html, dcc  #html.Div, html.H1, html.H2
import plotly.express as px #px.scatter_geo
import plotly.graph_objects as go
from dash import Input, Output
import networkx as nx

data = pd.read_csv('Victims_geocoded.csv', encoding='UTF-8')
data1 = pd.read_csv('Relationships.csv', encoding='utf-8')

############## table ##############
table_fig = go.Figure(data=[go.Table(
    header=dict(values=['Name', 'Date of birth', 'Date of death', 'Age of death']), #header names
    cells=dict(values=[data['Name'],
                       data['Birthdate'],
                       data['Deathdate'],
                       data['age']])
)])

############## map birthplace ##############
birth_circles = (
    data.groupby(['Birthplace', 'Birthlatitude', 'Birthlongitude'], as_index=False)
    .size() #groupby + size makes bubbles according to size
    .rename(columns={'size': 'victims'})
)

fig_birth_map = px.scatter_geo(   
                     birth_circles,
                     lat='Birthlatitude',
                     lon='Birthlongitude',
                     hover_name='Birthplace',
                     size='victims',
                     projection='natural earth', scope='europe')

############## map deathplace ##############
death_circles = (
    data.groupby(['Deathplace', 'Deathlatitude', 'Deathlongitude'], as_index=False)
    .size()
    .rename(columns={'size': 'victims'})
)

fig_death_map = px.scatter_geo(   
                     death_circles,
                     lat='Deathlatitude',
                     lon='Deathlongitude',
                     hover_name='Deathplace',
                     size='victims',
                     projection='natural earth', scope='europe')

############## network

#Reads the data from our relationship csv
data = pd.read_csv('Relationships.csv')

#Adding all unique IDs in the csv to a list of IDs
people_ids = []
for item in data['ID1']:
    if item not in people_ids:
        people_ids.append(item)
for item in data['ID2']:
    if item not in people_ids:
        people_ids.append(item)

#Adding all the relationships to a list of tuples
relationship_ids = []
for index, row in data.iterrows():
    relationship_ids.append((row['ID1'], row['ID2']))



#Creating the graph
G = nx.Graph()

#Adding our list of IDs so that each ID is their own node
G.add_nodes_from(people_ids)

#Adding all the "lines" between the nodes, these are called edges
G.add_edges_from(relationship_ids)

pos = nx.spring_layout(G)

edge_x = []
edge_y = []

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=1, color="gray"),
    hoverinfo="none",
    mode="lines"
)


node_x = []
node_y = []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers",
    text=list(G.nodes()),
    textposition="top center",
    hoverinfo="text",
    marker=dict(
        size=10,
        color="skyblue",
        line=dict(width=2, color="black")
    )
)

fig_net = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        title="Relative graph",
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
)


############## dash app ##############
app = dash.Dash(__name__) 
app.layout = html.Div([
        # table
        html.H1('Table over victims'),
        dcc.Graph(id = 'victims_table',figure = table_fig),
        # dropdown
            html.H2("Map"),
            dcc.Dropdown(
                id="map_selector",
                options=[
                    {"label": "Birthplaces", "value": "birth"},
                    {"label": "Deathplaces", "value": "death"},
                ],
                value="birth",   # default
                clearable=False
            ),
            dcc.Graph(id="map_graph"),    
       

        html.H2("Network graph"), #network graph here
        dcc.Graph(
            id='network_graph',
            figure=fig_net),
])

@app.callback(
    Output("map_graph", "figure"),
    Input("map_selector", "value")
)
def update_map(which):
    if which == "death":
        return fig_death_map
    return fig_birth_map
  
# run the app:
if __name__ == '__main__':
    app.run(debug=False, port=8040)


