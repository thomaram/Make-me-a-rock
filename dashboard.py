# -*- coding: utf-8 -*-
import pickle

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

import pandas as pd
import sklearn


# Imports =====================================================================
# Well coordinates
well_coordinates = pd.read_csv('./Data/xyz_combined.csv', sep=';')

# pickel objects
kmeans_file = open('kmeans_test.pkl', 'rb')
kmeans_obj = pickle.load(kmeans_file)
kmeans_file.close()


# Global constants ============================================================
EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
MAPBOX_TOKEN = 'pk.eyJ1Ijoic3RlZmFuYyIsImEiOiJjanh4OGI4NjMwbG5kM2JrOTBvMnNhMGVwIn0.lbCkgBoY_b96bco9H5sGzw'


# Layout ======================================================================
app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

app.layout = html.Div(children=[

    # row ---------------------------------------------------------------------
    html.Div([
        html.H1('Make me that rock', style={'color': 'white'})
    ], className='row', style={'backgroundColor':'#1f2c56'}),

    # row ---------------------------------------------------------------------
    html.Div([
        # col ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        html.Div([
            html.Div(id='div_map_plot'),
            html.Div([
                html.Div([
                    dcc.RadioItems(
                        id='map_style',
                        options=[
                            {"label": "basic", "value": "basic"},
                            {"label": "satellite", "value": "satellite"},
                            {"label": "outdoors", "value": "outdoors"},
                        ],
                        value='basic',
                        labelStyle={'display': 'inline-block'},                    
                    ),
                ], className='four columns'),
                html.Div(id='selected_coordinates', className='eight columns')
            ], style={'color': 'white'}),
        ], className="nine columns", style={'backgroundColor':'#1f2c56'}),
        # col ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        html.Div([
            dcc.Input(
                id='input_lat',
                type='number',
                placeholder='Latitude'
            ),
            dcc.Input(
                id='input_lon',
                type='number',
                placeholder='Longitude'
            ),
            dcc.Input(
                id='input_depth',
                type='number',
                placeholder='Depth'
            ),
        ], className="three columns", style={'backgroundColor':'#1f2c56'}),
    ], className='row', style={'backgroundColor':'#1f2c56'}),

    # row ---------------------------------------------------------------------
    html.Div([
        html.Div(
            html.H1('More selectors', style={'color': 'white'}),
        ),
    ], className='row', style={'backgroundColor':'grey'}),

    # row ---------------------------------------------------------------------
    html.Div([
        html.Div(
            html.H1('Poro / Perm / PorovsPerm', style={'color': 'white'}),
        ),
    ], className='row', style={'backgroundColor':'steelblue'}), 
])

# Callbacks ===================================================================
@app.callback(
    Output(component_id='div_map_plot', component_property='children'),
    [Input(component_id='map_style', component_property='value'),
     Input(component_id='input_lat', component_property='value'),
     Input(component_id='input_lon', component_property='value')]
)
def update_mapplot(map_style, input_lat, input_lon):

    if map_style:

        data = []

        if input_lat and input_lon:
            print(type(input_lat), input_lon)
            data = [
                {
                    'type': "scattermapbox",
                    'lat': int(input_lat),
                    'lon': int(input_lon),
                    'mode': "markers",
                    'marker': {'size': '14'},
                }
            ]

        else:
            print('Basic')
            new_trace = go.Scattermapbox({
                'lat': 56,
                'lon': 4,
                'mode': 'markers',
                'marker': {"color": 'red', "size": 100}
            }),
            data.append(new_trace)

        layout = {
            'autosize': True,
            'hovermode': "closest",
            'margin': {
                'l': 0,
                'r': 0,
                't': 0,
                'b': 0
            },
            'mapbox': dict(
                accesstoken = MAPBOX_TOKEN,
                bearing = 0,
                center = {
                    'lat': 56.88,
                    'lon': 2.47
                },
                pitch = 0,
                zoom = 10,
                style=map_style,
                layers = []
            )             
        }

        return dcc.Graph(figure={'data': data, 'layout': layout})

@app.callback(
    Output(component_id='selected_coordinates', component_property='children'),
    [Input(component_id='input_lat', component_property='value'),
     Input(component_id='input_lon', component_property='value'),
     Input(component_id='input_depth', component_property='value')]
)
def update_show_coordinates(input_lat, input_lon, input_depth):

    return html.Div([
        html.Div([
            html.P(f'Latitude: {input_lat}')
        ], className="four columns"),
        html.Div([
            html.P(f'Latitude: {input_lon}')
        ], className="four columns"),
        html.Div([
            html.P(f'Depth: {input_depth}')
        ], className="four columns")
    ])


# Server ======================================================================
if __name__ == '__main__':
    app.run_server(debug=True)