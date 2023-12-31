# -*- coding: utf-8 -*-

"""
stocknews.dashboard.pages.stocks.stock_plots.py
---------
stock_plots.py contains plot logic for the stocks page.


Created : 30 December 2023
Last Modified : 30 December 2023
"""


import pandas as pd
import plotly.express as px


def plot_polar(symbol):

    data_df = pd.read_pickle("data/polar_data_df.pkl")

    columns = ['1Y Return', '3M Volatility', 'Beta',
       'Dividend Yield', '5Y Dividend Growth',
       'P/E', 'P/FCF', '5Y EPS Growth', '12M EPS Growth',
       'Debt/Equity', 'Net Profit Margin', 'Return on Assets',
       'Return on Equity']
    data_df.columns = columns
    del data_df['Beta']

    for col in data_df.columns:
        if col in ['3MonthADReturnStd', 'beta', 'peBasicExclExtraTTM', 'pfcfShareTTM', 'longTermDebt/equityQuarterly']:
            data_df[col] = data_df[col].rank(ascending=False, pct=True)
        else:
            data_df[col] = data_df[col].rank(pct=True)

    polar_data_df = []
    for col, val in data_df.loc[symbol].items():
        percentiles = ["0.0-0.1", "0.1-0.2", "0.2-0.3", "0.3-0.4", "0.4-0.5",
                       "0.5-0.6", "0.6-0.7", "0.7-0.8", "0.8-0.9", "0.9-1.0"]
        percentiles.reverse()
        while val > 0:
            if val > 0.1:
                polar_data_df.append([col, percentiles.pop(), 0.1])
                val += -0.1
            else:
                polar_data_df.append([col, percentiles.pop(), val])
                val = 0

    polar_data_df = pd.DataFrame(polar_data_df, columns=['metric', 'percentile', 'value'])
    fig = px.bar_polar(polar_data_df, r="value", theta="metric", color="percentile", template="plotly_dark",
                       color_discrete_sequence=px.colors.sequential.Plasma_r)

    fig.update_layout(
        # polar=dict(
        #     radialaxis=dict(visible=True, range=[0, 1]),  # Set radial axis range
        #     # angularaxis=dict(rotation=90, direction="clockwise"),  # Adjust angle axis
        # ),
        title="%s Stock Relative to S&P500 Companies" % symbol,
    )

    return fig

