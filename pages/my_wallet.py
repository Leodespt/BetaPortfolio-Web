import dash
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Group, Scheme, Symbol
import plotly.express as px
import locale
# Import Transaction data
import TransactionData as T

# Display style of the tables and charts
WRAPPER_STYLE = {
    'margin-right': 'auto',
    'margin-left': 'auto',
    'max-width': '1200px',
    'padding-right': 'auto',
    'padding-left': 'auto',
    'margin-top': '32px',
}

CARD_STYLE = {
    'margin-bottom': '24px',
    'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)',
}

# Root to the Wallet page
dash.register_page(__name__,path='/',name = 'Wallet',title='Wallet')

# Link the TransactionData to the wallet page
df = T.import_data
df = T.actual_summary(df)[0]
trx_summary = T.final_table(df)
total_table = T.total_table(trx_summary)

# Formating of the thousand values
locale.setlocale(locale.LC_ALL, '')
wallet_value = locale.format_string('%.2f', total_table[0], grouping=True)
wallet_pl = locale.format_string('%.2f', total_table[1], grouping=True)
pl_pourcentage = locale.format_string('%.2f', total_table[2], grouping=True)

# Creation of the header of the page
# Including Title and global info of the wallet (Size and Total P&L)
header = html.Div(
    children=[
        html.Div(style = {
  'backgroundColor': '#111111', },
            children=[
                html.P(children="📊", className="header-emoji"),
                html.H1(
                    children="My Wallet", className="header-title"
                ),
                html.P(f'Wallet value : {wallet_value} €', style={ 'text-align': 'center',},className="header-description"),
                html.P(f'{wallet_pl} €', style={ 'text-align': 'center','color': 'red' if total_table[1] < 0 else 'green'},className="header-description",),
                html.P(f'{pl_pourcentage} %', style={ 'text-align': 'center','color': 'red' if total_table[2] < 0 else 'green'},className="header-description",)],
            className="header",
        ),
    ])

# Pie chart creation
explode = (0.02,)*len((trx_summary))
pie = px.pie(trx_summary, values="Value", 
                names='Name', title='Portfolio allocation',height= 500, width = 500)
pie.update_traces(textposition='inside', textinfo='percent+label',hole=.4,pull=explode,)
pie.update_layout(
    title={
        "text": "Pie Chart",
        "font": {"color": "gray"},   
    },
    legend={"font": {"color": "white"}},
    plot_bgcolor="white",
    paper_bgcolor="#111111"
)

# Money and pourcentage values formating
#money = dash_table.FormatTemplate.money(2)
percentage = dash_table.FormatTemplate.percentage(2)

money = Format(
                scheme= Scheme.fixed, 
                precision=2,
                group= Group.yes,
                groups=3,
                group_delimiter=',',
                decimal_delimiter='.',
                symbol= Symbol.yes, 
                symbol_suffix=u'€') # $


# Table column creatijno and formating 
columns = [
    dict(id='Name', name='Name'),
    dict(id='Amount', name='Amount', type='numeric'),
    dict(id='Market Price', name='Market Price', type='numeric', format=money),
    dict(id='Value', name='Value', type='numeric', format= money),
    dict(id='P&L', name='P&L', type='numeric', format=money),
    dict(id='P&L %', name='P&L %', type='numeric', format=percentage),  
]

# Chart part of the page
chart = html.Div(
    children=[
    dbc.Row([
        # Pie chart creation
       dbc.Col(
            children=dcc.Graph(
                id="pie-chart", 
                figure = pie, 
                style = CARD_STYLE,
                )
        ),
        # Table creation
        dbc.Col(
            children=dash_table.DataTable(id = "investments-table",
                data= trx_summary.to_dict('records'),
                columns= columns,
                style_cell_conditional=[
                    {
                        'if': {'column_id': c},
                        'textAlign': 'left'
                    } for c in ['Date', 'Region']
                ],
                style_header={
                    'backgroundColor': '#111111',
                    'color': 'grey',
                    'fontWeight': 'bold',
                    'textAlign': 'center'
                },
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'color': '#F5F5F5',
                    'backgroundColor': '#111111'
                },
                style_as_list_view=True,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'whiteSpace': 'normal',
                    'height' : 'auto',
                    'minWidth': '110px', 'width': '110px', 'maxWidth': '110px',
                },
                style_data_conditional=[
                {
                    "if": {"column_id": "P&L", "filter_query": "{P&L} < 0"},
                    "color": "#FFA0A0"
                },
                {
                    "if": {"column_id": "P&L", "filter_query": "{P&L} >= 0"},
                    "color": "#C0FFC0"
                },
                {
                    "if": {"column_id": "P&L %", "filter_query": "{P&L %} < 0"},
                    "color": "#FFA0A0"
                },
                {
                    "if": {"column_id": "P&L %", "filter_query": "{P&L %} >= 0"},
                    "color": "#C0FFC0"
                }],
            ),
            style = CARD_STYLE,
        )]),
    ],
    style = WRAPPER_STYLE)


# Layout of the wallet page
layout = html.Div([dbc.Container([
    dbc.Row(
        [
                    header, 
                    chart,
                    #html.Div(id='currency-input'),
        ], align='center',className="g-0", 
    )
], style={"backgroundColor": "black", "color": "white", "textAlign": "center"})])
