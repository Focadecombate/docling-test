import datetime
import logging

import ollama

from ai_parsing.model import Result
from ai_parsing.prompts import read_expenses

logging.basicConfig(level=logging.INFO)
model = "llama3.1:8b"
logger = logging.getLogger("ai")


def convert_markdown_to_json(markdown_content: str):
    logger.info(f"file size: {len(markdown_content)}")
    full_response: list[str] = []
    try:
        response_iter = ollama.chat(
            model,
            messages=[
                ollama.Message(
                    role="user",
                    content=f"{read_expenses}\n{markdown_content}",
                )
            ],
            stream=True,
            format=Result.model_json_schema(),
            options={"temperature": 0, "num_ctx": 6000},
        )

        for response in response_iter:
            full_response.append(response.message.content or "")

        return Result.model_validate_json("".join(full_response))

    except ollama.ResponseError as e:
        logger.error("Error:", e.error)
        raise


if __name__ == "__main__":
    file_name = "fatura.md"
    with open(file_name) as file:
        markdown_content = file.read()
    result = convert_markdown_to_json(markdown_content)
    new_file_name = f"./{file_name}_{datetime.datetime.now().isoformat()}.json"
    with open(new_file_name, "w+") as file:
        file.write(result.model_dump_json())
