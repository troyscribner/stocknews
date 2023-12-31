# -*- coding: utf-8 -*-

"""
stocknews.dataqueries.finhub_queries.py
---------
finhub_queries.py contains the queries related to downloading stock data from finhub


Created : 28 December 2023
Last Modified : 28 December 2023
"""


import time
import numpy as np
import pandas as pd
import json
import finnhub


def query_sp500_data():

    finnhub_client = finnhub.Client(api_key="")

    sp500_df = pd.read_csv("../data/sp500.csv")

    for symbol in sp500_df['Symbol'].tolist():
        # saved_data = json.load(open("../data/stockdata/%s.json" % symbol))
        try:
            saved_data = json.load(open("../data/stockdata/%s.json" % symbol))
            # text_and_reply.append(saved_data['market-overview']['data'])
            # text_and_reply.append(saved_data['market-overview']['data'])
        except:
            print(symbol)

            fin_data = finnhub_client.company_basic_financials(symbol, 'all')
            time.sleep(1.0)
            with open("../data/stockdata/%s.json" % symbol, "w") as outfile:
                json.dump(fin_data, outfile)


def build_finhub_df():

    sp500_df = pd.read_csv("../data/sp500.csv")

    columns = [
            #momentum
            '52WeekPriceReturnDaily', '3MonthADReturnStd', #'beta',

            #dividends
            'currentDividendYieldTTM', 'dividendGrowthRate5Y',

            #value
            'peBasicExclExtraTTM', 'pfcfShareTTM',

            #earnings growth
             'epsGrowth5Y', 'epsGrowthTTMYoy',

            #leverage
            'longTermDebt/equityQuarterly', 'netProfitMarginTTM',

            #profitability
            'roaTTM', 'roeTTM'
        ]

    data_df = pd.DataFrame(
        columns=columns
    )
    for symbol in sp500_df['Symbol'].tolist():
        try:
            saved_data = json.load(open("../data/stockdata/%s.json" % symbol))
            data = []
            for col in columns:
                try:
                    data.append(saved_data['metric'][col])
                except:
                    if col == 'dividendGrowthRate5Y':
                        data.append(0.0)
                    else:
                        data.append(np.nan)
            data_df.loc[symbol] = data
        except:
            print(symbol)

    for col in data_df.columns:
        data_df[col] = data_df[col].fillna(data_df[col].median())

    return data_df


if __name__ == "__main__":

    data_df = build_finhub_df()
    print(data_df)
    data_df.to_pickle("../data/polar_data_df.pkl")

    # data_df = pd.read_pickle("../data/polar_data_df.pkl")
    #
    # for col in data_df.columns:
    #     if col in ['3MonthADReturnStd', 'beta', 'peBasicExclExtraTTM', 'pfcfShareTTM', 'longTermDebt/equityQuarterly']:
    #         data_df[col] = data_df[col].rank(ascending=False, pct=True)
    #     else:
    #         data_df[col] = data_df[col].rank(pct=True)
    #
    # polar_data_df = []
    #
    # for col, val in data_df.loc['XOM'].items():
    #     percentiles = ["0.0-0.1", "0.1-0.2", "0.2-0.3", "0.3-0.4", "0.4-0.5",
    #                    "0.5-0.6", "0.6-0.7", "0.7-0.8", "0.8-0.9", "0.9-1.0"]
    #     percentiles.reverse()
    #     while val > 0:
    #         if val > 0.1:
    #             polar_data_df.append([col, percentiles.pop(), 0.1])
    #             val += -0.1
    #         else:
    #             polar_data_df.append([col, percentiles.pop(), val])
    #             val = 0
    #
    # polar_data_df = pd.DataFrame(polar_data_df, columns=['metric', 'percentile', 'value'])
    #
    # import plotly.express as px
    #
    # fig = px.bar_polar(polar_data_df, r="value", theta="metric", color="percentile", template="plotly_dark",
    #                    color_discrete_sequence=px.colors.sequential.Plasma_r)
    #
    # fig.show()

