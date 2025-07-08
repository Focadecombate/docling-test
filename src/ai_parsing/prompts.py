from langchain_core.messages import SystemMessage

read_expenses = """
Please convert the following markdown invoice data into a structured JSON format that adheres to the specified schema.

For special cases:
- Group international transaction details (conversion rate, IOF) under the international_transactions object
- Include summary totals for future payments as separate properties
- Only include International transactions if there is a IOF charge

{format_instructions}

Content to process:
{content}

The output should be only the JSON.
"""


system_message = SystemMessage(
    content="""
You are an expert at converting markdown invoice data into structured JSON format.

Guidelines:
- Convert markdown invoice data to JSON following the exact schema provided
- For international transactions: group conversion rate and IOF under international_transactions object
- Include summary totals for future payments as separate properties
- Only include international_transactions if there is an IOF charge
- Output must be valid JSON only, no additional text or explanations
"""
)

human_template = """
{format_instructions}

Convert this markdown invoice data:
{content}
"""
