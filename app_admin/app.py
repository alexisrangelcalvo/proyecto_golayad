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
external_scripts = [
    "https://unpkg.com/dash.nprogress@latest/dist/dash.nprogress.js"]

app = Dash(name='app_superadmi',
           server=server,
           url_base_pathname='/Golayad/',
           # external_stylesheets=external_stylesheets,
           assets_url_path='..\assets',  # css
           suppress_callback_exceptions=True, update_title='Trabajando...', title='Golayad project', external_scripts=external_scripts
           )


app.layout = html.Div([
    # True para poder activar el intervalo en callback
    dcc.Location(id="url", refresh=True),
    dbc.Container(
        id="main_layout",
        children=[],
        fluid=True,
    )

])

# **************************************************************** CALLBACKS PARA LAYOUTS *****************************************************#


@ app.callback(Output('main_layout', 'children'),
               [Input('url', 'pathname')])  # vis1Cliente
def callback_layout(url):
    if url == "/Golayad/":
        return home_layout
        #raise PreventUpdate
