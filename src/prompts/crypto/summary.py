from langchain_core.prompts import ChatPromptTemplate


summarize_prompt = ChatPromptTemplate.from_template(
    """
    You are a seasoned crypto researcher. Read the following transcript and extract 
    the key points in a concise bullet-point summary.

    Transcript:
    {transcript}
    """
)