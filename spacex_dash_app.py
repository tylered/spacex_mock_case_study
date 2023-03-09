# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read the airline data into pandas dataframe
# spacex_df = pd.read_csv("spacex_launch_dash.csv")

spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
start = (max_payload - min_payload) / 2

# dropdown site options
site_labels = [{'label': 'All sites', 'value': 'None'}]
site_labels.extend([{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()])


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                             options=site_labels,
                                             placeholder='Select launch site:',
                                             value='None'),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=min_payload, max=max_payload, step=1000, value=[0, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def update(ste):

    if ste == 'None':
        new_df = spacex_df.groupby(['Launch Site']).sum(numeric_only=True).reset_index()
        fig = px.pie(new_df, names='Launch Site', values='class', title='Success Percentage')
        return fig

    x = spacex_df[spacex_df['Launch Site'] == ste]
    fig = px.pie(x, names='class', title='Success Percentage')
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='payload-slider', component_property='value'),
              Input(component_id='site-dropdown', component_property='value')
              )
def scatter(value, value1):
    x = spacex_df[spacex_df['Payload Mass (kg)'].between(value[0], value[1])]
    if value1 == 'None':
        fig = px.scatter(x, x='Payload Mass (kg)', y='class', title='Paylaod vs Success Rate', color="Booster Version Category")
        return fig
    x = x[spacex_df['Launch Site'] == value1]
    fig = px.scatter(x, x='Payload Mass (kg)', y='class', title='Paylaod vs Success Rate', color="Booster Version Category")
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
