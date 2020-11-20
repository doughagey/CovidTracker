import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import urllib.request, json
import json
import urllib.request
import requests
from pandas import json_normalize
#######################################################
# Plots json-based covid data in plotly via a wind rose chart #
#######################################################
'''with urllib.request.urlopen('https://opendata.ecdc.europa.eu/covid19/casedistribution/json/') as url:
    data = json.loads(url.read().decode())
    df = pd.DataFrame(json_normalize(data, 'records'))'''

url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'
response = requests.get(url=url)
if response.status_code == 200:
    data = response.json().get('records')
    df = pd.DataFrame(json_normalize(data))
else:
    pass

df.columns = ['Date','Day','Month','Year','Daily Cases','Daily Deaths','Country', 'GeoId','Code','Population2019','Continent','14 Day Cases per 100,000']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#####################################################################################
# Plot using a simple standard plotly express wind rose chart as it includes default styling
#####################################################################################

# Build the Dash app and deploy
continents = df['Continent'].unique()
continents_list = continents.tolist()
continents_list = sorted(continents_list)
countries = df['Country'].unique()
countries_list = countries.tolist()
countries_list = sorted(countries_list)
stat = ['Daily Cases','Daily Deaths','14 Day Cases per 100,000']

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='Country',
                options=[{'label': i, 'value': i} for i in countries_list],
                value='Austria'
            )
        ],
        style={'width': '34%', 'float':'middle','display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='Statistic',
                options=[{'label': i, 'value': i} for i in stat],
                value='cases'
            )
        ],
        style={'width': '34%', 'float':'middle','display': 'inline-block'}),
    ]),
    dcc.Graph(id='indicator-graphic')
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('Country', 'value'),
     Input('Statistic', 'value',)])

def update_graph(country, stat):
    filtered_df = df.loc[df['Country']==country]
    #filtered_df['dateRep']= pd.to_datetime(filtered_df['dateRep'])
    #filtered_df = filtered_df.sort_values(['countriesAndTerritories', "dateRep"], ascending = (True, True))
    #filtered_df = filtered_df.reset_index(drop=True) # reset index or it screws the graph up
    filtered_df = filtered_df[::-1]  # without this the graph is backwards
    fig = px.area(filtered_df, x='Date', y=stat)
    return fig

app.run_server(debug=False
               , use_reloader=False)
