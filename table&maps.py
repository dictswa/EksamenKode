import pandas as pd         #read_csv & dataframe operations
import dash                 #dash.Dash
from dash import html, dcc  #html.Div, html.H1, html.H2
import plotly.express as px #px.scatter_geo
import plotly.graph_objects as go

data = pd.read_csv('victims_geocoded.csv', encoding='UTF-8')

############## table ##############
table_fig = go.Figure(data=[go.Table(
    header=dict(values=['Name', 'Date of birth', 'Date of death']), #header names
    cells=dict(values=[data['Name'],
                       data['Birthdate'],
                       data['Deathdate']])
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
                     projection='natural earth')

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
                     projection='natural earth')

############## dash app ##############
app = dash.Dash(__name__) 
app.layout = html.Div([
        html.H1('Table over victims'),
        dcc.Graph(
            id = 'victims_table',
            figure = table_fig
        ),
         html.H2("Birthplaces of victims"),
         dcc.Graph(
             id="birthplace_map",
             figure=fig_birth_map
        ),
        html.H2('Deathplaces of victims'),
        dcc.Graph(
            id='deathplace_map',
            figure=fig_death_map
       ),
         
])
    
# run the app:
if __name__ == '__main__':
    app.run(debug=False, port=8090)


