import random
from datetime import datetime
import statistics
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
from itertools import groupby
from operator import itemgetter
from collections import defaultdict
from plotly.subplots import make_subplots
import warnings
import traceback
import re
from PyPDF2 import PdfFileReader
import os
import camelot
from collections import OrderedDict
import io
import math
import dash
import json
import base64
import locale
import numpy as np
import pandas as pd
from dash import dcc, html, Dash, dash_table
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


def card_introduction(title, ptext, suptitle):
    card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="https://avatars.githubusercontent.com/u/92005917?s=400&u=d4549d3393148a3e2fea015801e205264d5b65a5&v=4",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            
                            html.H4(title, className="card-title", style={"color":"white"}),
                            html.Small(
                                suptitle,
                                className="card-text text-muted",
                                style={"align-items":"center"}
                            ),
                            html.P(
                                ptext,
                                className="card-text",
                                style={"text-align": "justify"}
                            ),
                        ]
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    className="mb-3 cards1",
    style={"maxWidth": "540px", "color":"white"},
)

    return card

#, style={"border":"solid", "border-color":"black","background-color":"black", "color":"white", "border-radius":"10px", "margin":"auto", "width":"40%"}
def card_content(header, ptext, badge = None, bcgc = False, display=False):
    #, "display":"flex", "justify-content":"space-between"

    stl = {"border-color":"white", "color":"white", "display":"flex", "justify-content":"space-between"} if display else {"border-color":"white", "color":"white"}

    card_content_expl = [
        dbc.CardHeader([html.H5(header, className="legend_2", style={"font-size":"20px"}), badge], style=stl),
        dbc.CardBody(
            [
                #html.H5(title, className="card-title", style={"color":"white"}),
                html.P(
                    ptext,
                    className="card-text",
                    style={"color":"white", "text-align": "justify"}
                ),
            ]
        ),
    ]

    return dbc.Row([dbc.Col(dbc.Card(card_content_expl, color=bcgc, inverse=True))], className="cards1") if bcgc else dbc.Row([dbc.Card(card_content_expl, color="light", outline=True, style={"background-color":"transparent", "border":"none"})], className="cards1")


def badge_button(text, id, id_num):
    if text == 'Available':
        color = "success"
    else:
        color = "secondary"
    return html.Div([dbc.Badge(text, color=color, className="me-1", style={"width":"25%", "height":"20px"}), html.Div([], style={"width":"50%"}),dbc.Button("Select", id={
                'type': 'dynamic-dpn-ctg',
                'index': id_num},outline=True, color="light", className="me-1", size="sm", style={"width":"25%", "height":"28px"})], style={"display":"flex"})

def encontrar_diferencia(lista1, lista2):
    lista1, lista2 = [0 if elemento is None else elemento for elemento in lista1], [0 if elemento is None else elemento for elemento in lista2]
    for i in range(len(lista1)):
        if lista1[i] > lista2[i]:
            return i
    return None


def button_download_resume():
    return html.Div([
        dbc.Button("Download resume", id="btn_xlsx", color="success", className="me-1"),
    dcc.Download(id="download-dataframe-xlsx")
    ], style={"width":"30%"})

def social_bar():
    soc_bar = html.Div([
        html.A(
            href="https://github.com/alexisrangelcalvo",
            children=[
                html.Img(src="https://img.uxwing.com/wp-content/themes/uxwing/download/brands-social-media/github-icon.svg", className="set-img2", style={"border-radius":"8px", "background-color":"white", "margin-right": "5px"})
            ]
        ),
        html.A(
            href="https://rpubs.com/alexisrangel",
            children=[
                html.Img(src="https://storage.scolary.com/storage/file/public/38871d5b-8187-47a2-aeb8-17e44c7dbb83.svg", className="set-img2", style={"border-radius":"12px"})
            ]
        ),
        html.A(
            href="https://www.instagram.com/",
            children=[
                html.Img(src="https://www.logo.wine/a/logo/YouTube/YouTube-Icon-Full-Color-Logo.wine.svg", className="set-img2")
            ]
        ),
        html.A(
            href="https://www.linkedin.com/",
            children=[
                html.Img(src="https://img.uxwing.com/wp-content/themes/uxwing/download/brands-social-media/twitter-app-icon.svg", className="set-img2")
            ]
        ),
    ], style={"display":"flex", "align-items":"center",  "width":"25%"})
    return soc_bar


card_content2 = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]

def navbar_function(brand, href):
    PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
    navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Home", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/Golayad/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.NavItem(dbc.NavLink(brand, href=href, style={"color":"white"})),
        ]
    ),
    color="dark",
    dark=True,
)
    return navbar


def dcc_upload():
    return html.Div([dcc.Upload(
        id="upload_data_lab",
        children=html.Div([
            dcc.Loading(
            id="loading-1",
            type="default",
            color='white',
            children=html.A(id = "filename_lab", style={'textAlign': 'center', 'color': 'white'})
        )
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'color':'white'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    #html.Div(id='filename_lab')
    ])

def parse_contents(contents, filename, date):
    """
        This function help us to manage the file to store in a dash request way
        currently working just for .csv, .xls, y .pdf files
    """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
    return df.to_json(orient='records')



class templateLab(object):

    """
        Esta clase pretende generar templates para la creación de las vistas de los laboratorios en la vista Alexis´s lab
    """

    def __init__(self, name_lab):
        self.name_lab = name_lab
        self.header_lab = html.Div([html.H4(name_lab, className="legend_2", style={"width":"80%"}), html.Div(dcc_upload(), style={"width":"80%", "margin-right":"10px"})], style={"display":"flex", "justify-content":"space-evenly", "align-items":"center", "margin-bottom":"10px"}, className='cards1')
        self.customized_panel = []
        self.command_board = html.Div(["command board"])
        self.body_lab = html.Div()
        self.footer_lab = []

    def customize_command_board(self):
        if self.name_lab == "Statistics Lab":
            cmd_board = self.command_board_statistics()
            body_lab = self.customize_body_statistics()
        elif self.name_lab == "Supervissed learning Lab":
            cmd_board = self.command_board_sl()
            body_lab = self.customize_body_sl()
        elif self.name_lab == "Unsupervissed learning":
            pass
        elif self.name_lab == "Time series & forecasting":
            pass
        elif self.name_lab == "Data mining":
            cmd_board = self.command_board_dm()
            body_lab = self.customize_body_dm()
        elif self.name_lab == "Miscellaneous":
            pass
        self.command_board = cmd_board
        self.body_lab = body_lab

    def customize_footer(self):
        self.footer_lab = html.Div("Adding a footer", style={"border-color":"white"})


    @staticmethod
    def command_board_statistics():
        """
            Nos quedamos aquí (19/05/2023)
            Modificando el command board de statistics, queda pendiente agregar dropdowns que tomaran info de los archivos cargados y estilizar
        """
        cbs = html.Div([
            html.Br(),
            html.H4("Command board", style={"margin-top":"5px"}),
            
            html.Div([html.H5(["Upload the file!"], id="r1_c1_labs", style={"display":"flex", "justify-content":"space-evenly", "align-items":"center","width":"15%"}),
                      html.Div([
                        html.Div([html.P("Tarjet", style={"color":"white", "font-size":"15px", "margin-bottom":"-1px"}), 
                                  html.Div(dcc.Dropdown(['New York City', 'Montreal', 'San Francisco'], placeholder="Select tarjet"),  id="r1_c2_labs")
                                  ], style={"width":"30%"}),
                        html.Div([html.P("Variable", style={"color":"white", "font-size":"15px", "margin-bottom":"-1px"}),
                                html.Div(dcc.Dropdown(['New York City', 'Montreal', 'San Francisco'], placeholder="Select variable"),  id="r1_c3_labs")
                        ], style={"width":"30%"}),
                        html.Div([html.P("Type of graph", style={"color":"white", "font-size":"15px", "margin-bottom":"-1px"}),
                                html.Div(dcc.Dropdown(['New York City', 'Montreal', 'San Francisco'], placeholder="Select type of graph"),  id="r1_c4_labs")
                        ], style={"width":"30%"}),
                        dbc.Checklist(options=[{"label": "Trend line", "value": 2}], id="switches_input_lab1", switch=True,  style={"color":"white", "width":"5%"}),
                      ], style={"display":"flex", "justify-content":"space-evenly", "align-items":"center","width":"60%"}),
                      html.Div([
                            dbc.Button("Create!", color="info", className="me-1", id = "button_graph_1"),
                            #dbc.Button("Add dimention", color="secondary", className="me-1", style={"width":"50%", "font-size":"10px"}),
                            html.Div([
                                dbc.Checklist(options=[{"label": "", "value": 2}], id="switches_input_lab2", switch=True,  style={"color":"white", "width":"5%", "margin":"auto"}),
                                html.P("Add dimention",  style={"font-size":"12px", "color":"white", "margin":"auto", "text-align": "center"})
                            ])
                            
                      ], style={"display":"flex", "justify-content":"center", "align-items":"center","width":"20%"}),
                        
                        ], 
                        className="command_board"), 
            html.Div(id="new_dimensions_lab"),
            html.Br()
                        
                        ], className="cards1")
        return cbs
    
    @staticmethod
    def customize_body_statistics():
        """
            Using tabs to manage with statistcs test (univarite, bivariate, multivariate)
        """
        body_lab = html.Div([
        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='Univarite', value='tab-1', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Bivariate', value='tab-2', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Multivariate', value='tab-3', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Other', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
        html.Div(id='tabs-content-inline')
        ])

        return body_lab
    
    
    @staticmethod
    def command_board_sl():
        cbs = html.Div([html.H4("TARJET"), html.H4("MODELS"), html.H4("THIRD PART")], className="command_board")
        return cbs
    
    @staticmethod
    def customize_body_sl():
        """
            Using tabs to manage with statistcs test (univarite, bivariate, multivariate)
        """
        body_lab = html.Div([
        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='Tab1', value='tab-1', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab2', value='tab-2', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab3', value='tab-3', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab4', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
        html.Div(id='tabs-content-inline')
        ])

        return body_lab
    
    @staticmethod
    def command_board_dm():
        cbs = html.Div([html.H4("TARJET")], className="command_board")
        return cbs
    
    @staticmethod
    def customize_body_dm():
        """
            Using tabs to manage with statistcs test (univarite, bivariate, multivariate)
        """
        body_lab = html.Div([
        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='Tab1', value='tab-1', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab2', value='tab-2', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab3', value='tab-3', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab4', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
        html.Div(id='tabs-content-inline')
        ])
        return body_lab
    
    def wrap_lab(self):
        """
            Se requiere devolver como lista, no como html.Div() dash component
        """
        lab_card = [
        self.header_lab,
        self.command_board,
        #self.customized_panel,
        self.body_lab,
        self.footer_lab
    ]
        return lab_card
    

def determinar_tipo_variable(columna):
    unique_values = columna.unique()
    num_unique_values = len(unique_values)
    is_quantitative = pd.api.types.is_numeric_dtype(columna)
    
    if is_quantitative:
        return 'Cuantitativa'
    elif num_unique_values <= 10:
        return 'Cualitativa'
    else:
        return 'No determinado'
    

def datatable_lab(df):
    return dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            sort_action='native',
            filter_action="native",
            sort_mode='multi',
            selected_rows=[],
            page_action='native',
            # dividir el paginado por el num de metricas para cada cliente
            page_size=5,
            editable=True,

            style_cell={
                'height': 'auto',
                'whiteSpace': 'normal',
                'font-family': 'Poppins',
                'font-size': '11.3px',
                'font-weight': 'bold',
                'z-index': '0',
                'textAlign': 'center'
            },

            css=[{
                'selector': '.dash-table-tooltip',
                'rule': 'background-color: #000000; font-family: monospace; color: white',
                'z-index': '0', 'position': 'absolute', 'border': 'solid', 'border-color': 'black'
            }],

            style_header={
                'fontWeight': 'bold',
                'textAlign': 'center',
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data_conditional=[
            {
                'backgroundColor': 'rgb(114, 114, 114)',
                'color': 'white',
            },
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(59, 59, 59)',
                'color': 'white',
            },

        ]
        )


tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}