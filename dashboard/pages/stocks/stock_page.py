# -*- coding: utf-8 -*-

"""
stocknews.dashboard.pages.stock_page.py
---------
stock_page.py is the page containing stock information.


Created : 28 December 2023
Last Modified : 28 December 2023
"""
import datetime
import json
import numpy as np
import pandas as pd
from pandas.tseries.offsets import DateOffset

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import yfinance as yf

from flask import Flask, session
import dash
from dash import Input, Output, State, callback, html, dcc, clientside_callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from dataqueries.alphavantage_queries import query_news
from dataqueries.finhub_queries import build_finhub_df
from dashboard.pages.stocks.stock_plots import plot_polar
from dashboard.pages.stocks.chatbox import generate_ai_bubble, generate_user_bubble

from langchain_logic.lc_agent import build_agent
from dashboard.pages.stocks.chatbox import chat_div

dash.register_page(__name__, path='/market')


news_df = query_news("AAPL", "demo")
news_df['relevance'] = np.round(news_df['relevance'].astype(float), 3)
news_df['sentiment'] = np.round(news_df['sentiment'].astype(float), 3)

sp500_df = pd.read_csv("data/sp500.csv", index_col=0)
symbols = sorted(sp500_df['Symbol'].tolist())


def left_column():
    return dbc.Col(
        [
            dmc.Stack(
                children=[
                    dmc.TextInput(
                        label="OpenAI API Key",
                        id="openai-api-key",
                        placeholder="Your chat-gpt api_key:", style={"width": 500},
                        persistence="local",
                        type="password"
                    ),
                    dmc.TextInput(
                        label="Alphavantage API Key",
                        id="alphavantage-api-key",
                        style={"width": 500},
                        placeholder="Your alphavantage api_key.  If no key, use 'demo' for AAPL only:",
                        value="demo",
                        persistence="local",
                        type="password"
                    ),
                    dmc.Select(
                        id="symbol-select",
                        data=symbols,
                        value="AAPL",
                        style={"width": 200},
                        searchable=True,
                        icon=DashIconify(icon="radix-icons:magnifying-glass"),
                        rightSection=DashIconify(icon="radix-icons:chevron-down"),
                    ),
                    chat_div,

                    dmc.Textarea(
                        id="input-textarea",
                        placeholder="Enter your prompt here.",
                        autosize=False,
                        radius='md',
                        minRows=2,
                        maxRows=2,
                    ),
                    dmc.Button("Submit prompt to LLM", id="loading-button"),
                ],
            )
        ],
        width=5,
        # className="g-0",
        style={}
    )


def build_ag_grid(
        id,
        df,
        columnDefs,
        height='32vh',
        rowHeight=None,
        headerHeight=None,
        width=None,
        columnSizeOptions=None
):

    defaultColDef = {
        "filter": False,
        "resizable": True,
        "sortable": False,
        "editable": False,
        "floatingFilter": False,
        "tooltipComponent": "CustomTooltip",
        # "minWidth": 125,
    }

    style = {}
    if height:
        style['height'] = height
    if width:
        style['width'] = width

    dashGridOptions = {"undoRedoCellEditing": True, "rowSelection": "single", "tooltipShowDelay": 100}
    if rowHeight:
        dashGridOptions['rowHeight'] = rowHeight
    if headerHeight:
        dashGridOptions['headerHeight'] = headerHeight

    if columnSizeOptions:
        pass
    else:
        columnSizeOptions = {
            # 'defaultMinWidth': 100,
            'columnLimits': [{'key': 'id', 'maxWidth': 10}],
        },

    return dag.AgGrid(
        id=id,
        className="ag-theme-alpine",
        columnDefs=columnDefs,
        rowData=df.to_dict("records"),
        defaultColDef=defaultColDef,
        # cellStyle=cellStyle,
        dangerously_allow_code=True,
        dashGridOptions=dashGridOptions,
        style=style,
        columnSize="sizeToFit",
        # columnSizeOptions=columnSizeOptions,

    )


def right_column():
    return dbc.Col(
        [
            # dmc.LoadingOverlay(
            #     id="loading-customize-output",
            #     children=[
            #         dcc.Graph(id="market-treemap", style={"margin": 0, "height": "86vh", }),
            #     ],
            #     loaderProps={"variant": "dots", "color": "orange", "size": "xl"},
            # ),
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Metrics", value="metrics", style={'height': '4vh'}),
                            # dmc.Tab("Treemap", value="treemap", style={'height': '4vh'}),
                            dmc.Tab("Price", value="prices", style={'height': '4vh'}),
                            # dmc.Tab("Prices Min", value="prices-min", style={'height': '4vh'}),
                        ]
                    ),
                    dmc.TabsPanel(
                        children=dcc.Graph(
                            id="metrics-graph",
                            style={"margin": 0, 'height': '50vh'},
                        ),
                        id='metrics-tab',
                        value="metrics"),
                    # dmc.TabsPanel(
                    #     children=dcc.Graph(
                    #         id="treemap-graph",
                    #         style={"margin": 0, 'height': '50vh'},
                    #     ),
                    #     id='treemap-tab',
                    #     value="treemap"),
                    dmc.TabsPanel(
                        children=dcc.Graph(
                            id="stock-day-graph",
                            style={"margin": 0, 'height': '50vh'},
                        ),
                        id='prices-tab',
                        value="prices"),
                    # dmc.TabsPanel(
                    #     children=dcc.Graph(
                    #         id="prices-min-graph",
                    #         style={"margin": 0, 'height': '50vh'}
                    #     ),
                    #     id='prices-min-tab',
                    #     value="prices-min"),
                ],
                value="metrics",
                color="blue",
                orientation="horizontal",
            ),

            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("News", value="news", style={'height': '4vh'}),
                            # dmc.Tab("Graph Inputs", value="graph", style={'height': '4vh'}),
                        ]
                    ),
                    dmc.TabsPanel(
                        children=build_ag_grid(

                            id="news-grid",
                            # df=pd.DataFrame(),
                            df=news_df[['title', 'summary', 'url', 'relevance', 'sentiment']],
                            columnDefs=[
                                # {'field': 'index', 'width': 10, 'suppressSizeToFit': True},
                                {'field': 'title', "filter": "agTextColumnFilter", "floatingFilter": True,
                                 "floatingFilterComponentParams": {"suppressFilterButton": True},
                                 "tooltipField": 'title',
                                 "tooltipComponent": "CustomTooltip"
                                 },
                                {'field': 'url', 'cellRenderer': 'markdown', 'width': 80},
                                {'field': 'relevance', 'width': 50},
                                {'field': 'sentiment', 'width': 50},
                            ],
                            height='34vh',
                            rowHeight=24,
                            headerHeight=24,
                        ),
                        id='news-tab',
                        value="news"),
                ],
                value="news",
                color="blue",
                orientation="horizontal",
            ),

        ],
        width=7,
        # className="g-0",
        style={'margin-left': 0, 'buffer-right': 0}
    )


layout = dbc.Row(
    [
        left_column(),
        right_column()
    ],
    # className="g-0",
)


clientside_callback(
    """
    function updateLoadingState(n_clicks) {
        return true
    }
    """,
    Output("loading-button", "loading", allow_duplicate=True),
    Input("loading-button", "n_clicks"),
    prevent_initial_call=True,
)


@callback(
    Output("chat-history", "children"),
    Output("input-textarea", "value"),
    Output("loading-button", "loading"),
    State("chat-history", "children"),
    State("input-textarea", "value"),
    Input("loading-button", "n_clicks"),
    prevent_initial_call=True,
)
def add_chat_card(chat_history, input_text, n_clicks):
    if input_text is None or input_text == "":
        raise dash.exceptions.PreventUpdate

    global agent

    try:
        result = agent({"input": input_text})

        # # create the users prompt card
        user_card = generate_user_bubble(input_text)
        ai_card = generate_ai_bubble(result["output"])
        chat_history.append(user_card)
        chat_history.append(ai_card)

    except:
        user_card = generate_user_bubble(input_text)
        ai_card = generate_ai_bubble("Unable to generate a resonse. Reenter OpenAI API Key and refresh page.")
        chat_history.append(user_card)
        chat_history.append(ai_card)

    return chat_history, "", False


@callback(
    Output("metrics-graph", "figure"),
    Input("symbol-select", "value"),
)
def metrics_graph(symbol):
    fig = plot_polar(symbol)

    return fig


@callback(
    Output("stock-day-graph", "figure"),
    Input("symbol-select", "value"),
)
def update_indicator(symbol):

    today = datetime.datetime.now()
    day_start_date = today - DateOffset(months=24)

    prices_day_df = yf.download(symbol,
                     start=day_start_date,
                     end=today,
                     progress=True,
                     interval='1d',
                     )['Adj Close']

    prices_day_df = pd.concat([prices_day_df], axis=1, keys=[symbol])

    fig = make_subplots(1, 1,
                        subplot_titles=[
                            # 'Regression p-values',
        ],
                        # specs=[[{"secondary_y": True}]],

                        )

    for col in prices_day_df.columns:
        fig.add_trace(
            go.Scatter(
                x=prices_day_df.index,
                y=prices_day_df[col].values,
                mode="lines",
                name=col,
            ),
            # secondary_y=True,
            row=1,
            col=1)

    fig.update_layout(
        autosize=True,
        showlegend=True,
        margin=dict(l=20, r=20, t=20, b=20),
        # padding=dict(b=20),
        paper_bgcolor="LightSteelBlue",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.00,
            xanchor="left",
            x=0
        )
    )

    return fig


@callback(
    Output("news-grid", "rowData"),
    State("news-grid", "rowData"),
    State("alphavantage-api-key", "value"),
    State("openai-api-key", "value"),
    Input("symbol-select", "value"),

)
def news_grid(rowData, alphavantage_api_key, openai_api_key, symbol):
    global agent
    global text_and_reply

    text_and_reply = []

    df = query_news(symbol, alphavantage_api_key)
    df['relevance'] = np.round(df['relevance'].astype(float), 3)
    df['sentiment'] = np.round(df['sentiment'].astype(float), 3)

    df = df[['title', 'summary', 'url', 'relevance', 'sentiment']]

    try:
        agent = build_agent(df, openai_api_key)
    except:
        pass

    return df.to_dict("records")


