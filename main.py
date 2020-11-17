import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import urllib.request


# update data from European Centre for Disease Prevention and Control
print("start update...")
url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/data.csv'
output = f'data/update_data.csv'
urllib.request.urlretrieve(url, output)
print(f"File {output} -- saved...")


# get all COVID data from the United States
covid_data = pd.read_csv('data/update_data.csv')
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
    html.Div([
        html.P(["US COVID-19 Data by Month (2020)"])
    ], style={'textAlign': 'center', 'fontSize': '50px', 'fontFamily': '"Lucid Console", Courier, monospace'}),
    html.Div([
        html.P(["Deaths per Month"], style={'fontSize': '20px'}),
        dcc.Graph(figure=fig_deaths)
    ], style={'fontFamily': '"Lucid Console", Courier, monospace'}),
    html.Div([
        html.Hr([], style={'width': '100%', 'height': '50px', 'visibility': 'hidden'}),
        html.P(["Cases per Month"], style={'fontSize': '20px'}),
        dcc.Graph(figure=fig_cases)
    ], style={'fontFamily': '"Lucid Console", Courier, monospace'}),
    html.Div([
        html.Hr([], style={'width': '100%', 'height': '50px', 'visibility': 'hidden'}),
        html.P(["Cases vs Deaths per Month"], style={'fontSize': '20px'}),
        dcc.Graph(figure=fig_monthly_cases_and_deaths_comparison)
    ], style={'fontFamily': '"Lucid Console", Courier, monospace'}),

], style={'width': '60%', 'height': '100%', 'margin': 'auto'})

app.run_server(debug=True, use_reloader=False)
