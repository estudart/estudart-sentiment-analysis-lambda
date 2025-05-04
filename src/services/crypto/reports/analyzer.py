from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser

from src.adapters.faiss_adapter import FAISSAdapter
from src.prompts.crypto.insight import insight_prompt, long_report_prompt



class MarketAnalyzer:
    def __init__(self):
        self.chat = ChatOpenAI(model='gpt-3.5-turbo') # ChatGoogleGenerativeAI(model='gemini-pro')
        
        self.vectorstore = FAISSAdapter().get_vector_store()

        self.setup = RunnableParallel(
            {
                'question': RunnablePassthrough(),
                'context': self.vectorstore.as_retriever(
                    search_type='mmr', 
                    search_kwargs={
                        'k': 12,
                        'fetch_k': 150
                    }
                )
            }
        )

    def join_documents(self, input):
        input['context'] = '\n\n'.join([c.page_content for c in input['context']])
        return input

    def run(self):
        chain = self.setup | long_report_prompt | self.chat | StrOutputParser()
        while True:
            question = input("Ask something to your db: ")
            if question == "byebye":
                break
            answer = chain.invoke(question)
            print(f"{answer}\n")