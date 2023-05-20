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
            className="g-0 d-flex align-items-center", style={"background-color":"#1a1d20"},
        )
    ],
    className="mb-3",
    style={"maxWidth": "540px", "color":"white", "background-color":"#212428"},
)

    return card

#, style={"border":"solid", "border-color":"black","background-color":"black", "color":"white", "border-radius":"10px", "margin":"auto", "width":"40%"}
def card_content(header, ptext, badge = None, bcgc = False):

    card_content_expl = [
        dbc.CardHeader([html.H5(header, className="legend_2", style={"font-size":"20px"}), badge], style={"border-color":"white", "color":"white"}),
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

    return dbc.Row([dbc.Col(dbc.Card(card_content_expl, color=bcgc, inverse=True))]) if bcgc else dbc.Row([dbc.Card(card_content_expl, color="light", outline=True, style={"background-color":"transparent"})])


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
    return dcc.Upload(
        id="id_upload_lab",
        children=html.Div([
            html.A("Upload your xlsx or pdf files", style={"color":"white"})
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
    )


class templateLab(object):

    """
        Esta clase pretende generar templates para la creación de las vistas de los laboratorios en la vista Alexis´s lab
    """

    def __init__(self, name_lab):
        self.name_lab = name_lab
        self.header_lab = html.Div([html.H4(name_lab, className="legend_2", style={"width":"100%"}), html.Div(dcc_upload(), style={"width":"80%"})], style={"display":"flex", "justify-content":"space-evenly", "align-items":"center"})
        self.customized_panel = []
        self.command_board = html.Div(["command board"])
        self.body_lab = html.Div(["Content"])
        self.footer_lab = []

    def customize_command_board(self):
        if self.name_lab == "Statistics Lab":
            cmd_board = self.command_board_statistics()
        elif self.name_lab == "Supervissed learning Lab":
            cmd_board = self.command_board_sl()
        elif self.name_lab == "Unsupervissed learning":
            pass
        elif self.name_lab == "Time series & forecasting":
            pass
        elif self.name_lab == "Data mining":
            cmd_board = self.command_board_dm()
        elif self.name_lab == "Miscellaneous":
            pass
        self.command_board = cmd_board

    def customize_panel(self):
        self.customized_panel = html.Div([
            dcc.Dropdown(
                options=[{'label': 'NYC', 'value': 'NYC'}, {'label': 'MTL', 'value': 'MTL'}, {'label': 'SF', 'value': 'SF'}],
                value='NYC',
                id={'type': 'dropdown', 'index': 0}
            ),
            dcc.Checklist(
                options=[
                    {'label': 'New York City', 'value': 'New York City'},
                    {'label': 'Montréal', 'value': 'Montréal'},
                    {'label': 'San Francisco', 'value': 'San Francisco'}
                ],
                values=['New York City', 'Montréal'],
                id={'type': 'checklist', 'index': 0}
            )
        ], style={"border-color": "white"})
        
    def customize_footer(self):
        self.footer_lab = html.Div("Adding a footer", style={"border-color":"white"})

    @staticmethod
    def command_board_statistics():
        """
            Nos quedamos aquí (19/05/2023)
            Modificando el command board de statistics, queda pendiente agregar dropdowns que tomaran info de los archivos cargados y estilizar
        """
        cbs = html.Div([html.H4("TARJET"), html.H4("VARIABLE"), html.H4("GRAPH TYPE")], className="command_board")
        return cbs
    
    @staticmethod
    def command_board_sl():
        cbs = html.Div([html.H4("TARJET"), html.H4("MODELS"), html.H4("THIRD PART")], className="command_board")
        return cbs
    
    @staticmethod
    def command_board_dm():
        cbs = html.Div([html.H4("TARJET")], className="command_board")
        return cbs
    
    def wrap_lab(self):
        """
            Se requiere devolver como lista, no como html.Div() dash component
        """
        lab_card = [
        self.header_lab,
        self.command_board,
        self.customized_panel,
        self.body_lab,
        self.footer_lab
    ]
        return lab_card
    
        