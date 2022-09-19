import plotly.graph_objects as go
import yfinance as yf
from datetime import date
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

colors = {
    'background': '#000000',
    'text': '#000000'
}


stock_range = yf.download('TSLA', start="2017-01-01", end="2017-04-30")
fig = go.Figure(data=go.Scatter(x=stock_range.index, y=stock_range["Close"]))

app = Dash(__name__)
app.layout = html.Div([
    html.Div([
    html.H1(children='Stocks',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
                ),

    html.Div(children='''
        Input a stock index
    ''', style={'textAlign': 'center', 'color': colors['text']}),
            "Stock ticker: ",
            dcc.Input(id='my-input', value='TSLA', type='text')
        ]),
    html.Br(),
    dcc.DatePickerRange(
            id='my-date-picker-range',
            month_format='YYYY MM DD',
            initial_visible_month=date(2022, 8, 5),
        ),
    html.Br(),
    html.Div(id='output-container-date-picker-range'),
    html.Br(),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input(component_id='my-input', component_property='value')

)
def update_output_div(start_date, end_date, my_input):
    stock = str(my_input)
    print(stock)
    stock_range = yf.download(stock, start=start_date, end=end_date)
    fig = go.Figure(data=go.Scatter(x=stock_range.index, y=stock_range["Close"]))
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)

