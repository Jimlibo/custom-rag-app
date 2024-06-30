"""
Created on 29 June 2024
@authro: Dimitris Lymperopoulos
Description: A script containing utility functions for streamlit content
"""

import os
import streamlit as st


def home_page(db_agent):
    pass


def upload_documents(db_agent):
    """
    A function offers the gui for uploading documents to the vector database through streamlit.

    :param db_agent: a DbPopulator object used to interact with vector databases
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

    if st.button("Upload") and uploaded_files and db_name:

        db_agent.set_db_path(os.path.join("./DBs", db_name))
        db_agent.set_data_path(data_dir)
        message = db_agent.rag_pipeline()
        st.success(message)

        # reset chunks and documents of the db agent
        db_agent.clear_chunk_documents()

        # delete the uploaded files from the data folder
        for file in uploaded_files:
            os.remove(os.path.join(data_dir, file.name))


def query_documents(db_agent):
    pass


def delete_documents(db_agent):
    """
    A function offers the gui for deleting existing vector databases through streamlit.

    :param db_agent: a DbPopulator object used to interact with vector databases
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
