import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)

# Load the data
spacex_df = pd.read_csv('spacex_launch_dash.csv')

# Find the minimum and maximum payload values
min_payload = spacex_df['PayloadMass'].min()
max_payload = spacex_df['PayloadMass'].max()


dcc.Dropdown(
    id='site-dropdown',
    options=[
        {'label': 'All Sites', 'value': 'ALL'},
        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
    ],
    value='ALL',
    placeholder="Select a Launch Site here",
    searchable=True
)

dcc.RangeSlider(
    id='payload-slider',
    min=0,
    max=10000,
    step=1000,
    value=[min_payload, max_payload]
)

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', title=f'Success vs Failure for {entered_site}')
        return fig


@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['PayloadMass'] > low) & (spacex_df['PayloadMass'] < high)
    
    if entered_site == 'ALL':
        fig = px.scatter(
            spacex_df[mask], 
            x="PayloadMass", 
            y="class", 
            color="Booster Version Category",
            title="Payload vs. Outcome for All Sites"
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.scatter(
            filtered_df[mask], 
            x="PayloadMass", 
            y="class", 
            color="Booster Version Category",
            title=f"Payload vs. Outcome for {entered_site}"
        )
    
    return fig