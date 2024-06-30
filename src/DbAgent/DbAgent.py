"""
Created on 28 June 2024
@author: Dimitris Lymperopoulos
Description: A script containing the class that will interact with the vector database
"""

import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate

from utils.utils import get_embedding_function, calculate_chunk_ids


class DbAgent:
    def __init__(self):
        # Initialize the DbAgent object with the necessary attributes
        self.db_path = None
        self.data_path = None
        self.documents = None
        self.chunks = None

    def set_db_path(self, db_path):
        """
        A function that sets the database path

        :param db_path: the path to the database
        """

        self.db_path = db_path

    def set_data_path(self, data_path):
        """
        A function that sets the data path

        :param data_path: the path to the data
        """

        self.data_path = data_path

    def load_documents(self):
        """
        A function that loads the documents from the specified data_path

        :return: DbAgent object
        """

        # check if data_path is file or directory and use the appropriate loader
        if os.path.isdir(self.data_path):
            document_loader = PyPDFDirectoryLoader(self.data_path)
        else:
            document_loader = PyPDFLoader(self.data_path)

        self.documents = document_loader.load()

        return self

    def split_documents(self):
        """
        A method that splits the documents into chunks

        :return: DbAgent object
        """

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False
        )

        self.chunks = text_splitter.split_documents(self.documents)

        return self

    def add_to_database(self):
        """
        A method that adds the previously generated chunks to the database

        :return: DbAgent object
        """

        # load the database
        db = Chroma(persist_directory=self.db_path, embedding_function=get_embedding_function())

        # calculate the chunk ids for the previously generated chunks
        chunks_with_ids = calculate_chunk_ids(self.chunks)

        # check existing items in the database
        existins_items = db.get(include=[])
        existing_ids = set(existins_items['ids'])
        print(f"Number of existing items in the Database: {len(existing_ids)}")

        # add the new chunks to the database
        new_chunks = []
        for chunk in chunks_with_ids:
            if chunk.metadata['id'] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks):
            new_chunk_ids = [chunk.metadata['id'] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
            db.persist()
            ret_message = f"✅ Added {len(new_chunks)} new items."

        else:
            ret_message = "✅ No new items to add."

        return ret_message

    def clear_database(self):
        """
        A method that clears the database
        """

        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)

    def clear_chunk_documents(self):
        """
        A method that clears the chunks and the documents.
        """

        self.documents = None
        self.chunks = None

    def populate_database(self):
        """
        A function that runs the entire pipeline to populate the vector database with the embeddings of the
        data files in the specified data path.

        :return: string message indicating the status of the operation
        """

        message = self.load_documents().split_documents().add_to_database()

        return message

    def get_rag_prompt(self, query_text):
        """
        A function that takes as input a text string and returns the appropriate input prompt based on similarity
        with the vector database's documents.

        :param query_text: string representing the question we want the llm to answer
        :return: string representing the input prompt to feed the llm and list of most similar items from the db
        """

        base_prompt_template = """
        Answer the question based only on the following context:

        {context}

        ---

        Answer the question based on the above context: {question}
        """

        # load the database
        db = Chroma(persist_directory=self.db_path, embedding_function=get_embedding_function())

        # Search the DB.
        results = db.similarity_search_with_score(query_text, k=5)

        # generate the appropriate input prompt for  llm
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(base_prompt_template)
        prompt = prompt_template.format(context=context_text, question=query_text)

        return prompt, results
