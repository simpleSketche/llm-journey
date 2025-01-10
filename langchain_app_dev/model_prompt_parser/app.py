import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from langchain.output_parsers import StructuredOutputParser

from resp_schema import response_schemas


"""
Global settings
"""
_ = load_dotenv(find_dotenv()) # read local .env file
api_key=os.environ.get("API_KEY")

llm_model = "gpt-4o-mini"


chat = ChatOpenAI(
    temperature=0.0, # randomness value
    model=llm_model, # define the api model
    streaming=True, # for chunking purpose
    openai_api_key=api_key # where your wallet is bleeding
    )

# instruction for the LLM, tell it what to do and how to structure the response
review_template = """\
For the following text, extract the following information:

gift: Was the item purchased as a gift for someone else? \
Answer True if yes, False if not or unknown.

delivery_days: How many days did it take for the product \
to arrive? If this information is not found, output -1.

price_value: Extract any sentences about the value or price,\
and output them as a comma separated Python list.

Format the output as JSON with the following keys:
gift
delivery_days
price_value

text: {text}
"""

# user input string
customer_review = """\
This leaf blower is pretty amazing.  It has four settings:\
candle blower, gentle breeze, windy city, and tornado. \
It arrived in two days, just in time for my wife's \
anniversary present. \
I think my wife liked it so much she was speechless. \
So far I've been the only one using it, and I've been \
using it every other morning to clear the leaves on our lawn. \
It's slightly more expensive than the other leaf blowers \
out there, but I think it's worth it for the extra features.
"""

# create the prompt template
prompt_template = ChatPromptTemplate.from_template(review_template)

# initialize the json parser from predefined schemas
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

# get the 
messages = prompt_template.format_messages(
    text=customer_review,
    format_instructions=format_instructions
)
response = chat.stream(messages) # mimic openapi web experience, returning chunks one at a time

resp_message =""
for chunk in response:
    print(chunk.content, end="")
    resp_message += chunk.content # manually aggregating chunk texts into one blob of message, for the parsering later.

json_output = output_parser.parse(resp_message)
print(json_output["gift"])
print(json_output["price_value"])
print(json_output["delivery_days"])