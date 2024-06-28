"""
Created 28 June 2024
@author: Dimitris Lymperopoulos
Description: A script containing utility functions
"""

from langchain_community.embeddings.huggingface import HuggingFaceBgeEmbeddings


def get_embedding_function():
    """
    A function that returns the embedding function used for the project.

    :return: embedding function
    """

    model_name = 'Alibaba-NLP/gte-large-en-v1.5'
    model_kwargs = {
        'device': 'cpu',
        'trust_remote_code': True
    }

    hfe = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
    )

    return hfe
