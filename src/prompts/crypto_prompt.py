from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from utils.config import secrets

model = ChatOpenAI(api_key=secrets.get("OPENAI_API_KEY"))

translate_prompt = ChatPromptTemplate.from_template(
    """
    Translate the following text to english:
    {transcript}
    """
)

summarize_prompt = ChatPromptTemplate.from_template(
    """
    You are a seasoned crypto researcher. Read the following transcript and extract 
    the key points in a concise bullet-point summary.

    Transcript:
    {transcript}
    """
)

insight_prompt = ChatPromptTemplate.from_template(
    """
    You are a crypto analyst skilled at interpreting sentiment and spotting opportunities 
    based on expert commentary.

    Given the following summary from a crypto-related video:
    {transcript}

    Do the following:
    1. Identify the overall sentiment (bullish, bearish, neutral)
    2. List any specific projects, sectors, or trends mentioned that could offer investment opportunities
    3. Justify each insight with reasoning based on the summary
    """
)

summarize_chain = summarize_prompt | model | StrOutputParser()
insight_chain = insight_prompt | model | StrOutputParser()
translate_chain = translate_prompt | model | StrOutputParser()
