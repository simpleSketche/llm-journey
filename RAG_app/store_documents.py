import faiss
from dotenv import load_dotenv, find_dotenv
import os
import numpy as np
from typing import Tuple, List
from data_embedding import generate_embeddings

load_dotenv(find_dotenv()) # read local .env file
DIMENSION = os.environ.get("DIMENSION")
print(DIMENSION)
heading_index = faiss.IndexFlatL2(1536)
subheading_index = faiss.IndexFlatL2(1536)

heading_texts = []
subheading_texts = []

def populate_faiss_indices(headings: List[str], subheadings: List[str]):
    global heading_texts, subheading_texts

    heading_embeddings = generate_embeddings(headings)
    subheading_embeddings = generate_embeddings(subheadings)

    heading_index.add(heading_embeddings)
    heading_texts.extend(headings)

    subheading_index.add(subheading_embeddings)
    subheading_texts.extend(subheadings)

    return heading_index, heading_texts, subheading_index, subheading_texts