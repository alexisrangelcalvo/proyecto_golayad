from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from modulos.tools import *


home_layout = dbc.Container(
    html.Div([
        #Agregando un Header sobre dash
        html.Div([html.Div(html.Img(src="https://dash.gallery/dash-deck-explorer/assets/dash-logo.png", className="set-img1")), html.Div(html.H5(
            '', style={'color': 'white', 'font-family': 'Poppins'})), html.Img(src="https://www.vectorlogo.zone/logos/python/python-horizontal.svg", className="set-img1")], className='my_header'),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),


        #Agregando un contenedor de botones
        dbc.ButtonGroup(
        [
            dbc.Button("About Alexis Rangel Calvo", color="warning", size="lg", className="me-1", href="/About-Alexis", style={"font-size": "20px", "color":"white"}),
            dbc.Button("Alexis Business Science Lab", color="success", size="lg", href="/Alexis-Lab", style={"font-size": "20px"}),
        ], className="pair-button"),

        #Agregando un div con una frase que me describa
        html.Div([html.P("Alexis´s project", className="legend_2"), html.P('"Empower your business with cutting-edge automated reports and data science applications, revolutionizing the way you overcome challenges."', className="legend_1", style={"font-size":"20px"})]),
        html.Br(),
        

    ], className="home-layout"),
    fluid=True,
)

"""
    In resume layout is missin just connect social media bar & trigger the download full resume
    (17/05/2023)
"""

resume_layout = html.Div([
    html.Div(id="nav_bar"),

    dbc.Container(
    html.Div([
        html.Div([
            #html.H4("About me", className="legend_2"),
            html.Br(),
            card_introduction("Alexis Rangel Calvo", "I create automated reports and data science applications to tackle business challenges. I'm a continuous learning professional, whether it is Statistics, Economics or Programming, my goal is to apply this knowledge to solve real problems in financial industry. I'm keen to make business science & Graph Model Learning.", 
                              "Data analyst"),
            html.Div([button_download_resume(), social_bar()], style={"display":"flex", "align-items":"center"}),
            html.H5("Mail: alexisrangelcalvo@gmail.com", style={"margin-top":"5px", "text-align": "start"})
            ], style={"width":"45%"}),



        html.Div([
                    card_content("Software development & Databases", "Apps, dashboards, API's or Scripts development for process automation and CRUD & ETL using language Sql", html.Div([dbc.Badge("Python", color="warning", className="me-1"), dbc.Badge("Sql", color="success", className="me-1"), dbc.Badge("Linux", color="dark", className="me-1"), dbc.Badge("Git", color="danger", className="me-1")])),
                    card_content("Data & Risk Analyst", "Data extraction or data mining, data management, data analysis and big data. KPI's, financial ratios, study cash flow and vintage analysis", html.Div([dbc.Badge("Python", color="warning", className="me-1"), dbc.Badge("R", color="primary", className="me-1")])),
                    card_content("Statistic", "Exploratory data analysis, Descriptive and Inferencial statistics, Test hypothesis, Time series, Supervised learning and Explanatory Model Analysis", html.Div([dbc.Badge("Python", color="warning", className="me-1"), dbc.Badge("R", color="primary", className="me-1")])),
                    #card_content("Databases", "CRUD & ETL using language Sql"),
                    card_content("How all above works together?", 
                                 "One of my biggest professional experiences has been developing apps for instant credit analyst and processes automation like reports or visualizations (clients portfolio, assess the impact of credit politics or market campaign results) using python (dash and flask). It was a game changer in the nacional credit market agains long process that usually takes the credit asses of prospect profile due to fast response normally implies increase market share."),
                        
                        ], style={"width":"55%"})

    ], className="resume-layout"),
    fluid=True,
)
])


lab_layout = dbc.Container(
    html.Div([
        html.Div(id="nav_bar"),
        html.Br(),
        html.H4("My experience as business scientist", className="legend_2"),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content("Statistics", "lorem impsum",  badge_button("Available", "Available_b1", 1), "dark"))),
                dbc.Col(dbc.Card(card_content("Supervissed learning", "lorem ipsum", badge_button("Available", "Available_b2", 2), "dark"))),
                dbc.Col(dbc.Card(card_content("Unsupervissed learning", "Lorem ipsum", badge_button("Soon", "Soon_b1", 3), "dark"))),
            ]
        ),
        html.Br(),
        html.Br(),

        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content("Time series & forecasting", "Lorem ipsum", badge_button("Soon", "Soon_b2", 4), "dark"))),
                dbc.Col(dbc.Card(card_content("Data mining", "Lorem ipsum", badge_button("Available", "Available_b3", 5), "dark"))),
                dbc.Col(dbc.Card(card_content("Miscellaneous", "Lorem ipsum", badge_button("Soon", "Soon_b4", 6), "dark"))),
            ]
        ),
        html.Br(),
        html.Hr(style={"background-color": "white", "height": "4px", "border": "none"}),
        html.Div(id="content_lab"),
        dcc.Store(id="current_lab"),
        dcc.Store(id="card_to_paint"),
        html.Hr(style={"background-color": "white", "height": "4px", "border": "none"}),
        html.Br(),

        html.H5("¿Why and what's business science?", className="legend_2", style={"font-size":"30px"}),
        html.P("Lorem ipsum ipsum, Lorem ipsum ipsum, Lorem ipsum ipsum, Lorem ipsum ipsum, Lorem ipsum ipsum", className="legend_1"),

    ], className="home-layout"),
    fluid=True,
)
