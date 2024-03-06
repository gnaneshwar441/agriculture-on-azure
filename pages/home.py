# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 12:02:38 2024

@author: Gnaneshwar
"""

import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H5('Agriculture on Azure is a farmer oriented platform that provides rich and consolidated information about farming and crops'),
    html.Div('Click on the tabs above to get started'),
])
