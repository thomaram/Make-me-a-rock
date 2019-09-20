# -*- coding: utf-8 -*-
import pickle

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.figure_factory as ff

import pandas as pd
import sklearn
import numpy as np
from sklearn import linear_model
import kmodes


# Imports =====================================================================
# Well coordinates
well_coordinates = pd.read_csv('./Data/xyz_combined.csv', sep=';')
print(well_coordinates.columns)

# pickel objects
kmeans_file = open('kmeans_test.pkl', 'rb')
kmeans_obj = pickle.load(kmeans_file)
kmeans_file.close()


# Model processing on init ====================================================
# Hardcoded variables
keepColumns=['md', 'kh_kl_log', 'kv_kl_log', 'phi_best', 'clean_litho',
       'grain_density', 'grain_size', 'sorting', 'cement', 'wellbore_y',
       'formation']


# Read and process inputdata from file
inputdata_df = pd.read_csv('./Data/second_batch.csv')

inputdata_df['kh_kl_log'] = np.log10(inputdata_df['kh_kl'])
inputdata_df['kv_kl_log'] = np.log10(inputdata_df['kv_kl'])


# Read and process inputdata from file
inputdata_df = pd.read_csv('./Data/second_batch.csv')

inputdata_df['kh_kl_log'] = np.log10(inputdata_df['kh_kl'])
inputdata_df['kv_kl_log'] = np.log10(inputdata_df['kv_kl'])


# Load fkmodes
kmodes_file = open('kmodes_5clusters.pkl', 'rb')
kmodes_obj = pickle.load(kmodes_file)
kmodes_file.close()


# Update inputdata_df
inputdata_df['cluster'] = kmodes_obj.predict(inputdata_df[keepColumns])


# Dict of filenames
regr_kh_kl_clusters_names = [
    'regr__kh_kl_log__cluster1.pkl',
    'regr__kh_kl_log__cluster2.pkl',
    'regr__kh_kl_log__cluster3.pkl',
    'regr__kh_kl_log__cluster4.pkl',
]

regr_phi_best_cluster_names = [
    'regr__phi_best__cluster0.pkl',
    'regr__phi_best__cluster1.pkl',
    'regr__phi_best__cluster2.pkl',
    'regr__phi_best__cluster3.pkl',
    'regr__phi_best__cluster4.pkl',
]


# Read files from harddrive to memory
regr_kh_kl={}
for i, c in enumerate(regr_kh_kl_clusters_names):
    
    file_i = open(c, 'rb')
    regr_kh_kl[i] = pickle.load(file_i)
    file_i.close()
    
regr_phi_best={}
for i, c in enumerate(regr_phi_best_cluster_names):
    
    file_i = open(c, 'rb')
    regr_phi_best[i] = pickle.load(file_i)
    file_i.close()


# Unique vals
md_vals = inputdata_df['md'].unique()
kh_kl_log_vals = inputdata_df['kh_kl_log'].unique()
phi_best_vals = inputdata_df['phi_best'].unique()
clean_litho_vals = inputdata_df['clean_litho'].unique()
grain_density_vals = inputdata_df['grain_density'].unique()
grain_size_vals = inputdata_df['grain_size'].unique()
sorting_vals = inputdata_df['sorting'].unique()
cement_vals = inputdata_df['cement'].unique()
wellbore_y_vals = inputdata_df['wellbore_y'].unique()
formation_vals = inputdata_df['formation'].unique()


# Global constants ============================================================
EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
MAPBOX_TOKEN = 'pk.eyJ1Ijoic3RlZmFuYyIsImEiOiJjanh4OGI4NjMwbG5kM2JrOTBvMnNhMGVwIn0.lbCkgBoY_b96bco9H5sGzw'


# Layout ======================================================================
app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

app.layout = html.Div(children=[

    # row ---------------------------------------------------------------------
    html.Div([
        html.H1('Make me that rock', style={'color': 'black'})
    ], className='row', style={'backgroundColor':'white', 'padding': 10}),

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
                        value='satellite',
                        labelStyle={'display': 'inline-block'},                    
                    ),
                ], className='four columns'),
                html.Div([
                    dcc.Checklist(
                        id='checkbox_show_wells',
                        options=[
                            {'label': 'Show Wells', 'value': 'show_wells'}
                        ],
                        value=[],
                    ),
                ], className='two columns'),
                html.Div(id='selected_coordinates', className='six columns'),
            ], style={'color': 'black'}),
        ], className="nine columns", style={'backgroundColor':'white', 'padding': 10}),
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
                    placeholder='Depth',
                ),                
            ], className='row'),
            html.Div([
                dcc.Dropdown(
                    id='input_md',
                    placeholder='md',
                    options=[{'label': i, 'value': i } for i in md_vals],
                    value=md_vals[0]
                ),                
            ], className='row'),
            html.Div([
                dcc.Dropdown(
                    id='input_kh_kl_log',
                    placeholder='kh_kl_log',
                    options=[{'label': i, 'value': i } for i in kh_kl_log_vals],
                    value=kh_kl_log_vals[0]
                ),                
            ], className='row'),
            html.Div([
                dcc.Dropdown(
                    id='input_phi_best',
                    placeholder='phi_best',
                    options=[{'label': i, 'value': i } for i in phi_best_vals],
                    value=phi_best_vals[0]
                ),                
            ], className='row'),
            html.Div([
                dcc.Dropdown(
                    id='input_clean_litho',
                    placeholder='clean_litho',
                    options=[{'label': i, 'value': i } for i in clean_litho_vals],
                    value=clean_litho_vals[0]
                ),                
            ], className='row'),
            html.Div([
                dcc.Dropdown(
                    id='input_grain_density',
                    placeholder='grain_density',
                    options=[{'label': i, 'value': i } for i in grain_density_vals],
                    value=grain_density_vals[0]
                ),                
            ], className='row'),
            html.Div([
                dcc.Dropdown(
                    id='input_grain_size',
                    placeholder='grain_size',
                    options=[{'label': i, 'value': i } for i in grain_size_vals],
                    value=grain_size_vals[0]
                ),                
            ], className='row'),
            html.Div([
                dcc.Dropdown(
                    id='input_sorting',
                    placeholder='sorting',
                    options=[{'label': i, 'value': i } for i in sorting_vals],
                    value=sorting_vals[0]
                ),                
            ], className='row'),
            html.Div([
                dcc.Dropdown(
                    id='input_cement',
                    placeholder='cement',
                    options=[{'label': i, 'value': i } for i in cement_vals],
                    value=cement_vals[0]
                ),                
            ], className='row'),
            html.Div([
                dcc.Dropdown(
                    id='input_wellbore_y',
                    placeholder='wellbore_y',
                    options=[{'label': i, 'value': i } for i in wellbore_y_vals],
                    value=wellbore_y_vals[0]
                ),                
            ], className='row'),
            html.Div([
                dcc.Dropdown(
                    id='input_formation',
                    placeholder='formation',
                    options=[{'label': i, 'value': i } for i in formation_vals],
                    value=formation_vals[0]
                ),                
            ], className='row'),
        ], className="two columns", style={'backgroundColor':'white', 'padding': 10}),
    ], className='row', style={'backgroundColor':'white'}),

    # row ---------------------------------------------------------------------
    html.Div([
        html.Div(
            html.Div(id='porr_perm_plot'),
        ),
    ], className='row', style={'backgroundColor':'white', 'padding': 10}), 
], style={"max-width": "1200px", "margin": "auto", 'backgroundColor':'black'})

# Callbacks ===================================================================
@app.callback(
    Output(component_id='div_map_plot', component_property='children'),
    [Input(component_id='map_style', component_property='value'),
     Input(component_id='input_lat', component_property='value'),
     Input(component_id='input_lon', component_property='value'),
     Input(component_id='checkbox_show_wells', component_property='value'),]
)
def update_mapplot(map_style, input_lat, input_lon, checkbox_show_wells):

    if map_style:

        data = []

        if input_lat and input_lon:
            new_trace = go.Scattermapbox(
                lat=[f'{input_lat}'],
                lon=[f'{input_lon}'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=10,
                    color='#FF4500',
                ),
                name='Selected point',
            )
            data.append(new_trace)

        else:
            new_trace = go.Scattermapbox(
                lat=['56.88'],
                lon=['2.47'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=0.1,
                    color='blue',
                ),
                text=['Montreal'],
                showlegend=False,
            )
            data.append(new_trace)

        if 'show_wells' in checkbox_show_wells:

            well_traces = go.Scattermapbox(
                lat=well_coordinates['coor_ns'],
                lon=well_coordinates['coor_ew'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=2,
                    color='#FFA500',
                ),
                name='Wells',
            )
            data.append(well_traces)

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
                    'lat': 60,
                    'lon': 3
                },
                pitch = 0,
                zoom = 5,
                style=map_style,
                layers = []
            ),
            'legend': go.layout.Legend(
                x=0,
                y=1,
                traceorder="normal",
                font=dict(
                    family="sans-serif",
                    size=12,
                    color="black"
                ),
                bgcolor="LightSteelBlue",
                bordercolor="Black",
                borderwidth=2
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
            html.P(f'Longitude: {input_lon}')
        ], className="four columns"),
        html.Div([
            html.P(f'Depth: {input_depth}')
        ], className="four columns")
    ])

@app.callback(
    Output(component_id='porr_perm_plot', component_property='children'),
    [Input(component_id='input_lat', component_property='value'),
     Input(component_id='input_lon', component_property='value'),
     Input(component_id='input_depth', component_property='value'),
     Input(component_id='input_md', component_property='value'),
     Input(component_id='input_kh_kl_log', component_property='value'),
     Input(component_id='input_phi_best', component_property='value'),
     Input(component_id='input_clean_litho', component_property='value'),
     Input(component_id='input_grain_density', component_property='value'),
     Input(component_id='input_grain_size', component_property='value'),
     Input(component_id='input_sorting', component_property='value'),
     Input(component_id='input_cement', component_property='value'),
     Input(component_id='input_wellbore_y', component_property='value'),
     Input(component_id='input_formation', component_property='value')]
)
def update_poro_perm_plot(
        input_lat,
        input_lon,
        input_depth,
        md,
        kh_kl_log,
        phi_best,
        clean_litho,
        grain_density,
        grain_size,
        sorting,
        cement,
        wellbore_y,
        formation
    ):

    

    # Todo: replace with appropriate function => kmeans
    df = well_coordinates

    _fig_poro = px.scatter(
        df,
        x='coor_ns',
        y='coor_ew',
        #marginal_y="violin",
        title='Porosity',
        template='plotly_dark',
    )

    fig_perm = px.scatter(
        df,
        x='coor_ew',
        y='coor_ns',
        #marginal_y="violin",
        title='Permeability',
        template='plotly_dark'
    )

    s_poro = np.random.normal(0.23, 0.1, 1000)
    s_perm = np.random.normal(823, 0.1, 1000)

    hist_data_poro = [s_poro]
    group_labels_poro = ['Porosity']
    fig_poro = ff.create_distplot(
        hist_data_poro,
        group_labels_poro,
        show_hist=False
    )

    hist_data_perm = [s_perm]
    group_labels_perm = ['Permeability']
    fig_perm = ff.create_distplot(
        hist_data_perm,
        group_labels_perm,
        show_hist=False
    )

    fig_poro = ff.create_distplot(
        hist_data_poro,
        group_labels_poro,
        show_hist=False
    )

    fig_perm = ff.create_distplot(
        hist_data_perm,
        group_labels_perm,
        show_hist=False
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