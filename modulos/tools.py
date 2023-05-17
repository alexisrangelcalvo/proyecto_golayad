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


def button_client(client, coacred, id_num, color):
    #print(f"color -> {color}")
    # id_num prop es unica para cada boton

    if coacred is not None:
        # print(coacred)
        # print(type(coacred))
        div = html.Div([dbc.Button(
            id={
                'type': 'dynamic-dpn-ctg',
                'index': id_num}, type='submit',
            children=client,  className=f'client_button2_nc {color} coac_head'), dbc.Button(id=f'coacred_button {coacred}', type='submit',
                                                                                            children='Coacreditado', className='client_button3'),
            dbc.Popover(
            [
                dbc.PopoverHeader(
                    f"El cliente {client} es asociado con el coacreditado"),
                dbc.PopoverBody(
                    f" -> {coacred}"),
            ],
            target=f'coacred_button {coacred}',
            trigger="click",
            style={'background-color': 'white', 'border': 'solid',
                   'border-color': 'gray', 'border-radius': '5px', 'font-family': 'Poppins'}
        )], style={'display': 'flex', 'widht': '100%', 'height': '50%', 'justify-content': 'space-around', 'margin': 'auto'}
        )

    else:
        leng = "coac_head" if len(client) > 60 else "client_head"
        div = html.Div([dbc.Button(id={
            'type': 'dynamic-dpn-ctg',
            'index': id_num}, type='submit',
            children=client, className=f'client_button2_nc {color} {leng}')], style={'display': 'flex', 'widht': '100%', 'height': '50%', 'justify-content': 'center', 'margin': 'auto'}
        )
    return div


def metrica_cliente(cliente, bin1, bin2, shortcut_key, metricas_mul, coacred, id_num):

    bin1List = []
    n = 0
    for e in bin1:
        if e == 1:
            # Cuando cumple, se le dará el estilo y color verde a la casilla (Si es una metrica seleccionada en la tabla de shortcuts, la letra sera de otro color)
            if metricas_mul[n] == shortcut_key:
                #print(f'bin1 == {metricas_mul[n]}, {shortcut_key}')
                #print(f'{metricas_mul[n]} == {shortcut_key}')
                bin1List.append('grid-box-color-2_1')
            else:
                bin1List.append('grid-box-color-2')
        elif e == 0:
            # Cuando no cumple, se le dará el estilo y color rojo a la casilla
            if metricas_mul[n] == shortcut_key:
                #print(f'{metricas_mul[n]} == {shortcut_key}')
                bin1List.append('grid-box-color-1_1')
            else:
                bin1List.append('grid-box-color-1')
        n += 1

    n = 0
    bin2List = []
    for e in bin2:
        if e == 1:
            # Cuando cumple, se le dará el estilo y color verde a la casilla
            if metricas_mul[n] == shortcut_key:
                #print(f'bin2 == {metricas_mul[n]}, {shortcut_key}')
                bin2List.append('grid-box-color-2')
            else:
                bin2List.append('grid-box-color-2')
        elif e == 0:
            # Cuando no cumple, se le dará el estilo y color rojo a la casilla
            if metricas_mul[n] == shortcut_key:
                #print(f'{metricas_mul[n]} == {shortcut_key}')
                bin2List.append('grid-box-color-1')
            else:
                bin2List.append('grid-box-color-1')
        n += 1

    cuadricula0 = html.Div([html.Div(html.H5('FE'), className=bin1List[0]), html.Div(html.H5('AS'), className=bin1List[1]), html.Div(html.H5('DB'), className=bin1List[2]),
                            html.Div(html.H5('AP'), className=bin1List[3]), html.Div(html.H5('RMY'), className=bin1List[4]), html.Div(html.H5('RMN'), className=bin1List[5]), html.Div(html.H5('RF'), className=bin1List[6]), html.Div(html.H5('HHI'), className=bin1List[7]), html.Div(html.H5('AE'), className=bin1List[8]), html.Div(html.H5('DFC'), className=bin1List[9])], className='grid-box2')

    cuadricula1 = html.Div([html.Div(html.H5('FE'), className=bin2List[0]), html.Div(html.H5('AS'), className=bin2List[1]), html.Div(html.H5('DB'), className=bin2List[2]),
                            html.Div(html.H5('AP'), className=bin2List[3]), html.Div(html.H5('RMY'), className=bin2List[4]), html.Div(html.H5('RMN'), className=bin2List[5]), html.Div(html.H5('RF'), className=bin2List[6]), html.Div(html.H5('HHI'), className=bin2List[7]), html.Div(html.H5('AE'), className=bin2List[8]), html.Div(html.H5('DFC'), className=bin2List[9])], className='grid-box')

    #print(f"bin2 -> {bin2} -> sum  {sum(bin2)}")
    # if sum(bin2) >= 4:
    #     color = "red_color"
    if sum(bin2) <= 5:  # con 5 rojos
        color = "red_color"
    elif sum(bin2) == 7 or sum(bin2) == 6:  # con 3 o 4 rojos
        color = "yellow_color"
    else:
        color = "blue_color"
    div = html.Div([

        html.Div([button_client(cliente, coacred, id_num, color)], style={
                 'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'width': '320px', 'margin': 'auto', 'padding-top': '5px', 'margin-bottom': '5px'}),

        html.Div([

            html.Div([html.Div([html.H4('CRITERIOS DE APROBACIÓN DE MES BASE', style={'display': 'flex', 'flex': '1', 'text-align': 'center', 'color': 'white', 'font-size': 10, 'height': '50%', 'margin': 'auto', 'justify-content': 'center', 'align-items': 'center'}),
                                ], className='mainFlex-box')]),

            html.Div([html.Div([html.H4('PROMEDIO U3M', style={'display': 'flex', 'flex': '1', 'padding-top': '2%', 'color': 'white', 'font-size': 10, 'height': '50%', 'margin': 'auto', 'justify-content': 'center', 'align-items': 'center'}),
                                ], className='mainFlex-box')]),

        ], className='mainFlex'),

        html.Div([cuadricula0, cuadricula1], className='mainFlex')


    ], className='mainContainer')

    return div


modal = html.Div(
    [
        dbc.Button("Diseña tu estudio de crédito",
                   id="open", style={'width': '250px'}),


        dbc.Modal([
            dbc.ModalHeader("Diseña tu estudio de crédito"),
            dbc.ModalBody([
                html.P(
                    'Selecciona las opciones acorde al cliente que le deseas realizar el estudio de crédito'),
            ]
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="close", className="ml-auto")
            ),
        ],
            id="modal",
            is_open=False,    # True, False
            size="sm",        # "sm", "lg", "xl"
            backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
            scrollable=True,  # False or True if modal has a lot of text
            centered=True,    # True, False
            fade=True         # True, False
        ),
    ]
)
