from langchain_core.output_parsers import StrOutputParser

from src.prompts.translate.translate_to_english import translate_prompt
from src.utils.extensions import model

translate_chain = translate_prompt | model | StrOutputParser()