from langchain_core.prompts import ChatPromptTemplate


translate_prompt = ChatPromptTemplate.from_template(
    """
    Translate the following text to english:
    {transcript}
    """
)