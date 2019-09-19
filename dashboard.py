# -*- coding: utf-8 -*-
import pickle

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import plotly.express as px

import pandas as pd
import sklearn


# Imports =====================================================================
# Well coordinates
well_coordinates = pd.read_csv('./Data/xyz_combined.csv', sep=';')
print(well_coordinates.columns)

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
        ], className="nine columns", style={'backgroundColor':'#1f2c56', 'padding': 10}),
        # col ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        html.Div([
            html.Div([
                dcc.Input(
                    id='input_lat',
                    type='number',
                    placeholder='Latitude'
                ),
            ], className='row'),
            html.Div([
                dcc.Input(
                    id='input_lon',
                    type='number',
                    placeholder='Longitude'
                ),                
            ], className='row'),
            html.Div([
                dcc.Input(
                    id='input_depth',
                    type='number',
                    placeholder='Depth'
                ),                
            ], className='row'),
        ], className="two columns", style={'backgroundColor':'#1f2c56'}),
    ], className='row', style={'backgroundColor':'#1f2c56'}),

    # row ---------------------------------------------------------------------
    html.Div([
        html.Div(
            html.Div(id='porr_perm_plot'),
        ),
    ], className='row', style={'backgroundColor':'#1f2c56', 'padding': 10}), 
], style={"max-width": "1200px", "margin": "auto", 'backgroundColor':'white'})

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
            new_trace = go.Scattermapbox(
                lat=[f'{input_lat}'],
                lon=[f'{input_lon}'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=14
                ),
                text=['Montreal'],
            )
            data.append(new_trace)

        else:
            new_trace = go.Scattermapbox(
                lat=['56.88'],
                lon=['2.47'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=14
                ),
                text=['Montreal'],
            )
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
                zoom = 5,
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

@app.callback(
    Output(component_id='porr_perm_plot', component_property='children'),
    [Input(component_id='input_lat', component_property='value'),
     Input(component_id='input_lon', component_property='value'),
     Input(component_id='input_depth', component_property='value')]
)
def update_poro_perm_plot(input_lat, input_lon, input_depth):

    print(input_lat, input_lon, input_depth)

    # Todo: replace with appropriate function => kmeans
    df = well_coordinates

    fig_poro = px.scatter(
        df,
        x='coor_ns',
        y='coor_ew',
        marginal_y="violin"
    )

    fig_perm = px.scatter(
        df,
        x='coor_ew',
        y='coor_ns',
        marginal_y="violin"
    )

    return [
        html.Div([
            dcc.Graph(figure=fig_poro)
        ], className="six columns"),
        html.Div([
            dcc.Graph(figure=fig_perm)
        ], className="six columns"),
    ]


# Server ======================================================================
if __name__ == '__main__':
    app.run_server(debug=True)