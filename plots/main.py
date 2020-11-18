import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import urllib.request
from dash.dependencies import Output, Input


# update datasets from European Centre for Disease Prevention and Control
print("start update...")
url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/data.csv'
output = f'../datasets/update_data.csv'
urllib.request.urlretrieve(url, output)
print("update finished!")
print(f"File {output} -- saved...")


# get all COVID datasets from the United States
covid_data = pd.read_csv('../datasets/update_data.csv')
united_states_data = covid_data[covid_data.countriesAndTerritories == 'United_States_of_America']
new_data = pd.DataFrame(united_states_data)


# get COVID deaths per month
monthly_deaths = new_data.groupby('month', as_index=False).deaths.sum()
fig_deaths = go.Figure()

dates = pd.date_range('2020-01', '2020-12', freq='MS')
fig_deaths.layout.xaxis.tickvals = pd.date_range('2020-01', '2020-12', freq='MS')
fig_deaths.layout.xaxis.tickformat = '%b'

fig_deaths.add_trace(
    go.Bar(x=dates, y=monthly_deaths['deaths'])
)

fig_deaths.update_layout(
    margin=dict(l=25, r=25, t=25, b=25),
    paper_bgcolor="LightSteelBlue",
    plot_bgcolor="LightSteelBlue"
)

fig_deaths.update_traces(
    marker_color='#ED553C'
)


# get COVID cases per month
monthly_cases = new_data.groupby('month', as_index=False).cases.sum()
fig_cases = go.Figure()

fig_cases.layout.xaxis.tickvals = pd.date_range('2020-01', '2020-12', freq='MS')
fig_cases.layout.xaxis.tickformat = '%b'

fig_cases.add_trace(
    go.Bar(x=dates, y=monthly_cases['cases'])
)

fig_cases.update_layout(
    margin=dict(l=25, r=25, t=25, b=25),
    paper_bgcolor="LightSteelBlue",
    plot_bgcolor="LightSteelBlue"
)

fig_cases.update_traces(
    marker_color='#636FF4'
)


# compare cases to deaths per month
fig_monthly_cases_and_deaths_comparison = go.Figure(data=[
    go.Bar(x=dates, y=monthly_cases['cases'], name="cases"),
    go.Bar(x=dates, y=monthly_deaths['deaths'], name="deaths")
])

fig_monthly_cases_and_deaths_comparison.layout.xaxis.tickvals = pd.date_range('2020-01', '2020-12', freq='MS')
fig_monthly_cases_and_deaths_comparison.layout.xaxis.tickformat = '%b'

fig_monthly_cases_and_deaths_comparison.update_layout(
    margin=dict(l=25, r=25, t=25, b=25),
    paper_bgcolor="LightSteelBlue",
    plot_bgcolor="LightSteelBlue"
)


# setup layout and server
app = dash.Dash()

app.layout = html.Div([
    html.Div(
        [
            html.Div([
                html.Header(
                    ["2020 US COVID-19 Data"],
                    style={'textAlign': 'center', 'fontSize': '50px',
                           'fontFamily': '"Lucid Console", Courier, monospace', 'borderBottom': '1px solid #B0C4DE'}
                ),
                html.P(
                    [
                        "All COVID-19 datasets is retrieved from the ECDC (European Centre for Disease Prevention and Control). "
                        "The datasets can be accessed on their website here: https://www.ecdc.europa.eu/en/publications-data "],
                    style={'textAlign': 'left', 'fontSize': '25px', 'fontFamily': '"Lucid Console", Courier, monospace',
                           'width': '1200px', 'margin': 'auto', 'marginTop': '40px'}
                ),
                html.Hr([], style={'width': '100%', 'height': '30px', 'visibility': 'hidden'}),
                html.Hr([], style={'width': '100%', 'border': '0', 'borderTop': '1px solid #B0C4DE'})

            ], style={}),

            # Data
            html.Div([
                html.Div([
                    # deaths
                    html.P(["Deaths per Month"], style={'fontSize': '20px'}),
                    dcc.Dropdown(
                        id='dropdown-menu-death',
                        options=[
                            {'label': 'Bar Graph', 'value': 'Bar'},
                            {'label': 'Line Graph', 'value': 'Line'},
                        ],
                        value='Bar',
                        style={'width': '200px'}
                    ),
                    dcc.Graph(figure=fig_deaths, id="death_graph"),
                ], style={'fontFamily': '"Lucid Console", Courier, monospace', 'width': '575px', 'float': 'left',
                          'marginRight': '50px'}),
                html.Div([
                    html.P(["Cases per Month"], style={'fontSize': '20px'}),
                    dcc.Dropdown(
                        id='dropdown-menu-case',
                        options=[
                            {'label': 'Bar Graph', 'value': 'Bar'},
                            {'label': 'Line Graph', 'value': 'Line'},
                        ],
                        value='Bar',
                        style={'width': '200px'}
                    ),
                    dcc.Graph(figure=fig_cases, id="case_graph")
                ], style={'fontFamily': '"Lucid Console", Courier, monospace', 'width': '575px', 'float': 'left'}),
                html.Div([
                    html.Hr([], style={'width': '100%', 'height': '50px', 'visibility': 'hidden'}),
                    html.P(["Cases vs Deaths per Month"], style={'fontSize': '20px'}),
                    dcc.Dropdown(
                        id='dropdown-menu-case-and-death',
                        options=[
                            {'label': 'Bar Graph', 'value': 'Bar'},
                            {'label': 'Line Graph', 'value': 'Line'},
                        ],
                        value='Bar',
                        style={'width': '200px'}
                    ),
                    dcc.Graph(figure=fig_monthly_cases_and_deaths_comparison, id="case_death_graph")
                ], style={'fontFamily': '"Lucid Console", Courier, monospace', 'width': '1200px'}),
            ], style={'width': '1200px', 'margin': 'auto'}),
        ], style={'width': '1350px', 'height': '100%', 'margin': 'auto', 'background': '#F5F5F5',
                  'border': '1px solid #B0C4DE'}
    )

], style={'width': '100%', 'height': '100%', 'margin': 'auto', 'background': '#F5F5F5'})


@app.callback(
    Output('death_graph', 'figure'),
    [Input('dropdown-menu-death', 'value')])
def update_output(value):
    if value == 'Line':
        new_fig = go.Figure()
        new_fig.layout.xaxis.tickvals = pd.date_range('2020-01', '2020-12', freq='MS')
        new_fig.layout.xaxis.tickformat = '%b'
        new_fig.add_trace(
            go.Scatter(x=dates, y=monthly_deaths['deaths'])
        )
        new_fig.update_layout(
            margin=dict(l=25, r=25, t=25, b=25),
            paper_bgcolor="LightSteelBlue",
            plot_bgcolor="LightSteelBlue"
        )
        new_fig.update_traces(
            marker_color='#ED553C'
        )
    else:
        new_fig = go.Figure()
        new_fig.layout.xaxis.tickvals = pd.date_range('2020-01', '2020-12', freq='MS')
        new_fig.layout.xaxis.tickformat = '%b'
        new_fig.add_trace(
            go.Bar(x=dates, y=monthly_deaths['deaths'])
        )
        new_fig.update_layout(
            margin=dict(l=25, r=25, t=25, b=25),
            paper_bgcolor="LightSteelBlue",
            plot_bgcolor="LightSteelBlue"
        )
        new_fig.update_traces(
            marker_color='#ED553C'
        )
    return new_fig


@app.callback(
    Output('case_graph', 'figure'),
    [Input('dropdown-menu-case', 'value')])
def update_output(value):
    if value == 'Line':
        new_fig = go.Figure()
        new_fig.layout.xaxis.tickvals = pd.date_range('2020-01', '2020-12', freq='MS')
        new_fig.layout.xaxis.tickformat = '%b'
        new_fig.add_trace(
            go.Scatter(x=dates, y=monthly_cases['cases'])
        )
        new_fig.update_layout(
            margin=dict(l=25, r=25, t=25, b=25),
            paper_bgcolor="LightSteelBlue",
            plot_bgcolor="LightSteelBlue"
        )
        new_fig.update_traces(
            marker_color='#636FF4'
        )
    else:
        new_fig = go.Figure()
        new_fig.layout.xaxis.tickvals = pd.date_range('2020-01', '2020-12', freq='MS')
        new_fig.layout.xaxis.tickformat = '%b'
        new_fig.add_trace(
            go.Bar(x=dates, y=monthly_cases['cases'])
        )
        new_fig.update_layout(
            margin=dict(l=25, r=25, t=25, b=25),
            paper_bgcolor="LightSteelBlue",
            plot_bgcolor="LightSteelBlue"
        )
        new_fig.update_traces(
            marker_color='#636FF4'
        )
    return new_fig


@app.callback(
    Output('case_death_graph', 'figure'),
    [Input('dropdown-menu-case-and-death', 'value')])
def update_output(value):
    if value == 'Line':
        new_fig = go.Figure(
            data=[
                go.Scatter(x=dates, y=monthly_cases['cases'], name="cases"),
                go.Scatter(x=dates, y=monthly_deaths['deaths'], name="deaths")
            ]
        )
        new_fig.layout.xaxis.tickvals = pd.date_range('2020-01', '2020-12', freq='MS')
        new_fig.layout.xaxis.tickformat = '%b'
        new_fig.update_layout(
            margin=dict(l=25, r=25, t=25, b=25),
            paper_bgcolor="LightSteelBlue",
            plot_bgcolor="LightSteelBlue"
        )
    else:
        new_fig = go.Figure(
            data=[
                go.Bar(x=dates, y=monthly_cases['cases'], name="cases"),
                go.Bar(x=dates, y=monthly_deaths['deaths'], name="deaths")
            ])
        new_fig.layout.xaxis.tickvals = pd.date_range('2020-01', '2020-12', freq='MS')
        new_fig.layout.xaxis.tickformat = '%b'

        new_fig.update_layout(
            margin=dict(l=25, r=25, t=25, b=25),
            paper_bgcolor="LightSteelBlue",
            plot_bgcolor="LightSteelBlue"
        )
    return new_fig


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
