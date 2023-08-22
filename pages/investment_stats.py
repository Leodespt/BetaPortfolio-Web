import dash
from dash import html, dash_table, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
# Import Transaction data
import TransactionData as T

# String to Datetime
from dateutil.parser import parse
import requests

# Formating of the thousand values
import locale
locale.setlocale(locale.LC_ALL, '')

dash.register_page(__name__,name = 'Investment Stats',title='Investment Stats')

# %% Display style of the tables and charts
MENU_STYLE = {
    'height': '112px',
    'width': '912px',
    'display': 'flex',
    'justify-content': 'space-evenly',
    'padding-top': '24px',
    'margin': '-80px auto 0 auto',
    'background-color': '#FFFFFF',
    'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)',
}

MENU_TITLE_STYLE = {
    'margin-bottom': '6px',
    'font-weight': 'bold',
    'color': '#079A82',
}

# %% Import needed data
# Spécifiez les dates sous forme de chaînes
end_date = datetime.today()

# Convertir les chaînes en objets datetime
end_datetime = end_date

# Convertir les objets datetime en timestamps Unix
end_timestamp = int(end_datetime.timestamp() * 1000)

df_volume = T.import_data
df_price = T.actual_summary(df_volume)[0]

usd_value = T.usd_value()

# %% Regroup data into W, M or D
def df_volume_formated(interval,df=df_volume):
    if interval == '1w':
        p = 'W'
    if interval == '1M':
        p = 'M'
    if interval == '3d' or interval == '1d' :
        p = 'D'

    df = df.groupby(['Date', 'crypto', 'action']).sum(numeric_only=True).reset_index()
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df = df.set_index('Date').groupby(['crypto', 'action']).resample(p).sum(numeric_only=True)
    df.drop(df[df['qty_bought'] == 0].index, inplace=True)
    df = df.reset_index()
    return df

# %% Function that enables to select the time range of the graphs
def load_price_data(interval, symbol):
    days = 500
    if interval == '1d':
        start_timestamp  = int ((end_date - timedelta(days=days)).timestamp() * 1000)
    elif interval == '3d':
        start_timestamp  = int ((end_date - timedelta(days=days*3)).timestamp() * 1000)
    elif interval == '1w':
        start_timestamp  = int ((end_date - timedelta(days=days*7)).timestamp() * 1000)
    elif interval == '1M':
        start_timestamp  = int ((end_date - timedelta(days=days*30)).timestamp() * 1000)

    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&startTime={start_timestamp}&endTime={end_timestamp}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

    # Convertir les timestamps en objets datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # convert numerical columns from str to float
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)

    return df

# %% Callback of the price and avg acquisition price chart
@callback(Output(component_id='crypto-graph', component_property='figure'),
    [Input(component_id='crypto-filter', component_property='value'), 
     Input(component_id='interval-filter', component_property='value'),
     ])
def crypto_chart(selected_crypto,interval):

    avg_price = round(df_price.loc[df_price.index == selected_crypto]['Price'].values[0],2) / usd_value

    symbol = selected_crypto+'USDT'    # "EUR"#   #Only works when crypto/EUR pair exists (example XTZ doesn't work)

    interval = interval

    df = load_price_data(interval,symbol)

    fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])
    
    # Add a horizontal line at y = average acquisition price
    fig.add_shape(type='line', x0=df['timestamp'].iloc[0], y0=avg_price, x1=df['timestamp'].iloc[-1], y1=avg_price,
              line=dict(color='#FFFFFF', width=2, dash='dot'))
    
    # Add the line value as an annotation
    fig.add_annotation(x=df['timestamp'].iloc[-1],
                   y=avg_price,
                   text=str(locale.format_string('%.2f', avg_price, grouping=True)+' $'),#' #€'),
                   showarrow=False,
                   font=dict(color="#FFFFFF",size=16),
                   yshift=10,
                   xshift = -50,
                   hovertext=str(locale.format_string('%.2f', avg_price, grouping=True))+' $')#' €')

    fig.update_layout(
        title={
            "text": "Price Chart",
            "font": {"color": "gray"},   
        },
            legend={
            'font': {'color': 'gray'}
        },
        xaxis={
            'tickfont': {'color': 'gray'},
            'titlefont': {'color': 'gray'},
            'gridcolor': 'gray'
        },
        yaxis={
            'tickfont': {'color': 'gray'},
            'titlefont': {'color': 'gray'},
            'gridcolor': 'gray'
        },
        plot_bgcolor="#111111",
        paper_bgcolor="black",
        height=600,
    )
    return fig


# %% Callback of the buying timing chart

@callback(Output(component_id='crypto-graph-vertical', component_property='figure'),
    [Input(component_id='crypto-filter', component_property='value'), 
     Input(component_id='interval-filter', component_property='value'),
     ])
def crypto_chart_vertical(selected_crypto,interval):

    symbol = selected_crypto+'USDT' #"EUR"#      #Only works when crypto/EUR pair exists (example XTZ doesn't work)

    interval = interval
    df = load_price_data(interval,symbol)
    df_volume = df_volume_formated(interval)
    max_high = df['high'].max()

    fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])
    
    df_volume = df_volume[df_volume['Date'] >= df['timestamp'].min()]
    
    # Define a list of x-coordinates for the vertical lines
    buy_dates = df_volume.loc[(df_volume['crypto'] == selected_crypto) & (df_volume['action'] == 'achat'), 'Date'].tolist()
    
    sell_dates = df_volume.loc[(df_volume['crypto'] == selected_crypto) & (df_volume['action'] == 'vente'), 'Date'].tolist()

    # Add vertical lines to the chart for each x-coordinate in the list
    for x in buy_dates:
        if x in sell_dates:
            color = 'orange'
            sell_dates.remove(x)  # Remove the date from sell_dates if it's already plotted in orange
        else:
            color = 'green'
        fig.add_shape(type='line', x0=x, y0=0, x1=x, y1=max_high,
                line=dict(color=color, width=2, dash='dot'))

    # Add remaining sell_dates lines in red
    for x in sell_dates:
        fig.add_shape(type='line', x0=x, y0=0, x1=x, y1=max_high,
                line=dict(color='red', width=2, dash='dot'))

    fig.update_layout(
        title={
            "text": "Volume Chart",
            "font": {"color": "gray"},   
        },
            legend={
            'font': {'color': 'gray'}
        },
        xaxis={
            'tickfont': {'color': 'gray'},
            'titlefont': {'color': 'gray'},
            'gridcolor': 'gray'
        },
        yaxis={
            'tickfont': {'color': 'gray'},
            'titlefont': {'color': 'gray'},
            'gridcolor': 'gray'
        },
        yaxis2={
            'title': 'Volume',
            'tickfont': {'color': 'gray'},
            'titlefont': {'color': 'gray'},
            'gridcolor': 'gray'
        },
        plot_bgcolor="#111111",
        paper_bgcolor="black",
        height=600,
    )
    return fig

# %% Import crypto list into investment_stats page 
# (only crypto symbols that are currently being held in the portfolio)
crypto_list = df_price.index.tolist()     #T.crypto()

# %% Drop symbols not supported by binance
def binance_filter(crypto_list):
    crypto_list_binance = []
    for symbol in crypto_list: 
        interval = '1h'
        end_timestamp = datetime.today()
        start_timestamp = end_timestamp - timedelta(hours=24)
        start_timestamp = int(start_timestamp.timestamp() * 1000)
        end_timestamp = int(end_timestamp.timestamp() * 1000)
        url = f'https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval={interval}&startTime={start_timestamp}&endTime={end_timestamp}'
        response = requests.get(url)
        if response.status_code == 200:
            crypto_list_binance.append(symbol)
    
    # Return the list of crypto symbols supported by binance API
    return crypto_list_binance


# %% Filter that enables the user to filter cryptos
filter_crypto = html.Div(
    children=[
        html.Div(children="Crypto", style = MENU_TITLE_STYLE),
        dcc.Dropdown(
            id="crypto-filter",
            options=[
                {"label": crypto, "value": crypto}
                for crypto in binance_filter(crypto_list)
            ],
            clearable=False,
            className="dropdown",
            value = 'BTC',
            style={
            'backgroundColor': '#f9f9f9',
            'color': '#333333',
            },
        ),
    ])

#  %% crypto price graph layout
crypto_graph = dcc.Graph(
        id='crypto-graph',
        figure = crypto_chart('BTC','1w')
    )

#  %% crypto graph vertical layout
crypto_graph_vertical = dcc.Graph(
        id='crypto-graph-vertical',
        figure = crypto_chart_vertical('BTC','1w')
    )

# %% Intervals
interval = ['1d','3d','1w','1M'] 

# %% Filter that enables a user to choose the interval of the graph (Daily, weekly, monthly)
filter_interval = html.Div(
    children=[
        html.Div(children="Interval", style = MENU_TITLE_STYLE),
        dcc.Dropdown(
            id="interval-filter",
            options=[
                {"label": time, "value": time}
                for time in interval
            ],
            clearable=False,
            className="dropdown",
            value = '1w',
            style={
            'backgroundColor': '#f9f9f9',
            'color': '#333333',
            'align-items': 'center',
            'justify-content': 'center'
            },
        ),
    ])

# %% Header layout
header = html.Div(
    children=[
        html.Div(style = {
  'backgroundColor': 'black', },
            children=[
                html.P(children="🧮", className="header-emoji"),
                html.H1(
                    children="Investment Statistiques", className="header-title"
                )],
            className="header")])




# %% Investment_stats page layout           # VALEUR PAR DEFAULT DANS LES FLILTRES? COULEUR DES CHOIX DANS DROP DOWN 
layout = html.Div(children=[
    header,
    html.Div([filter_crypto,
              filter_interval,
      ],style = MENU_STYLE),
    crypto_graph,
    crypto_graph_vertical,
])