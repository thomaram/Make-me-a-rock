# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html


# Global constants ============================================================
EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


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
            html.H1('Map', style={'color': 'white'})
        ],  className="eight columns", style={'backgroundColor':'orange'}),
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

    # row 
    html.Div([
        html.Div(
            html.H1('Poro / Perm / PorovsPerm', style={'color': 'white'}),
        ),
    ], className='row', style={'backgroundColor':'steelblue'}), 
])

# Server ======================================================================
if __name__ == '__main__':
    app.run_server(debug=True)