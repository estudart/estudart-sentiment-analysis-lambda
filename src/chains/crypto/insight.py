from langchain_core.output_parsers import StrOutputParser

from src.prompts.crypto.insight import insight_prompt
from src.utils.extensions import model

insight_chain = insight_prompt | model | StrOutputParser()