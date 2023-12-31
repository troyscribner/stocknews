# -*- coding: utf-8 -*-

"""
stocknews.dashboard.pages.about..about_page.py
---------


Created : 28 December 2023
Last Modified : 28 December 2023
"""


import dash
from dash import dcc
dash.register_page(__name__, path='/about')


layout = dcc.Markdown('''
## **Troy Scribner**

StockSavvy was developed by Troy Scribner in 2023 for the [Dash-Langchain App Building Challenge](https://community.plotly.com/t/dash-langchain-app-building-challenge/79663/1).  

''')
