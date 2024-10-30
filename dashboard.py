import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

# Load the data
csv_path = '../dummy_sample.csv'
data = pd.read_csv(csv_path)

# Initialize the Dash app with a Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the dashboard
app.layout = dbc.Container([
    html.H1("Investment and Emissions Dashboard", className="text-center my-4"),
    
    dbc.Tabs([
        dbc.Tab(label="Fund Size", tab_id="tab-fund-size", children=[
            dbc.Container([
                html.H2("Fund Size by Fund Type", className="text-center mt-4"),
                dcc.Graph(id='fund-size-chart'),
            ])
        ]),
        
        dbc.Tab(label="Investment Distribution", tab_id="tab-investment-distribution", children=[
            dbc.Container([
                html.H2("Investment Distribution by Company", className="text-center mt-4"),
                dcc.Graph(id='investment-distribution'),
            ])
        ]),
        
        dbc.Tab(label="Emissions", tab_id="tab-emissions", children=[
            dbc.Container([
                html.H2("Total Emissions by Fund", className="text-center mt-4"),
                dcc.Graph(id='emissions-chart'),
                html.Label("Select Emission Scope:", className="mt-3"),
                dcc.Dropdown(
                    id='scope-dropdown',
                    options=[
                        {'label': 'Total Emissions', 'value': 'Total Emissions by Fund (tons of CO2e)'},
                        {'label': 'Scope 1', 'value': 'Scope 1 Emissions (tons of CO2e)'},
                        {'label': 'Scope 2', 'value': 'Scope 2 Emissions (tons of CO2e)'},
                        {'label': 'Scope 3', 'value': 'Scope 3 Emissions (tons of CO2e)'}
                    ],
                    value='Total Emissions by Fund (tons of CO2e)',
                    clearable=False
                )
            ])
        ])
    ], id="tabs", active_tab="tab-fund-size", className="my-4"),
], fluid=True)

# Callback to update fund size chart
@app.callback(
    Output('fund-size-chart', 'figure'),
    Input('scope-dropdown', 'value')
)
def update_fund_size_chart(selected_scope):
    fig = px.bar(
        data, x='Fund', y='Fund Size ($M)', color='Fund',
        title="Fund Size by Fund Type",
        template="plotly_white"
    )
    fig.update_layout(showlegend=False)
    return fig

# Callback to update investment distribution chart
@app.callback(
    Output('investment-distribution', 'figure'),
    Input('scope-dropdown', 'value')
)
def update_investment_distribution(selected_scope):
    fig = px.pie(
        data, values='Investment ($M)', names='Company Name',
        title="Investment Distribution by Company",
        template="plotly_white",
        hole=0.3  # Adds a donut style
    )
    fig.update_traces(textinfo='percent+label')
    return fig

# Callback to update emissions chart based on scope
@app.callback(
    Output('emissions-chart', 'figure'),
    Input('scope-dropdown', 'value')
)
def update_emissions_chart(selected_scope):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data['Fund'],
        y=data[selected_scope],
        marker=dict(color='lightsalmon'),
        name=selected_scope
    ))
    fig.update_layout(
        title=f"{selected_scope} by Fund",
        xaxis_title="Fund",
        yaxis_title="Emissions (tons of CO2e)",
        template="plotly_white"
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
