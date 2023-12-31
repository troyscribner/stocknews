

import os

from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import DataFrameLoader
from langchain.document_loaders import JSONLoader
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.chat_models import ChatOpenAI
from dataqueries.alphavantage_queries import query_news


def df_loader(news_df):

    loader = DataFrameLoader(
        news_df,
        page_content_column="title"
    )

    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)

    retriever = db.as_retriever()

    news_tool = create_retriever_tool(
        retriever,
        "search_stock_news",
        "Searches and returns news dataframe.",
    )

    return news_tool

#
# def json_loader():
#     """
#     THIS DATA IS TOO LARGE FOR THE CURRENT MODEL, SO WOULD NEED ANOTHER WAY TO REDUCE BEFORE IT IS USABLE
#     """
#
#     symbol = "AAPL"
#
#     loader = JSONLoader(
#         file_path="data/stockdata/%s.json" % symbol,
#         jq_schema='.',
#         text_content=False
#     )
#     # loader = JSONLoader(
#     #     file_path='./example_data/facebook_chat.json',
#     #     jq_schema='.messages[].content',
#     #     text_content=False)
#
#     documents = loader.load()
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     texts = text_splitter.split_documents(documents)
#     embeddings = OpenAIEmbeddings()
#     db = FAISS.from_documents(texts, embeddings)
#
#     retriever = db.as_retriever()
#
#     metrics_tool = create_retriever_tool(
#         retriever,
#         "search_earnings",
#         "Searches and returns earnings and other metrics.",
#     )
#     return metrics_tool


def build_agent(news_df, openai_api_key):

    os.environ["OPENAI_API_KEY"] = openai_api_key

    news_tool = df_loader(news_df)
    # metrics_tool = json_loader()

    tools = [news_tool]

    llm = ChatOpenAI(temperature=0)
    agent_executor = create_conversational_retrieval_agent(llm, tools, verbose=False)

    return agent_executor

