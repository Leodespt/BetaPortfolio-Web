import dash
import dash_bootstrap_components as dbc

#Creation of the app, main app module
external_stylesheets=[dbc.themes.SPACELAB]
app = dash.Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets)