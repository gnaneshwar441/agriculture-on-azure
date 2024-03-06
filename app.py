# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 10:33:59 2024

@author: Gnaneshwar
"""

import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP])
server = app.server

app.layout = html.Div([
    html.H1('Agriculture on Azure (AOA)', 
            style={
                "color":"white",
                "backgroundColor":"green",
                "textAlign":"center"
                }),
    html.Div([
        html.Div(
            dbc.Button(f"{page['name']}", href=page["relative_path"], className="me-1")
        ) for page in dash.page_registry.values()
    ],style={"display":"flex"}),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True, dev_tools_hot_reload = False)