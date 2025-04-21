from langchain_core.prompts import ChatPromptTemplate



bullet_to_text_prompt = ChatPromptTemplate.from_template(
    """
    You are a skilled technical writer.

    Turn the following bullet points into a well-written, coherent paragraph that flows naturally. 
    Preserve all key ideas and keep it concise.

    Bullet points:
    {bullets}
    """
)