from langchain_core.prompts import ChatPromptTemplate



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





