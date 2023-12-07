import time
import streamlit as st
from modules.vectorstore import VectorStore
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatGooglePalm
import os
from langchain.embeddings.cohere import CohereEmbeddings
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI


class LLMLibrary:
        
    def __init__(self):
        BASEDIR = os.path.abspath(os.path.dirname("main.py"))
        load_dotenv(os.path.join(BASEDIR, '.env'))
        choere_api_key = os.getenv("COHERE_API_KEY")
        self.atlas_api_key = os.getenv("ATLAS_API_KEY")
        self.embedding_function = CohereEmbeddings(model="embed-multilingual-v2.0", cohere_api_key=choere_api_key)
        self.vectorstore = VectorStore()
        os.environ["OPENAI_API_TYPE"] = os.getenv("OPENAI_API_TYPE")
        os.environ["OPENAI_API_VERSION"] = os.getenv("OPENAI_API_VERSION")
        os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")    

    def get_llm(self):
        print(f"Loading LLM {st.session_state.llm}")
        if st.session_state.llm == "vertex":
            return ChatGooglePalm(temperature=0.0)
        elif st.session_state.llm == "openai":
            return AzureChatOpenAI(deployment_name="gpt-4", model_name="gpt-4", temperature=0.0)
    
    def ask(self):

        llm = self.get_llm()
        print(f"LLM: {llm}\n")  
        vectordb = self.vectorstore.get_vectordb()

        system_template = '''
        You are a helpful assistant that is a DevOps Engineer. Your goal is to provide high quality Terraform code to users that are looking to deploy infrastructure on the cloud.

        Context:
        {context}

        '''
        messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template("Provide Terraform to the following question: {question}:"),
        ]
        prompt = ChatPromptTemplate.from_messages(messages)

        # generate_queries = (
        #     prompt | llm | StrOutputParser() | (lambda x: x.split("\n"))
        # )
        # Create a retriever from the vector database
        retriever = vectordb.as_retriever(
                    search_type="similarity",
                    search_kwargs={
                        "k": 5,
                        "search_distance": 0.6,
                    },
            )


        memory = ConversationBufferMemory(memory_key="chat_history", output_key="answer", return_messages=True, max_token_limit=1024)
        print(f"Initiating chat conversation memory\n")
        #print(f"Conversation Memory: {memory}\n")
        conversation_chain= ConversationalRetrievalChain.from_llm(
              llm,
              retriever=retriever,
              memory=memory,
              rephrase_question=True,
              combine_docs_chain_kwargs={'prompt': prompt},
              return_source_documents=True,
              verbose=True,
        )
        #print(f"Conversation chain: {conversation_chain}\n")
        return conversation_chain