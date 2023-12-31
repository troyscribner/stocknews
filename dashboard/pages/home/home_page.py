# -*- coding: utf-8 -*-

"""
stocknews.dashboard.pages.home_page.py
---------


Created : 28 December 2023
Last Modified : 28 December 2023
"""


import dash
from dash import dcc
dash.register_page(__name__, path='/')


layout = dcc.Markdown('''
## **StockSavvy: Unveiling the Market with Dash and LangChain**

Welcome to StockSavvy, your AI-powered window into the financial world. Ever feel overwhelmed by the constant flood of news about your favorite stocks? Wish you had a personal assistant to decipher all the headlines and answer your burning questions? Look no further!

Forget static reports and one-dimensional analyses. StockSavvy leverages the cutting-edge combination of Plotly's Dash and LangChain to bring you an AI powered agent that dives deep into the top news surrounding any stock. No more skimming headlines—StockSavy reads, understands, and remembers the key takeaways, ready to distill market insights and answer your questions.

Why StockSavvy?
* Cut through the noise: Go beyond surface-level headlines and gain deeper understanding of market dynamics.
* Ask anything: Our AI agent can answer follow-up questions based on previous inquiries, fostering a natural conversation about your chosen stock.
* Stay informed: Get quick summaries of key news and real-time insights as new articles surface.
* Gain confidence: Make informed investment decisions based on a comprehensive understanding of market sentiment and trends.

Who is StockSavvy for?

* Individual investors: Whether you're a seasoned pro or a curious beginner, StockSavvy empowers you to navigate the market with clarity and confidence.
* Financial advisors: Enhance your client consultations with up-to-date, insightful analyses of their chosen stocks.
* Market researchers: Uncover hidden patterns and gain deeper understanding of market behavior through detailed news analysis.

Ready to dive deeper? Explore the features and see how StockSavvy can transform your relationship with the financial world. 

Before you begin, visit these two sites to get your OpenAI API key and AlphaVantage API Key:
* [OpenAI](https://platform.openai.com/playground) API Key. 
* [AlphaVantage](https://www.alphavantage.co/support/#api-key) API Key (Free key is available on signup.  Users may use "demo" as a key, although this will limit news stories to AAPL).

Remember, knowledge is power, let StockSavvy become your market advantage.

Continue by clicking on the "MARKET" tab in the left sidebar.

''')
