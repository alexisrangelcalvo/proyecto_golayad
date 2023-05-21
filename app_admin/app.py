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


@app.callback([Output("card_to_paint", "data"), Output("content_header_lab", "children"), Output("current_lab", "data")], Input(component_id={'type': 'dynamic-dpn-ctg', 'index': ALL}, component_property='n_clicks'), State("current_lab", "data"))
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

@ app.callback(
    Output('filename_lab', 'children'),
    [Input('upload_data_lab', 'contents')],
    [State('upload_data_lab', 'filename')],)
def reload_filename(contents, filename):
    """
        Callback que muestra y actualiza el estado de carga de archivos
    """
    if contents is None:
        return html.A(f'Drag and Drop or select your files here!')
    elif "xls" in  filename[0] or "xlsx" in  filename[0] or "pdf" in  filename[0]:
        return html.A(f'"{filename[0]}" file processed succesfully!')
    else:
        return html.A(f'"{filename[0]}" file was not processed succesfully!', style={"color":"red"})

@app.callback(Output('lab_files', 'data'),
              [Input('upload_data_lab', 'contents')],
              [State('upload_data_lab', 'filename'),
               State('upload_data_lab', 'last_modified')])
def loading_lab_files(list_of_contents, list_of_names, list_of_dates):
    """
        Callback que toma el archivo introducido por el usuario y lo almacena en una variable local de la interfaz del usuario como json
    """
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
    
@ app.callback(
    [Output('r1_c1_labs', 'children'), Output('r1_c2_labs', 'children'), Output('r1_c3_labs', 'children'), Output('r1_c4_labs', 'children'), Output('labDatatable_1', 'children')],
    [Input('lab_files', 'data')], [State('upload_data_lab', 'filename')])
def storing_loaded_files(data, filename):
    """
        Callback que toma los archivos almacenados por el usuario para la manipulación de datos y actualización del nivel 1 en body (despues de header )
    """
    if data is not None:
        if "xls" in filename[0] or "xlsx" in filename[0]:
            df = pd.read_json(data[0], orient='records')
            df_columns = df.columns.tolist()
            df.fillna(0, inplace=True)

            df2 = df.describe().transpose()
            initial_cols = [c for c in df2.columns]

            # Agregar variable y tipo de variable a df2, y formateando datos
            df2['Variable'] = df.apply(determinar_tipo_variable)
            df2['Tipo'] = df.dtypes
            df2['Tipo'] = df2['Tipo'].astype(str)
            for col in initial_cols:
                df2[col] = df2[col].apply(lambda x: f"{x:,.1}")
                
            # Renombrar las columnas para mayor claridad
            df2.reset_index(inplace=True)
            df2.rename(columns={'index':'Nombre', 'mean': 'Promedio', 'std': 'Desviación estándar', '25%': 'q1', '50%': 'q2', '75%': 'q3'}, inplace=True)

            datatable_2 = datatable_lab(df2) 

            dataset_info = html.H5("Dataset info: with changes")
            lista_graficas = ["Scatter plot", "Bar graph"]
            
            return dataset_info, dcc.Dropdown(df_columns, placeholder="Select tarjet", id="r1_c2_labs"), dcc.Dropdown(df_columns, placeholder="Select variable",  id="r1_c3_labs"), dcc.Dropdown(lista_graficas, placeholder="Select type of graph",  id="r1_c4_labs"), datatable_2
        if "pdf" in filename:
            """
                Habilitar para recibir pdfs y minar archivo
            """
            raise PreventUpdate
    raise PreventUpdate

@app.callback(
    [Output("new_dimensions_lab", "children"), Output("new_dimensions_lab", "style")],
    [Input('lab_files', 'data'), Input("switches_input_lab2", "value")],
)
def add_dimentions(data, switch):
    if data is None:
        raise PreventUpdate
    
    df = pd.read_json(data[0], orient='records')
    df_columns = df.columns.tolist()
    div = html.Div([
        html.Div([html.P("Color", style={"color":"white", "font-size":"12px", "margin-bottom":"-1px"}), dcc.Dropdown(df_columns, placeholder="Select color",  id="r1_c5_labs")], style={"width":"15%", "font-size":"12px"}), 
        html.Div([html.P("Size", style={"color":"white", "font-size":"12px", "margin-bottom":"-1px"}), dcc.Dropdown(df_columns, placeholder="Select size",  id="r1_c6_labs")], style={"width":"15%", "font-size":"12px"}), 
        html.Div([html.P("Hover", style={"color":"white", "font-size":"12px", "margin-bottom":"-1px"}), dcc.Dropdown(df_columns, placeholder="Select hover",  id="r1_c7_labs")], style={"width":"15%", "font-size":"12px"}),
    ], style={"display":"flex", "justify-content":"center"})
    if switch == [2]:
        return div, {}
    return div, {"display":"none"}

    
@ app.callback(
    [Output('labFigure_1', 'children')],
    [Input('lab_files', 'data'), Input('r1_c2_labs', 'value'), Input('r1_c3_labs', 'value'), Input('r1_c4_labs', 'value'), Input('r1_c5_labs', 'value'), Input('r1_c6_labs', 'value'), Input('r1_c7_labs', 'value'), Input('button_graph_1', 'n_clicks')])
def lab_figure(data, tarjet, variable, type_graph, color, size, hover_d, nclick):
    print(f"hover_d -> x={tarjet}, y={variable}, type={type_graph}")
    if nclick is not None and tarjet is not None and variable is not None:
        print("nclick")
        print(nclick)
        df = pd.read_json(data[0], orient='records')
        # creando la figura personalizada
        fig = px.scatter(df, x=tarjet, y=variable, color=color,
                 size=size, hover_data=[hover_d])
        fig.update_layout(
                            title="title_graph",
                            plot_bgcolor='rgba(0, 0, 0, 0)',
                            paper_bgcolor='rgba(0, 0, 0, 0)',
                            font=dict(
                                family="Poppins",
                                size=15,
                                color="white"
                            ),
                            showlegend=True,
                            legend=dict(
                                title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
                            )
                        )
        return [dcc.Graph(figure=fig)]
    raise PreventUpdate




    
    

#dff = pd.read_json(data[0], orient='records')