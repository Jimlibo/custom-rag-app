"""
Created on 29 June 2024
@author: Dimitris Lymperopoulos
Description: A streamlit app that offers a gui to interact with a rag pipeline
"""

import streamlit as st
from DbPopulator.DbPopulator import DbPopulator
from utils.streamlit_utils import home_page, upload_documents, query_documents


def main():
    # add main page properties
    st.set_page_config(page_title="Custom RAG App", page_icon=":computer:", layout="wide")

    # create sidebar menu
    with st.sidebar:
        st.image("./Images/logo.png", width=200)
        st.title("Custom RAG App")
        choice = st.radio("Navigation", ["Home", "Upload Documents", "Query Documents", "Delete Documents"])
        st.write("")

    # create object to interact with the database
    db_populator = DbPopulator()

    if choice == "Home":
        home_page(db_populator)

    if choice == "Upload Documents":
        upload_documents(db_populator)

    if choice == "Query Documents":
        query_documents(db_populator)


if __name__ == "__main__":
    main()