from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
from typing import Tuple, List
import numpy as np

"""
Global settings
"""
load_dotenv(find_dotenv()) # read local .env file
EMBEDDING_MODEL=os.environ.get("EMBEDDING_MODEL")
API_KEY = os.environ.get("API_KEY")

client = OpenAI(
    api_key=API_KEY
)

def generate_embeddings(text_list: List[str]) -> np.ndarray:
    response = client.embeddings.create(
        input=text_list,
        model=EMBEDDING_MODEL
    )
    embeddings = [np.array(e.embedding, dtype=np.float32) for e in response.data]
    return np.array(embeddings)