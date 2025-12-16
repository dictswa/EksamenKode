import pandas as pd
import plotly.graph_objects as go
import networkx as nx

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
    mode="markers+text",
    text=list(G.nodes()),
    textposition="top center",
    hoverinfo="text",
    marker=dict(
        size=10,
        color="skyblue",
        line=dict(width=2, color="black")
    )
)

fig = go.Figure(
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

import plotly.io as pio
pio.renderers.default = "browser"


# Show plot
fig.show()


