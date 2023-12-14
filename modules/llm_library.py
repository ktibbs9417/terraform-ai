import time
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import (
    ChatPromptTemplate,
    AIMessagePromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts import MessagesPlaceholder
from langchain.chat_models import ChatGooglePalm
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.vectorstores import FAISS



class LLMLibrary:
        
    def __init__(self):
        BASEDIR = os.path.abspath(os.path.dirname("main.py"))
        load_dotenv(os.path.join(BASEDIR, '.env'))
        os.environ["OPENAI_API_TYPE"] = os.getenv("OPENAI_API_TYPE")
        os.environ["OPENAI_API_VERSION"] = os.getenv("OPENAI_API_VERSION")
        os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        choere_api_key = os.getenv("COHERE_API_KEY")
        self.embedding_function = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=choere_api_key)

    def get_llm(self):
        print(f"Loading LLM {st.session_state.llm}")
        if st.session_state.llm == "vertex":
            return ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.0)
        elif st.session_state.llm == "openai":
            return AzureChatOpenAI(deployment_name="gpt-4", model_name="gpt-4", temperature=0.0)
        
    def faiss(self, doc_splits, blob_name):
        print("Creating FAISS Index")
        global vectorstore
        vectorstore = FAISS.from_documents(
            doc_splits, 
            embedding=self.embedding_function
        )
        vectorstore.save_local("gemini-bug")
    def ask(self):
        llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.0)
        print(f"LLM: {llm}\n")
        vectordb = FAISS.load_local("gemini-bug", embeddings=self.embedding_function)

        system_template = '''
        You are a helpful assistant that is a DevOps Engineer. Your goal is to provide high quality Terraform code to users that are looking to deploy infrastructure on the cloud.

        Context:
        {context}

        Provide Terraform to the following question: {question}:

        '''
        messages = [
            HumanMessagePromptTemplate.from_template(system_template),
            #AIMessagePromptTemplate.from_template(system_template),
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
        
        print (f"Prompt: {prompt}\n")
        retriever = vectordb.as_retriever(
                    search_type="similarity",
                    search_kwargs={
                        "k": 1,
                        "search_distance": 0.6,
                    },
            )


        memory = ConversationBufferMemory(memory_key="chat_history", output_key="answer", return_messages=True, max_token_limit=1024)
        print(f"Initiating chat conversation memory\n")
        print(f"Conversation Memory: {memory}\n")
        conversation_chain= ConversationalRetrievalChain.from_llm(
            llm,
            retriever=retriever,
            memory=memory,
            rephrase_question=True,
            combine_docs_chain_kwargs={'prompt': prompt},
            return_source_documents=True,
            verbose=True,
        )
        print(f"Conversation chain: {conversation_chain}\n")
        return conversation_chain
    
if __name__ == "__main__":
    llm_library = LLMLibrary()
    question = "595132057377"
    conversation = llm_library.ask()
    response = conversation({'question': question})
    print (response['chat_history'])