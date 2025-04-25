from langchain_openai import ChatOpenAI
from langchain.chains.retrieval_qa.base import RetrievalQA

from src.adapters.faiss_adapter import FAISSAdapter
from src.prompts.crypto.insight import insight_prompt, long_report_prompt



class MarketAnalyzer:
    def __init__(self):
        self.chat = ChatOpenAI(model='gpt-3.5-turbo-0125')
        self.vectorstore = FAISSAdapter().get_vector_store()

        self.chat_chain = RetrievalQA.from_chain_type(
            llm=self.chat,
            retriever=self.vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 50}),
            chain_type='stuff', # 'refine', 'map_reduce'
            return_source_documents=True,
            chain_type_kwargs={"prompt": long_report_prompt}
        )

    def run(self):
        while True:
            question = input("Ask something to your db: ")
            if question == "byebye":
                break
            answer = self.chat_chain.invoke({'query': question})
            print(f"{answer.get('result')}\n")