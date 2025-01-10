import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationTokenBufferMemory

"""
Global settings
"""
_ = load_dotenv(find_dotenv()) # read local .env file
api_key=os.environ.get("API_KEY")

llm_model_type = "gpt-4o-mini"

model = ChatOpenAI(
    temperature=0.0, # randomness value
    model=llm_model_type, # define the api model
    streaming=True, # for chunking purpose
    openai_api_key=api_key # where your wallet is bleeding
)

# Initialize memory
memory = ConversationTokenBufferMemory(
    max_token_limit=200,
    llm = model
)

# Initialize conversation
conversation = ConversationChain(
    llm = model,
    memory = memory,
    verbose=True
)

# define roles
message_history = [
    {
        "role": "system", "content": "you are a helpful assistant!"
    }
]

# running the bot!
print("The bot is ready....")
while True:

    # get user input
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # add user message to the history
    message_history.append({"role": "user", "content": user_input})
    
    # get the response from the model
    try:
        response = conversation.predict(input=user_input)
        print(f"Assistant: {response}")
        
        # Add assistant response to the history
        message_history.append({"role": "assistant", "content": response})
    except Exception as e:
        print(f"Error: {e}")