# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State


# Global constants ============================================================
EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
MAPBOX_TOKEN = 'pk.eyJ1Ijoic3RlZmFuYyIsImEiOiJjanh4OGI4NjMwbG5kM2JrOTBvMnNhMGVwIn0.lbCkgBoY_b96bco9H5sGzw'


# Layout ======================================================================
app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

app.layout = html.Div(children=[

    # row -------------------------------------------------------------------
    html.Div([
        html.H1('Make me that rock', style={'color': 'white'})
    ], className='row', style={'backgroundColor':'#1f2c56'}),

    # row -------------------------------------------------------------------
    html.Div([
        # col
        html.Div([
            html.Div(id='div_map_plot'),
            dcc.RadioItems(
                id='map_style',
                options=[
                    {"label": "basic", "value": "basic"},
                    {"label": "satellite", "value": "satellite"},
                    {"label": "outdoors", "value": "outdoors"},
                ],
                value='basic',
                labelStyle={'display': 'inline-block'}
            ),
        ],  className="eight columns", style={'backgroundColor':'#1f2c56'}),
        # col
        html.Div([
            html.H1('Selectors', style={'color': 'white'})
        ],  className="four columns", style={'backgroundColor':'yellow'}),
    ], className='row', style={'backgroundColor':'blue'}),

    # row 
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
    [Input(component_id='map_style', component_property='value')]
)
def update_mapplot(map_style):

    if map_style:

        data = [
            {
                'type': "scattermapbox",
                'lat': 38.30,
                'lon': -90.68,
                'mode': "markers",
                'marker': {'size': '14'},
            }
        ]

        layout = {
            'autosize': True,
            'hovermode': "closest",
            'margin': dict(l = 0, r = 0, t = 0, b = 0),
            'mapbox': dict(
                accesstoken = MAPBOX_TOKEN,
                bearing = 0,
                center = dict(lat = 56.88, lon = 2.47),
                pitch = 0,
                zoom = 5,
                style=map_style,
                layers = []
            )             
        }

        return dcc.Graph(figure={'data': data, 'layout': layout})

# Server ======================================================================
if __name__ == '__main__':
    app.run_server(debug=True)