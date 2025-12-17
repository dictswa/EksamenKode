import pandas as pd         #read_csv & dataframe operations
import dash                 #dash.Dash
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px #px.scatter_geo
import plotly.graph_objects as go
import dash_cytoscape as cyto

VictGeo_df = pd.read_csv('Victims_geocoded.csv', encoding='UTF-8')
Rela_df = pd.read_csv('Relationships.csv', encoding='utf-8', dtype=str)

############## table ##############
table_fig = go.Figure(data=[go.Table(
    header=dict(values=['Name', 'Date of birth', 'Date of death', 'Age of death']), #header names
    cells=dict(values=[VictGeo_df['Name'],
                       VictGeo_df['Birthdate'],
                       VictGeo_df['Deathdate'],
                       VictGeo_df['age']])
)])

############## map birthplace ##############
birth_circles = (
    VictGeo_df.groupby(['Birthplace', 'Birthlatitude', 'Birthlongitude'], as_index=False)
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
    VictGeo_df.groupby(['Deathplace', 'Deathlatitude', 'Deathlongitude'], as_index=False)
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

elements = []

for item in pd.concat([Rela_df['ID1'], Rela_df['ID2']]).unique():
    elements.append({'data': {'id': item}})

for _, row in Rela_df.iterrows():
    elements.append({'data': {'source': row['ID1'], 'target': row['ID2'], 
                              'general':row['General relationship type'],
                              'detailed':row['Detailed relationship type']}})





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
                value="birth",  #set birth as default
                clearable=False
            ),
            # map graph
            dcc.Graph(id="map_graph"), 
            # network graph
            html.H2("Network"),
            cyto.Cytoscape(
                id="cytoscape",
                elements=elements,
                layout={"name": "cose"},
            ),
            html.Div(id="cytoscape-tapNodeData-output"),
            html.Div(id="cytoscape-tapEdgeData-output"),
])

        



@app.callback(
    Output("map_graph", "figure"),
    Input("map_selector", "value")
)
def update_map(which):
    if which == "death":
        return fig_death_map
    return fig_birth_map


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

  
# run the app:
if __name__ == '__main__':
    app.run(debug=False, port=8040)


