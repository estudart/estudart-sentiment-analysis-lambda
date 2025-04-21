from langchain_core.output_parsers import StrOutputParser

from src.prompts.text_convertions.bullet_to_text import bullet_to_text_prompt
from src.utils.extensions import model


bullet_to_text_chain = bullet_to_text_prompt | model | StrOutputParser()