"""
Created on 28 June 2024
@author: Dimitris Lymperopoulos
Description: A script containing utility functions
"""

from langchain_community.embeddings.huggingface import HuggingFaceBgeEmbeddings
from torch.cuda import is_available


def get_embedding_function():
    """
    A function that returns the embedding function used for the project.

    :return: embedding function
    """

    model_name = 'Alibaba-NLP/gte-large-en-v1.5'
    model_kwargs = {
        'device': 'cuda' if is_available() else 'cpu',
        'trust_remote_code': True
    }

    hfe = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
    )

    return hfe


def calculate_chunk_ids(chunks):
    """
    A function that calculates the chunk ids based on filename, page and chunk number of each chunk.

    :param chunks: list of chunks
    :return: list of chunks with updated metadata
    """

    last_page_id = None
    current_chunk_idx = 0

    for chunk in chunks:
        source = chunk.metadata.get('source')   # returns the filename from which the chunk was extracted
        page = chunk.metadata.get('page')       # returns the page number from which the chunk was extracted
        current_page_id = f"{source}:{page}"    # shows in which page of which document the chunk is in

        # if the page ID is the same as the last one, increment the chunk index
        if current_page_id == last_page_id:
            current_chunk_idx += 1
        else:
            current_chunk_idx = 0

        # calculate the chunk id and update the last_page_id
        chunk_id = f"{current_page_id}:{current_chunk_idx}"
        last_page_id = current_page_id

        # add it to the page metadata
        chunk.metadata['id'] = chunk_id

    return chunks
