import dash
from dash import html, dash_table, dcc, Output, Input, State, callback
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

dash.register_page(__name__,name = 'Transactions',title='Transactions')

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


# %% Import Transaction Data

df = T.import_data

# %% Filter that enables the user to filter cryptos
transactions_table = html.Div(
    style={'height': '400px', 'overflowY': 'scroll'},
    children=[
        dash_table.DataTable( 
            id='datatable',
             columns=[
                {'id': 'Date', 'name': 'Date'},
                {'id': 'qty_bought', 'name': 'Quantity Bought'},
                {'id': 'qty_spent', 'name': 'Quantity Spent'},
                {'id': 'fee', 'name': 'Fee'},
                {'id': 'price', 'name': 'Price'},
                {'id': 'fiat', 'name': 'Fiat'},
                {'id': 'crypto', 'name': 'Crypto'},
                {'id': 'action', 'name': 'Action'},
                {'id': 'platform', 'name': 'Platform'},
                {'id': 'Commentaire', 'name': 'Commentaire'}
            ], 
            data = df.to_dict('records'),
            filter_action="native",
            filter_options={"placeholder_text": "Filter column..."},
            #page_size=10,
            style_cell={'color': 'black' },
            style_as_list_view=True,
            style_header={
                'text-align': 'center',
                'backgroundColor': '#888',
                'fontWeight': 'bold'
            },
            editable=True,  # Enable editing of cell values
            row_deletable=True,  # Enable row deletion
        )
    ]
)

# %% Header layout
header = html.Div(
    children=[
        html.Div(style = {
  'backgroundColor': 'black', },
            children=[
                html.P(children="📝", className="header-emoji"),
                html.H1(
                    children="Transactions", className="header-title"
                )],
            className="header")])

# %% Investment_stats page layout        
layout = html.Div(
    style={
    'backgroundColor': 'black',
    'height': '100vh',  # Définit la hauteur de l'élément à 100% de la hauteur de la vue
    'overflow': 'auto'  # Ajoute une barre de défilement si le contenu dépasse la hauteur de la vue
},
    children=[
    header,
    transactions_table,
])

# Ajouter popup de confirmation lors de suppression d'une colonne 
