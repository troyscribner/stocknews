# StockNews
StockNews combines Plotly Dash with LangChain and ChatGPT in order to answer questions about current stock market news for companies in the S&P500.  

## Description

StockNews queries news stories from AlphaVantage, provides earnings metrics from Finhub, and synthesizes this data into a conversational agent using LangChain with ChatGpt models at the core.  

## Getting Started

In order to access the full functionality of StockNews, users will need the following:
* ChatGPT API key (User must supply their own API key for ChatGPT):  https://openai.com
* AlphaVantage API key for news (Free api key with 25 queries per day limit is availalbe.  User can also use "demo" as api key, but only for 'AAPL' ticker queries).  https://www.alphavantage.co/

### Installing

* Clone repo from https://github.com/troyscribner/stocknews
* Install requirements with `pip3 install -r requirements.txt`

### Executing program

* Run python stocknews/app.py
* Access program from `http://localhost:8050/`
* Enter OpenAI API key in OpenAI Key Field
* Enter AlphaVantage API key or "demo" in AlphaVantage Field

## Authors

Troy Scribner 

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
