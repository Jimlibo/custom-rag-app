"""
Created on 29 June 2024
@authro: Dimitris Lymperopoulos
Description: A script containing utility functions for streamlit content
"""

import os
import streamlit as st


def home_page():
    """
    A function that contains the content of the home page for the streamlit app.

    :return: None
    """

    st.title("Welcome to the Custom RAG App!")

    st.write("""
    This app offers a simple interface for creating and using a rag pipeline. You can create new vector 
    databases, upload your documents to them and use an llm to query those documents and get the most relevant 
    answer. You can also delete existing databases with a few clicks.
    """)

    st.write("""
    To get started, choose one of the options from the sidebar on the left.
    """)


def upload_documents(db_agent):
    """
    A function offers the gui for uploading documents to the vector database through streamlit.

    :param db_agent: a DbAgent object used to interact with vector databases
    :return: None
    """

    st.title("Upload Documents")

    st.write("""
    Upload your own documents in a vector database. You can choose to either upload a single
    document or multiple ones.
    """)

    # add uploader key as a way to reset file uploader after a certain button has been clicked
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0

    data_dir = "./Data"
    uploaded_files = st.file_uploader("Choose PDF files", type='pdf', accept_multiple_files=True,
                                      key=f"uploader_{st.session_state.uploader_key}")

    # save each uploaded file to the data directory
    if uploaded_files:
        for file in uploaded_files:
            with open(os.path.join(data_dir, file.name), 'wb') as f:
                f.write(file.getvalue())

    # allow user to choose to create a new database or choose from existing ones
    db_name = None
    db_type = st.radio("Create a new database or choose an existing one", ["New", "Existing"])

    if db_type == "New":
        db_name = st.text_input("Enter the name of the new database")
    else:
        db_list = os.listdir("./DBs")
        if len(db_list) == 0:
            st.warning("⚠️No existing databases found!")
        else:
            db_name = st.selectbox("Choose an existing database", db_list)

    # when upload button has been pressed, check if all necessary variables as set
    if st.button("Upload"):
        if uploaded_files and db_name:

            db_agent.set_db_path(os.path.join("./DBs", db_name))
            db_agent.set_data_path(data_dir)
            message = db_agent.populate_database()
            st.success(message)

            # reset chunks and documents of the db agent
            db_agent.clear_chunk_documents()

            # delete the uploaded files from the data folder
            for file in uploaded_files:
                os.remove(os.path.join(data_dir, file.name))

        elif not uploaded_files and db_name:
            st.warning("⚠️No files uploaded!")
        elif uploaded_files and not db_name:
            st.warning("⚠️No database name provided!")
        else:
            st.warning("⚠️Please choose at least one file to upload and provide a database name.")


def query_documents(db_agent, model):
    """
    A function offers the gui for querying documents in the vector database through streamlit.

    :param db_agent: a DbAgent object used to interact with vector databases
    :param model: a pretrained llm used for generating responses
    :return: None
    """

    st.title("Query Documents")

    st.write("""
    Use RAG to get the most relevant answer based on your query. Simply  specify the database you want to search and 
    type your query in the text box. You can also choose to get the sources for the response.
    """)

    # check if there are existing databases and allow user to choose one
    db_name = None
    db_list = os.listdir("./DBs")
    if len(db_list):
        db_name = st.selectbox("Choose a database", db_list)
    else:
        st.warning("⚠️No existing databases found!")

    # get the query from the user
    query = st.text_area("Enter your query:")

    get_sources = st.checkbox("Get sources for the response")

    if st.button("Generate Response"):
        if db_name and query:
            # get the rag prompt based on the query and the specified database
            db_agent.set_db_path(os.path.join("./DBs", db_name))
            input_prompt, results = db_agent.get_rag_prompt(query)

            # get the response from the llm
            response_text = model.invoke(input_prompt)

            if not get_sources:
                st.info(response_text)
            else:
                sources = [doc.metadata.get("id", None) for doc, _score in results]
                formatted_response = f"{response_text}\n\nSources: {sources}"
                st.info(formatted_response)

        elif not db_name and query:
            st.warning("⚠️No database has been selected")
        elif db_name and not query:
            st.warning("⚠️No query has been provided")
        else:
            st.warning("⚠️Please specify a database and enter a query")


def delete_documents(db_agent):
    """
    A function offers the gui for deleting existing vector databases through streamlit.

    :param db_agent: a DbAgent object used to interact with vector databases
    :return: None
    """

    st.title("Delete Documents")

    st.write("""
    Delete databases along with all the documents they contain. Simply choose the database you want to delete
    and click the delete button. You can also choose multiple databases to delete.
    """)

    # check that there are existing databases
    db_list = os.listdir("./DBs")
    if len(db_list) == 0:
        st.warning("⚠️No existing databases found!")
    else:
        dbs_to_delete = st.multiselect("Choose databases to delete", db_list)
        if st.button("Delete") and len(dbs_to_delete):

            # delete the selected databases
            for db_name in dbs_to_delete:
                db_agent.set_db_path(os.path.join("./DBs", db_name))
                db_agent.clear_database()
                st.success(f"✅ Database '{db_name}' has been deleted.")
