import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
from dash import dash_table 

#?måske er der nogen imports der ikke bruges?


data = pd.read_csv('victims.csv') #read csv file


#Figure out how to convert death+birth date from str to num
#eller bare lav den i det andet doc, sikkert nemmere?

#tilføj age at death når vi har den
table_data = data[["Name", "Birthdate", "Deathdate"]] #.unique? no need i would think

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
        )
    ]) #spg: hvorfor skal vi ikke bruge en tom graf

#no callback for now. We can add later if sounds fun. example: filter by year, gender, convert number to stats, search field?

# run the app:

if __name__ == '__main__':
    app.run(debug=False, port=8090)
