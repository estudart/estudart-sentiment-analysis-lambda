import time

from concurrent.futures import ThreadPoolExecutor, as_completed

from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()



class FAISSAdapter:
    def __init__(self, documents=None, folder_path="src/files/full_db"):
        self.embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
        self.documents = documents
        self.folder_path = folder_path

        self.executor = ThreadPoolExecutor(max_workers=5)

        self.vectorestore = None

        self._start_db()

    def _start_db(self):
        if self.documents:
            self.vectorestore = FAISS.from_documents(
                documents=self.documents,
                embedding=self.embeddings
            )
        else:
            self.vectorestore = FAISS.load_local(
                folder_path=self.folder_path,
                embeddings=self.embeddings,
                allow_dangerous_deserialization=True
            )

    def get_vector_store(self):
        return self.vectorestore

    def find_similarity(self, text: str, num_similarity: int):
        return self.vectorestore.similarity_search(text, k=num_similarity)
    
    def find_max_marginal_relevance(self, text, num_similarity, num_marginal):
        return self.vectorestore.max_marginal_relevance_search(
            text, 
            k=num_similarity, 
            fetch_k=num_marginal
        )
    
    def add_new_document(self, new_document):
        try:
            self.vectorestore.add_documents(new_document)
            return True
        except Exception as err:
            print(f"Could not add new document {new_document} to database, reason: {err}")
            return False

    def add_new_documents(self, new_documents, batch_size=50):
        try:
            futures = [
                self.executor.submit(
                    self.add_new_document,
                    new_documents[i:i + batch_size]
                )
                for i in range(0, len(new_documents), batch_size)
            ]
            for future in as_completed(futures):
                future.result()

        except Exception as err:
            pass
    
    def save_local(self, path):
        try:
            self.vectorestore.save_local(path)
            return True
        except Exception as err:
            print(f"Could not store local, reason: {err}")
            return False
