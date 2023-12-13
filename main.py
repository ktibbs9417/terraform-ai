import os
import re
import google.auth
import streamlit as st
from google.cloud import storage, aiplatform
from modules.tf_reader_utility import TerraformReader
from modules.llm_library import LLMLibrary
from dotenv import load_dotenv
from htmlTemplates import css, bot_template, user_template
from langchain.memory import ConversationBufferMemory


class TF_ASSISTANT():
    
    def initiate(self):
        if not hasattr(st.session_state, 'init') or st.session_state.init is None:
            # Google Auth and Vertex AI Init
            load_dotenv()
            print(f"Initializing Google Auth and Vertex AI")
            st.session_state.terraformreader = TerraformReader()
            st.session_state.llmlibrary = LLMLibrary()
            self.credentials, self.project = google.auth.default()
            aiplatform.init(project=self.project, location="us-central1")
            st.session_state.init = True

    def reset_conversation(self):
        print(f"Resetting conversation")
        st.session_state.conversation = None
        st.session_state.chat_history = None
        st.session_state.gcs_blob = None
        st.session_state.llm = None
        st.session_state.disabled = False
        st.rerun()


    def handle_userinput(self, question):
        if "conversation" not in st.session_state or st.session_state["conversation"] is None:
            st.session_state.conversation = st.session_state.llmlibrary.ask()
        response = st.session_state.conversation({'question': question})
        print(f"Response: {response}")
        st.session_state.chat_history = response['chat_history']
        #print(f"Chat History:\n {st.session_state.chat_history}\n")
        #print(f"Conversation:\n {st.session_state.conversation}\n")

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
        
    def disable_upload(self):
        st.session_state.disabled = True


def main():
# Streamlit Code
    st.set_page_config('Terraform Assistant')
    st.write(css, unsafe_allow_html=True)

    # Initialize session_state if not already
    if "init" not in st.session_state:
        print(f"Initializing PDFQA")
        st.session_state.init = None
        tf_assist.initiate()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "gcs_blob" not in st.session_state:
        st.session_state.gcs_blob = None
    if "index" not in st.session_state:
        st.session_state.index = None
    if "disabled" not in st.session_state:
        st.session_state.disabled = False
    if 'message_placeholders' not in st.session_state:
        st.session_state.message_placeholders = []
    if "file_processed" not in st.session_state:
        st.session_state.file_processed = False
    if "llm" not in st.session_state:
        st.session_state.llm = "vertex"
        st.session_state.disabled = False


    if st.session_state.chat_history is not None:
        # Iterate over the chat history and display each message
        for i, message in enumerate(st.session_state.chat_history):
            # Ensure there's a placeholder for each message
            if len(st.session_state.message_placeholders) <= i:
                st.session_state.message_placeholders.append(st.empty())
            
            # Decide which template to use based on whether it's a user or bot message
            template = user_template if i % 2 == 0 else bot_template
            # Update the corresponding placeholder with the message
            st.session_state.message_placeholders[i].write(template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        
        template = user_template if i % 2 == 0 else bot_template
        st.session_state.message_placeholders[i].write(template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
   
    if question := st.chat_input("Ask a questions:"):
        if st.session_state.llm is not None:
            tf_assist.handle_userinput(question)
            st.session_state.disabled = True
        else:
            st.error("Please select a Language Model and ask again.")
            print("user did not select a language model")

# Side bar code
    with st.sidebar:
        with st.form("Terraform State Upload"):
            terraform_state_path = st.text_input("Terraform GCS path starts with gs:// ends with .tfstate:", key = "terraform_state_path")
            submit_button = st.form_submit_button(label='Submit', on_click=tf_assist.disable_upload, disabled=st.session_state.disabled)
            if submit_button:
                st.info("File Uploaded: "+ st.session_state.terraform_state_path)
                st.session_state.terraformreader.get_tf_state(st.session_state.terraform_state_path)
        # Reset Chat button
        if st.button("Reset Chat"):
            tf_assist.reset_conversation()
        # User Selects a Language Model
        llm = st.radio(
            "Select a Language Model",
            ["VertexAI", "OpenAI"],
            captions = ["Chat with Google's Chat Bison", "Use Azure OpenAI"],
            disabled=st.session_state.disabled,
            index = None,
        )
        print(f"Selected LLM: {llm}")
        if llm == "VertexAI":
            st.session_state.llm = "vertex"
        elif llm == "OpenAI":
            st.session_state.llm = "openai"
        else:
            st.session_state.llm = None


if __name__ == "__main__":
    tf_assist = TF_ASSISTANT()
    main()

