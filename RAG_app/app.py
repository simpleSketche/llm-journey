from pdf_extractor import extract_from_pdf_pages, extra_headings_subheadings
from openai import OpenAI
import os
from dotenv import find_dotenv, load_dotenv
from store_documents import populate_faiss_indices
from data_embedding import generate_embeddings
from store_documents import populate_faiss_indices
from typing import Tuple, List

load_dotenv(find_dotenv())
QA_MODEL = os.environ.get("QA_MODEL")
API_KEY = os.environ.get("API_KEY")

# Tip: if the pdf you found is shown in the pdf viewer on a website,
# open the dev Element inspector, and find the html element class named / id named -> "download",
# it's hidden by default, add / change the display style property to "inline" from "hidden".
pdf_file_path = "pdf_data/2022BC_NYC_BuildingCodes_Definitions.pdf"

client = OpenAI(
    api_key=API_KEY
)

def classify_query(query: str) -> str:
    prompt = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Classify the user's question as either "
                    "'broad' or 'specific'. A broad question asks for general or high-level "
                    "information, while a specific question seeks detailed, precise, or technical information. "
                    "Provide only the classification."
                ),
            },
            {"role": "user", "content": query},
        ]
    response = client.chat.completions.create(
        model=QA_MODEL,
        messages=prompt,
        max_tokens=10
    )
    return response.choices[0].message

def search_vector_space(query: str, query_type: str, headings, subheadings, k: int = 5):
    query_embedding = generate_embeddings([query])[0].reshape(1, -1)
    heading_index, heading_texts, subheading_index, subheading_texts = populate_faiss_indices(headings, subheadings)

    if query_type.content == "broad":
        distances, indices = heading_index.search(query_embedding, k)
        return [heading_texts[i] for i in indices[0] if i < len(heading_texts)]
    elif query_type.content == "specific":
        distances, indices = subheading_index.search(query_embedding, k)
        return [subheading_texts[i] for i in indices[0] if i < len(subheading_texts)]
    else:
        return []

def generate_answer(query: str, context: List[str]):
    context_text = "\n".join(context)
    prompt = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Use the given context to answer the user's "
                    "question in a clear and concise way."
                ),
            },
            {"role": "system", "content": f"Context:\n{context_text}"},
            {"role": "user", "content": query},
        ]
    response = client.chat.completions.create(
        model=QA_MODEL,
        messages=prompt,
        max_tokens=200
    )
    return response.choices[0].message

def run(user_query: str):
    pages = extract_from_pdf_pages(pdf_file_path)
    headings, subheadings = extra_headings_subheadings(pages)

    query_type = classify_query(user_query)

    # Retrieve relevant content
    context = search_vector_space(user_query, query_type, headings, subheadings)

    if context:
        return generate_answer(user_query, context)
    else:
        return "Sorry, I couldn't find relevant information to answer your question."

if(__name__ == "__main__"):
    # running the bot!
    print("The bot is ready....")
    while True:

        # get user input
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # add user message to the history
        # message_history.append({"role": "user", "content": user_input})
        
        # get the response from the model
        try:
            response = run(user_input)
            print(f"Assistant: {response.content}")
            
            # Add assistant response to the history
            # message_history.append({"role": "assistant", "content": response})
        except Exception as e:
            print(f"Error: {e}")