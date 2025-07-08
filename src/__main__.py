from datetime import datetime

from ai_parsing.run_ollama import convert_markdown_to_json
from parse_expense import pdf_to_markdown

file_name = "fatura-1.pdf"

markdown_content = pdf_to_markdown(file_name)

result = convert_markdown_to_json(markdown_content)

new_file_name = f"./generated/{file_name}_{datetime.now().isoformat()}.json"
with open(new_file_name, "w+") as file:
    file.write(result.model_dump_json())
