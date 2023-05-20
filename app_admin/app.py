# ULTIMA VERSION CON BOOTSTRAP THEME
from dash.exceptions import PreventUpdate
import numpy as np
import traceback
import statistics
import calendar
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import warnings
import plotly.graph_objs as go
import dash
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import trace
import random
from cmath import nan
from modulos.tools import *
import math
from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output
from modulos.server import *
from modulos.layouts import *
import dash_bootstrap_components as dbc
# from modulos.components import *
import pandas as pd
# import locale
# locale.setlocale(locale.LC_ALL, '')
# from dash_extensions import get_trigger
# from turtle import width
# import callbacks
# import modulos.tools
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
warnings.filterwarnings('ignore')


#********************************** LAYOUTS *****************************#

app = Dash(name='app_superadmi',
           server=server,
           url_base_pathname='/Golayad/',
           # external_stylesheets=external_stylesheets,
           assets_url_path='..\assets',  # css
           suppress_callback_exceptions=True, update_title='Trabajando...', title='Golayad project', external_stylesheets=[dbc.themes.BOOTSTRAP]
           )


url_content_layout = html.Div(children=[
    dcc.Location(id="url", refresh=False),
    dbc.Container(
        id="current_layout",
        children=[],
        fluid=True,
    )
])

app.validation_layout = html.Div([
    url_content_layout,
    home_layout,
    # second_layout,
    # third_layout
])

app.layout = url_content_layout

# **************************************************************** CALLBACKS PARA LAYOUTS *****************************************************#

@app.callback(Output(component_id="current_layout", component_property="children"), Input(component_id="url", component_property="pathname"))
def update_output_div(pathname):
    if pathname == "/Golayad/":
        return home_layout
    elif pathname == "/About-Alexis":
        return resume_layout
    elif pathname == "/Alexis-Lab":
        return lab_layout
    else:
        return home_layout
    

# **************************************************************** CALLBACKS DE LA APP *****************************************************#
@app.callback(Output("nav_bar", "children"), Input("url", "pathname"))
def update_output_div(pathname):
    if pathname == "/About-Alexis":
        return navbar_function("Alexis lab", "/Alexis-Lab")
    return navbar_function("About Alexis", "/About-Alexis")


@app.callback([Output("card_to_paint", "data"), Output("content_lab", "children"), Output("current_lab", "data")], Input(component_id={'type': 'dynamic-dpn-ctg', 'index': ALL}, component_property='n_clicks'), State("current_lab", "data"))
def update_lab_div(current_lab, previous_lab):
    if previous_lab is not None:
        """
            Cuando la lista previa de clicks sea diferente a None (Es None cuando no ha recibido ningun click),
            procede a encontrar la posición de la ultima tarjeta a la que se le dio click y enviar el indice de la tarjeta a un store para 
            que en un siguiente callback indique el cambio de color de tarjeta
        """
        index_change = encontrar_diferencia(current_lab, previous_lab) + 1

        
        if index_change == 1:
            """
                Cuando se selecciona statistics lab
            """
            cardLab = templateLab("Statistics Lab")
        elif index_change == 2:
            cardLab = templateLab("Supervissed learning Lab")
        elif index_change == 3:
            cardLab = templateLab("Unsupervissed learning")
        elif index_change == 4:
            cardLab = templateLab("Time series & forecasting")
        elif index_change == 5:
            cardLab = templateLab("Data mining")
        elif index_change == 6:
            cardLab = templateLab("Miscellaneous")

        cardLab.customize_command_board()

        
        return index_change, cardLab.wrap_lab(), current_lab
    else:
        return None, None, current_lab

# @app.callback(Output("Available_b1", "data"), Input("card_to_paint", "data"))
# def update_lab_div(current_lab, previous_lab):