from langchain.output_parsers import ResponseSchema

gift_schema = ResponseSchema(
    name="gift",
    description="Return True if this gift is bought for others, return False if not."
)

delivery_days_schema = ResponseSchema(
    name="delivery_days",
    description="Return the number of days as integer did it take for the gift to deliver. If this information is not provided, return -1."
)

price_value_schema = ResponseSchema(
    name="price_value",
    description="Return the float number of the gift price. If such information not found, return the list of sentences talk about value or price, and separate them with commas."
)

"""
gift_schema: boolean,
delivery_days_schema: int,
price_value_schema: float / str
"""
response_schemas = [
    gift_schema, delivery_days_schema, price_value_schema
]