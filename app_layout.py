# Dash Libraries
import dash
from dash import html,Output,Input,State,dcc,dash_table
import dash_bootstrap_components as dbc

# Import app
from main import app

# Menu Configuration, enables to change page in the Webapp
Menu = html.Div(
    [
        dbc.Button("Menu", id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(page["name"], href=page["path"]) 
                    for page in dash.page_registry.values()
                ]
            ),
            id="offcanvas",
            is_open=False,
            style = {"color" : "#111111"} # TO DO - GIVE A DARK STYLE TO THE MENU
        )],    
    className="my-3",
)


# Navbar configuration, enables to see the Menu button at the top of each page
navbar = dbc.Navbar(
    dbc.Container(
        [
            Menu,
            #dbc.Col([Menu]),
            #dbc.Col([Currency]),
        ]
    ),
    color='black',
    dark=True,
)

# App layout
layout = dbc.Container([
    dbc.Row(
        [
            navbar,
            dash.page_container
        ], align='center',className="g-0"
    )
], style={"backgroundColor": "black", "color": "white", "textAlign": "center"}, fluid=True)

# Menu callback, if the menu button is clicked the menu opens or closes
@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n, is_open):
    if n:
        return not is_open
    return is_open