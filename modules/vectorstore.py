import os
from langchain.embeddings.cohere import CohereEmbeddings
from dotenv import load_dotenv
from langchain.vectorstores import FAISS



class VectorStore:
    
    def __init__(self):
        BASEDIR = os.path.abspath(os.path.dirname("main.py"))
        load_dotenv(os.path.join(BASEDIR, '.env'))
        choere_api_key = os.getenv("COHERE_API_KEY")
        self.embedding_function = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=choere_api_key)

    
    def faiss(self, doc_splits, blob_name):
        print("Creating FAISS Index")
        db = FAISS.from_documents(
            doc_splits, 
            embedding=self.embedding_function
            )
        db.save_local("faiss_db")

    def get_vectordb(self):
        return FAISS.load_local("faiss_db", self.embedding_function)
