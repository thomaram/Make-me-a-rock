import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State


# Global constants ============================================================
MAPBOX_TOKEN = 'pk.eyJ1Ijoic3RlZmFuYyIsImEiOiJjanh4OGI4NjMwbG5kM2JrOTBvMnNhMGVwIn0.lbCkgBoY_b96bco9H5sGzw'


# Layout ======================================================================
app = dash.Dash()

app.layout = html.Div(style={}, children=[
    # Title # 1st row
    html.H1(children='Make me that rock'),
    # Map-Plot and Selector # 2nd row
    html.Div(children=[
        # left column
        html.Div(children=[
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
        ],  style={'width': '60%', 'float': 'left'}),
        # right columns
        html.Div(children=[
            # lat
            # lon
            # depth
        ],  style={'width': '40%', 'float': 'right'}),
    ]), 
])


# Callbacks ===================================================================
@app.callback(
    Output(component_id='div_map_plot', component_property='children'),
    [Input(component_id='map_style', component_property='value')]
)
def update_map_plot(map_style):

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