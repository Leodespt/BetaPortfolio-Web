import dash
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import locale
from dash.dash_table.Format import Format, Group, Scheme, Symbol
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

dash.register_page(__name__,name = 'Accepeted P&L',title='Accepeted P&L')

# Link the TransactionData to the wallet page
df = T.import_data
df = T.actual_summary(df)[1]
df = T.final_pl(df)

# Formating of the thousand values
locale.setlocale(locale.LC_ALL, '')
total_pl = df['P&L'].sum()
wallet_pl = locale.format_string('%.2f', total_pl, grouping=True)

# Creation of the header of the page
# Including Title and global info of the wallet (Size and Total P&L)
header = html.Div(
    children=[
        html.Div(style = {
  'backgroundColor': '#111111',#"display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "height": "100vh"},
            children=[
                html.P(children="📈📉", className="header-emoji"),
                html.H3(children="Accepeted P&L", className="header-title"),
                html.H4(f'{wallet_pl} €', style={ 'text-align': 'center',
                                                'color': 'red' if total_pl < 0 else 'green'},className="header-description",)],className="header")])

# Money and pourcentage values formating
money = Format(
                scheme= Scheme.fixed, 
                precision=2,
                group= Group.yes,
                groups=3,
                group_delimiter=',',
                decimal_delimiter='.',
                symbol= Symbol.yes, 
                symbol_suffix=u'€') 

# Table column creatijno and formating 
columns = [
    dict(id='crypto', name='Name'),
    dict(id='P&L', name='P&L', type='numeric', format=money),      
]

# Chart part of the page
chart = dbc.Row([
                dash_table.DataTable(id = "PL-table",
                data = df.to_dict('records'),
                columns = columns,
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
                    'textAlign': 'center',
                    'whiteSpace': 'normal',
                    'height' : 'auto',
                    'minWidth': '10px', 'width': '70px', 'maxWidth': '110px',
                },
                style_data_conditional=[
                {
                    "if": {"column_id": "P&L", "filter_query": "{P&L} < 0"},
                    "color": "#FFA0A0"
                },
                {
                    "if": {"column_id": "P&L", "filter_query": "{P&L} >= 0"},
                    "color": "#C0FFC0"
                }])
    ],style = CARD_STYLE)

# Accepted/Realized P&L layout
layout = dbc.Row([
        dbc.Col([header]),
        dbc.Col([chart])
        ])