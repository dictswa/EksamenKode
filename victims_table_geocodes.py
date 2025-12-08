import pandas as pd
import dash
from dash import html
from dash import dcc
from dash import dash_table 
import plotly.express as px

from dash.dependencies import Input, Output
import plotly.io as pio
import pandas


#?måske er der nogen imports der ikke bruges?


data = pd.read_csv('victims.csv') #read csv file

####################### table

#tilføj age at death når vi har den
table_data = data[["Name", "Birthdate", "Deathdate"]] #.unique? no need i would think


df = pd.read_csv("victims_geocoded.csv", encoding="UTF-8")

############### geomap birthplace
#df['victims'] = df['Birthplace']

birth_circles = (
    df.groupby(['Birthplace', 'Birthlatitude', 'Birthlongitude'], as_index=False)
    .size()
    .rename(columns={'size': 'victims'})
)

fig_b = px.scatter_geo(   
                     birth_circles,
                     lat="Birthlatitude",
                     lon="Birthlongitude",
                     hover_name="Birthplace",
                     size="victims",
                     projection="natural earth")

pio.renderers.default = 'browser'

#fig.show()

######### deathplace

#df['victims'] = df['Deathplace']

death_circles = (
    df.groupby(['Deathplace', 'Deathlatitude', 'Deathlongitude'], as_index=False)
    .size()
    .rename(columns={'size': 'victims'})
)

fig_d = px.scatter_geo(   
                     death_circles,
                     lat="Deathlatitude",
                     lon="Deathlongitude",
                     hover_name="Deathplace",
                     size="victims",
                     projection="natural earth")

pio.renderers.default = 'browser'


############ dash app
#Layout
app = dash.Dash(__name__) #dash.Dash: says "make me an app"
app.layout = html.Div([
        html.H1("Table over victims"), #make better title
        
        #datatable i stedet for dropdown
        dash_table.DataTable(
            id = 'victims_table',
            columns = [
                {"name": "Name", "id": "Name"},
                {"name": "Date of birth", "id": "Birthdate"},
                {"name": "Date of death", "id": "Deathdate"},
            ],
            data=table_data.to_dict("records")
        ),
     #spg: hvorfor skal vi ikke bruge en tom graf
         html.H2("Birthplaces of victims"),
         dcc.Graph(
             id="birthplace_map",
             figure=fig_b
        ),
        html.H2("Deathplaces of victims"),
        dcc.Graph(
            id="deathplace_map",
            figure=fig_d
       ),
         
])
    

# run the app:

if __name__ == '__main__':
    app.run(debug=False, port=8090)
#no callback for now. We can add later if sounds fun. example: filter by year, gender, convert number to stats, search field?


