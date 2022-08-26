# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from dash import Dash, Input, Output, dcc, html

app = Dash(__name__)
colors = {
    'background': '#000000',
    'text': '#000000'
}

tsla = yf.Ticker("TSLA")
# info = tsla.info
tsla_data = tsla.history(period='1y')
fig = go.Figure(data=go.Scatter(x=tsla_data.index, y=tsla_data["Close"]))




app.layout = html.Div(children=[
    html.H1(children='Stocks',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
            ),

    html.Div(children='''
        Input a stock index
    ''', style={'textAlign': 'center', 'color': colors['text']}),
html.Div([
        "Stock ticker: ",
        dcc.Input(id='my-input', value='initial value', type='text')
    ]),
    html.Br(),
    html.Div(id='my-output'),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    Input(component_id='my-input', component_property='value'),
)

def update_output_div(input_value):
    tsla = yf.Ticker(input_value)
    tsla_data = tsla.history(period='1y')
    fig = go.Figure(data=go.Scatter(x=tsla_data.index, y=tsla_data["Close"]))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
