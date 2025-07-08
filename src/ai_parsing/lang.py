import logging

from galileo.handlers.langchain import GalileoCallback
from langchain.callbacks.base import BaseCallbackHandler
from langchain.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_ollama import OllamaLLM

from ..settings import settings
from .model import Fatura
from .prompts import human_template, system_message

logger = logging.getLogger("ai")


class StreamingCallbackHandler(BaseCallbackHandler):
    """Custom callback handler to log streaming responses"""

    def __init__(self):
        self.full_response = []

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.full_response.append(token)
        logger.debug(f"Streaming token: {token}")

    def on_llm_end(self, response, **kwargs) -> None:
        logger.info(
            f"LLM finished with response length: {len(''.join(self.full_response))}"
        )


galileo_callback = GalileoCallback()


def convert_markdown_to_json_langchain_streaming(markdown_content: str) -> Fatura:
    """LangChain integration with streaming and callback handling"""
    logger.info(f"file size: {len(markdown_content)}")
    logger.info(f"Marking markdown content for processing {markdown_content}")

    # Initialize callback handler
    callback_handler = StreamingCallbackHandler()

    # Initialize LangChain Ollama LLM with streaming
    llm = OllamaLLM(
        model=settings.MODEL,
        temperature=0.1,
        num_ctx=5000,
        callbacks=[callback_handler, galileo_callback],
    )

    # Create output parser
    parser = PydanticOutputParser(pydantic_object=Fatura)

    prompt = ChatPromptTemplate.from_messages(
        [system_message, HumanMessagePromptTemplate.from_template(human_template)]
    )

    prompt = prompt.partial(format_instructions=parser.get_format_instructions())

    logger.info(
        f"Using model: {settings.MODEL} with context size: {llm.num_ctx}, prompt: {prompt}"
    )

    # Create chain
    chain = prompt | llm | parser

    try:
        result = chain.invoke(
            {"content": markdown_content},
        )
        return result
    except Exception as e:
        logger.error(f"LangChain streaming error: {e}")
        raise
