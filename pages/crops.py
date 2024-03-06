# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 15:28:02 2024

@author: Gnaneshwar
"""

import dash
from dash import dcc, html, Input, Output,State, html, callback
import dash_bootstrap_components as dbc
# from genai_api import genai_api
# from genai_palm_api import genai_api
# from genai_azure_api import genai_api
from genai_azure_vision_api import genai_vision_api
from genai_azure_text_api import genai_text_api
import base64
import datetime
import io
import os
import re

dash.register_page(__name__)
send_icon = html.I(className="bi bi-send-fill")
image_icon = html.I(className="bi bi-card-image")

def textbox(text, box="AI", name="bot"):
    text = text.replace(f"{name}:", "").replace("You:", "")
    style = {
        "max-width": "60%",
        "width": "max-content",
        "padding": "5px 10px",
        "border-radius": 25,
        "margin-bottom": 20,
    }

    if box == "user":
        style["margin-left"] = "auto"
        style["margin-right"] = 0

        return dbc.Card(text, style=style, body=True, color="primary", inverse=True)

    elif box == "AI":
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        thumbnail = html.Img(
            src=dash.get_asset_url("bot.jpg"),
            style={
                "border-radius": 50,
                "height": 36,
                "margin-right": 5,
                "float": "left",
            },
        )
        textbox = dbc.Card(text, style=style, body=True, color="light", inverse=False)

        return html.Div([thumbnail, textbox])

    else:
        raise ValueError("Incorrect option for `box`.")
        
layout = html.Div([
    html.Div([
        # html.P("Hello World")
    #     dcc.Upload(
    #     id='upload-image',
    #     children=html.Div([
    #         'Drag and Drop or ',
    #         html.A('Select Files')
    #     ]),
    #     style={
    #         'width': '100%',
    #         'height': '60px',
    #         'lineHeight': '60px',
    #         'borderWidth': '1px',
    #         'borderStyle': 'dashed',
    #         'borderRadius': '5px',
    #         'textAlign': 'center',
    #         # 'margin': '10px'
    #     },
    #     # Allow multiple files to be uploaded
    #     multiple=False
    # ),
    dcc.Loading(
          id="loading-1",
          type="default",
            children=[html.Div(id='output-image-upload')]
    ),  
    # html.Div(id='output-image-upload'),
    
    ], style={"width":"75%","height":"80vh"}),
    
    html.Div([
        # html.P("Hello Dash plotly!"),
        # html.Pre(id="chat_output",style={"whiteSpace":"pre-wrap","height":"80vh"}),
        html.Div(id="chat_output",style={"height":"80vh","overflow-y":"auto"}),
        # html.Br(),
        dbc.Spinner(html.Div(id="loading-component"),size="sm",color="primary", type="grow"),
        html.Div([
            
            dbc.Input(id="chat_input", placeholder="Ask chatbot...", type="text"),
            # dbc.Button("Submit", id="chat_submit", color="primary"),
            dcc.Upload(
                id='upload-image',
                children=dbc.Button([
                    # 'Drag and Drop or ',
                    image_icon,""
                    # html.A('Select Files')
                ], color="info",outline=True),
                style={
                    'width': '100%',
                    # 'fontSize':'2rem',
                    # 'color':'cornflowerblue'
                    # 'height': '60px',
                    # 'lineHeight': '60px',
                    # 'borderWidth': '1px',
                    # 'borderStyle': 'dashed',
                    # 'borderRadius': '5px',
                    # 'textAlign': 'center',
                    # 'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=False
            ),
            dbc.Button([send_icon,""], id="chat_submit", color="primary"),
        ],style={"display":"flex","bottom":"0"}),
        dcc.Store(id="store-conversation", data=""),
    ], style={"width":"25%","backgroundColor":"lightcyan","position":"fixed","left":"75%"}),
    
    
], style={"display":"flex"})

# @callback([Output("chat_output", "children"), Output("loading-component", "children")], [Input("chat_submit", "n_clicks"),Input("chat_input", "n_submit")], [State("chat_input","value")])
# def output_text(clicks, n_submit, input_value):
#     if input_value is not None:
#         try:
#             result = genai_text_api(input_value)
#             result = result.replace('**','')
#             return result,None
#         except Exception as e:
#             print("*** EXCEPTION ERROR ***")
#             print(str(e))
#     return "",None

@callback([Output("store-conversation", "data"), Output("loading-component", "children")], [Input("chat_submit", "n_clicks"),Input("chat_input", "n_submit")], [State("chat_input","value"), State("store-conversation", "data")])
def output_text(n_clicks, n_submit, input_value, chat_history):
    name = "bot"

    if n_clicks is None and n_submit is None:
        prompt = f"{name}: Hello! I'm here to provide you Agriculture related information. You can upload an image or ask me a question.<split>"
        # return "", None
        return prompt, None
    if input_value is None or input_value == "":
        return chat_history, None
    
    # name = "bot"
    
    
    
     # First add the user input to the chat history
    chat_history += f"You: {input_value}<split>{name}:"
    
    try:
        result = genai_text_api(input_value)
        result = result.replace('**','')
        chat_history += f"{result}<split>"
        return chat_history,None
    except Exception as e:
        print("*** EXCEPTION ERROR ***")
        print(str(e))

@callback(Output("chat_output", "children"), [Input("store-conversation", "data")])
def update_display(chat_history):
    return [
        textbox(x, box="AI") if i % 2 == 0 else textbox(x, box="user")
        for i, x in enumerate(chat_history.split("<split>")[:-1])
    ]

# @callback(Output("chat_output", "children", allow_duplicate=True), [Input("chat_submit", "n_clicks")], prevent_initial_call=True)
# def clear_output(clicks):
#     return "LOADING..."

@callback(Output("chat_input", "value"), [Input("chat_submit", "n_clicks"),Input("chat_input", "n_submit")])
def clear_input(clicks, n_submit):
    return ""

# def parse_contents(contents, filename):
#     try:
#         if '.jpg' in filename: # Assume that the user uploaded a JPEG file
#             # Saving the uploaded file into images folder
#             data = contents.encode("utf8").split(b";base64,")[1]
#             with open(f"./images/{filename}", "wb") as fp:
#                 fp.write(base64.decodebytes(data))
#             result = genai_vision_api(os.path.abspath(f"./images/{filename}"))
            
#             return html.Div([
#                 # HTML images accept base64 encoded strings in the same format
#                 # that is supplied by the upload
#                 html.Img(src=contents,style={"height":"150px"}),
#                 # html.H5(filename),
#                 html.Pre(result,style={"white-space":"pre-wrap","height":"50vh"})
#             ])
#         else:
#             raise Exception("Only .jpg images are supported")
#     except Exception as e:
#         print(e)
#         return html.Div([
#             str(e)
#             # 'There was an error processing this file.'
#         ])

# @callback(Output('output-image-upload', 'children'),
#               Input('upload-image', 'contents'),
#               State('upload-image', 'filename'))
# def update_output(list_of_contents, list_of_names):
#     if list_of_contents is not None:
#         children = parse_contents(list_of_contents, list_of_names)
#         return children

def parse_contents(contents, filename):
    if '.jpg' in filename: # Assume that the user uploaded a JPEG file
        # Saving the uploaded file into images folder
        data = contents.encode("utf8").split(b";base64,")[1]
        with open(f"assets/{filename}", "wb") as fp:
            fp.write(base64.decodebytes(data))
        result = genai_vision_api(os.path.abspath(f"./assets/{filename}"))
        # result = 'Name of crop: Rice\n\nStates grown in India:\n- West Bengal\n- Punjab\n- Uttar Pradesh\n- Andhra Pradesh\n- Bihar\n- Tamil Nadu\n- Odisha\n- Assam\n- Chhattisgarh\n- Haryana\n\nSeason of the Crop:\n- Kharif season (June to November)\n- Rabi season (November to March) in some parts of India\n\nCultivation methods:\n- Wet or lowland cultivation (most common method)\n- Dry or upland cultivation\n- Deep water or floating rice cultivation\n\nSeeds:\n- IR64\n- Sambha Mahsuri (BPT 5204)\n- Pusa Basmati 1121\n- Swarna\n\nFertilizers:\n- Urea\n- Di-ammonium phosphate (DAP)\n- Muriate of potash (MOP)\n- Zinc sulfate\n\nPesticides:\n- Pretilachlor\n- Butachlor\n- Buprofezin\n- Isoprothiolane\n\nProfit: Profit percentage for rice farming in India can vary widely depending on factors like yield, quality of the crop, market price at the time of sale, and the region where it is grown. However, on average, farmers can expect a profit margin of around 20-30% under optimal conditions.\n\nCost per Acre: The cost of cultivating rice per acre in India can range from INR 30,000 to INR 50,000, depending on the variety of rice, the method of cultivation, and the region.'
        result_list = result.split("\n\n")
        print("\nResult:")
        print(result)
        
        
        name_crop = result_list[0]
        states_crop = result_list[1]
        season_crop = result_list[2]
        cultivate_crop = result_list[3]
        seeds_crop = result_list[4]
        fertilizer_crop = result_list[5]
        pesticide_crop = result_list[6]
        profit_crop = result_list[7]
        cost_crop = result_list[8]
        
        # abs_filepath = os.path.abspath(f"./images/{filename}")
        abs_filepath = f"assets/{filename}"
        
        # Clean-up
        name_crop = name_crop.replace('Name of crop: ','')
        
        states_crop = states_crop.replace('States grown in India:\n','')
        states_crop = states_crop.replace('-','')
        states_crop = states_crop.split('\n')
        
        season_crop = season_crop.replace('Season of the Crop:\n','')
        season_crop = season_crop.replace('-','')
        season_crop = season_crop.split('\n')
        
        cultivate_crop = cultivate_crop.replace('Cultivation methods:\n','')
        cultivate_crop = cultivate_crop.replace('-','')
        cultivate_crop = cultivate_crop.split('\n')
        
        seeds_crop = seeds_crop.replace('Seeds:\n','')
        seeds_crop = seeds_crop.replace('-','')
        seeds_crop = seeds_crop.split('\n')
        
        fertilizer_crop = fertilizer_crop.replace('Fertilizers:\n','')
        fertilizer_crop = fertilizer_crop.replace('-','')
        fertilizer_crop = fertilizer_crop.split('\n')
        
        pesticide_crop = pesticide_crop.replace('Pesticides:\n','')
        pesticide_crop = pesticide_crop.replace('-','')
        pesticide_crop = pesticide_crop.split('\n')
        
        try:
            profit_crop = re.search(r'\d{1,3}%?(.+\d{1,2}%)*',profit_crop)[0]
        except Exception as e:
            profit_crop = ""
        # cost_crop = re.search(r'INR \d+(?:,\d+)? (?:to INR \d+(?:,\d+)?)?',cost_crop)[0]
        try:
            cost_crop = re.search(r'(INR|₹).*\d+(,\d+)?(.+\d+(,\d+)?)?',cost_crop)[0]
        except Exception as e:
            cost_crop = ""
        
        return {"abs_filepath":abs_filepath,"name_crop":name_crop,"states_crop":states_crop,"season_crop":season_crop,"cultivate_crop":cultivate_crop,"seeds_crop":seeds_crop,"fertilizer_crop":fertilizer_crop,"pesticide_crop":pesticide_crop,"profit_crop":profit_crop,"cost_crop":cost_crop}
    else:
        raise Exception("Only .jpg images are supported")

        
    
@callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        try:
            children = parse_contents(list_of_contents, list_of_names)
            print("\nchildren:")
            print(children)
            crop_card = dbc.Card([
                dbc.CardImg(src=children['abs_filepath'],bottom=True,style={"height": "18rem"}),
                dbc.CardBody(html.H3(f"{children['name_crop']}", className="card-text",style={"textAlign": "center"}),style={"padding": "0"}),
                
            ],style={"height":"20rem","width": "18rem"})
            
            states_card = dbc.Card([
                dbc.CardHeader(html.H5("States Grown", className="card-title")),
                dbc.CardBody(html.Div(html.Ul(id='my-list', children=[html.Li(i) for i in children['states_crop']]),className="card-text"))
            ],style={"height":"20rem","overflow-y":"auto"}, color="aliceblue")
            
            season_card = dbc.Card([
                dbc.CardHeader(html.H5("Seasons Grown", className="card-title")),
                dbc.CardBody(html.Div(html.Ul(id='my-list', children=[html.Li(i) for i in children['season_crop']]),className="card-text"))
            ],style={"height":"20rem","overflow-y":"auto"}, color="mintcream", inverse=False)
            
            cultivation_card = dbc.Card([
                dbc.CardHeader(html.H5("Cultivation Methods", className="card-title")),
                dbc.CardBody(html.Div(html.Ul(id='my-list', children=[html.Li(i) for i in children['cultivate_crop']]),className="card-text"))
            ],style={"height":"20rem","overflow-y":"auto"}, color="light", inverse=False)
            
            seeds_card = dbc.Card([
                dbc.CardHeader(html.H5("Seeds", className="card-title")),
                dbc.CardBody(html.Div(html.Ul(id='my-list', children=[html.Li(i) for i in children['seeds_crop']]),className="card-text"))
            ],style={"height":"20rem","overflow-y":"auto"}, color="floralwhite", inverse=False)
            
            fertilizer_card = dbc.Card([
                dbc.CardHeader(html.H5("Fertilizer", className="card-title")),
                dbc.CardBody(html.Div(html.Ul(id='my-list', children=[html.Li(i) for i in children['fertilizer_crop']]),className="card-text"))
            ],style={"height":"20rem","overflow-y":"auto"}, color="ghostwhite")
            
            pesticide_card = dbc.Card([
                dbc.CardHeader(html.H5("Pesticides", className="card-title")),
                dbc.CardBody(html.Div(html.Ul(id='my-list', children=[html.Li(i) for i in children['pesticide_crop']]),className="card-text"))
            ],style={"height":"20rem","overflow-y":"auto"}, color="honeydew", inverse=False)
            
            profit_card = dbc.Card([
                dbc.CardHeader(html.H5("Profit", className="card-title")),
                dbc.CardBody(html.P(children['profit_crop'],className="card-text"))
            ],style={"height":"20rem","overflow-y":"auto"}, color="snow", inverse=False)
            
            cost_card = dbc.Card([
                dbc.CardHeader(html.H5("Cost per Acre", className="card-title")),
                dbc.CardBody(html.P(children['cost_crop'],className="card-text"))
            ],style={"height":"20rem","overflow-y":"auto"}, color="azure", inverse=False)
            
            cards = html.Div([
                dbc.Row([
                    dbc.Col(crop_card),
                    dbc.Col(states_card),
                    dbc.Col(season_card),
                    dbc.Col(cultivation_card),
                    dbc.Col(seeds_card),
                    
                ],className="mb-4"),
                dbc.Row([
                    dbc.Col(fertilizer_card),
                    dbc.Col(pesticide_card),
                    dbc.Col(profit_card),
                    dbc.Col(cost_card),
                ])
            ])
            return cards
        except Exception as e:
            return dbc.Alert(
                str(e),
                color="danger",
                id="alert-auto",
                is_open=True,
                duration=4000,
            )
            # return str(e)
        