# -*- coding: utf-8 -*-

"""
stocknews.dashboard.pages.stocks.chatbox.py
---------
chatbox.py


Created : 28 December 2023
Last Modified : 28 December 2023
"""


from dash import Input, Output, State, callback, html, dcc, clientside_callback
import dash_bootstrap_components as dbc


def generate_user_bubble(text):

    return dbc.Card(
        dcc.Markdown(text),
        style={
        "width": "max-content",
        "font-size": "14px",
        "padding": "0px 0px",
        "border-radius": 15,
        "margin-bottom": 5,
        "margin-left": "auto",
        "margin-right": 0,
        "max-width": "80%",
    },
        body=True,
        color="#357ED5",
        inverse=True
    )


def generate_ai_bubble(text):

        return dbc.Card(
            dcc.Markdown(text),
            style={
            "width": "max-content",
            "font-size": "14px",
            "padding": "0px 0px",
            "border-radius": 15,
            "margin-bottom": 5,
            "margin-left": 0,
            "margin-right": "auto",
                "max-width": "80%",
        },
            body=True,
            color="#F5F5F5",
            inverse=False,
        )


chat_div = html.Div(
    html.Div(id="chat-history",
             children=[
                 generate_ai_bubble("Enter API keys before entering your prompt.  Select stock symbol above to focus your information on recent market news pertaining to a given stock.  Then enter questions in the prompt below."
                 )
             ]
             ),
    style={
        "overflow-y": "auto",
        "display": "flex",
        "height": "47vh",
        "flex-direction": "column-reverse",
    },
)

