import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import urllib.request, json
import json
import urllib.request
import requests
from pandas import json_normalize
#######################################################
# Plots json-based covid data time series             #
#######################################################

url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'
response = requests.get(url=url)
if response.status_code == 200:
    data = response.json().get('records')
    df = pd.DataFrame(json_normalize(data))
else:
    print('Error retrieving data from the internet....')

df.columns = ['Date','Day','Month','Year','Daily Cases','Daily Deaths','Country', 'GeoId','Code','Population2019','Continent','14 Day Cases per 100,000']
df = df[['Date','Daily Cases','Daily Deaths','Country', 'Population2019','Continent','14 Day Cases per 100,000']]

external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

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

controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label('Country:'),
                dcc.Dropdown(
                    id='Country',
                    options=[{'label': i, 'value': i} for i in countries_list],
                    value='Austria',
                    style={'color':'black'}
            )

            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('Country:'),
                dcc.Dropdown(
                    id='Statistic',
                    options=[{'label': i, 'value': i} for i in stat],
                    value='Daily Cases',
                    style={'color':'black'}
                )

            ]
        )

    ]
)

app.layout = dbc.Container(
    [
        #html.H1('Worldwide COVID-19 Tracker'),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id='indicator-graphic', config = {'displayModeBar':False}),md=8)
            ],
            align='center',
        ),
    ],
)

'''app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='Country',
                options=[{'label': i, 'value': i} for i in countries_list],
                value='Austria'
            )
        ],
        style={'width': '50%', 'float':'middle','display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='Statistic',
                options=[{'label': i, 'value': i} for i in stat],
                value='Daily Cases'
            )
        ],
        style={'width': '50%', 'float':'middle','display': 'inline-block'}),
    ]),
    dcc.Graph(id='indicator-graphic')
])'''

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
    date_list = filtered_df['Date'].to_list()
    date_list = date_list[::30]
    print(date_list)# Only get every 4th value - we're going to use this for showing fewer tickers
    fig = px.area(filtered_df, x='Date', y=stat, template='plotly_dark')
    fig.update_layout(title_font_family='Arial')
    fig.update_xaxes(tickangle=45, tickfont=dict(family='Arial', size=10))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True)
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=date_list,
            ticktext=date_list
        ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_layout(
        title={
            'text': 'Worldwide COVID-19 Tracker',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    return fig

app.run_server(debug=False
               , use_reloader=False)
