from langchain_core.output_parsers import StrOutputParser

from src.prompts.crypto.summary import summarize_prompt
from src.utils.extensions import model



summarize_chain = summarize_prompt | model | StrOutputParser()