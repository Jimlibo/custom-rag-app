"""
Created on 29 June 2024
@author: Dimitris Lymperopoulos
Description: A streamlit app that offers a gui to interact with a rag pipeline
"""

import os
import streamlit as st
from DbAgent.DbAgent import DbAgent
from utils.streamlit_utils import home_page, upload_documents, query_documents, delete_documents


def main():

    # create necessary directories if they do not exist
    if not os.path.exists("./Data"):
        os.makedirs("./Data")
    if not os.path.exists("./DBs"):
        os.makedirs("./DBs")

    # add main page properties
    st.set_page_config(page_title="Custom RAG App", page_icon=":computer:", layout="wide")

    # create sidebar menu
    with st.sidebar:
        st.image("./Images/logo.png", width=200)
        st.title("Custom RAG App")
        choice = st.radio("MENU", ["Home", "Upload Documents", "Query Documents", "Delete Documents"])
        st.write("")

    # create object to interact with the database
    db_agent = DbAgent()

    if choice == "Home":
        home_page(db_agent)

    if choice == "Upload Documents":
        upload_documents(db_agent)

    if choice == "Query Documents":
        query_documents(db_agent)

    if choice == "Delete Documents":
        delete_documents(db_agent)


if __name__ == "__main__":
    main()
