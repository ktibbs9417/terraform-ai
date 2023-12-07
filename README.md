# Terraform Assistant

This is a Python application that uses Google's Vertex AI and OpenAI to assist users in writing Terraform code. The application is built with Streamlit and uses Google Cloud Storage for file handling.

## Features

- **Terraform Code Generation**: The application can generate Terraform code based on user input.
- **Language Model Selection**: Users can choose between Google's Vertex AI and Azure OpenAI for code generation. API Keys are required for both models.
- **Vector Embeddings**: Embeddings are generated using Cohere. API Key is required.
- **File Upload**: Users can upload Terraform state files from Google Cloud Storage using the gs:// path.

## Setup

1. Clone the repository.
2. Obtain API Key from [Cohere](https://dashboard.cohere.com/).
3. If you would like to use Azure OpenAI, follow the instructions [here](https://python.langchain.com/docs/integrations/llms/azure_openai) to obtain an API Key.
4. To use Vertex AI, obtain your API Key [here](https://developers.generativeai.google/products/palm). Note, you will need to create a Google Cloud project and enable Vertex AI. then you will need to run:
   ```
   export GOOGLE_API_KEY=<VERTEXAI_API_KEY>
   ```
5. Now you will need to create a Service Account and give that Service Account Admin access to the storeage bucket where your Terraform state file is stored.
6. Since the application uses the `google.auth` module, you can either use the `GOOGLE_APPLICATION_CREDENTIALS` environment variable or the `gcloud auth application-default login` command to authenticate. NOTE: if you are using the `GOOGLE_APPLICATION_CREDENTIALS` environment variable, you will need to set the `GOOGLE_CLOUD_PROJECT` environment variable as well.
   ```
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json
   ```
   
7. Install the required Python packages using pip:
   ```
   pip install -r requirements.txt
   ```
8. Set up your `.env` file within the root directory as shown below.
    ```
      COHERE_API_KEY=<API_KEY>
      REGION=<VERTEX_AI_REGION>
      PROJECT_ID=<VERTEX_AI_PROJECT>
      OPENAI_API_TYPE=azure
      OPENAI_API_VERSION=<VERSION>
      OPENAI_API_BASE=<BASE_URL>
      OPENAI_API_KEY=<API_KEY>
    ```
9.  Run the application with Streamlit:
   ```
   streamlit run main.py
   ```

## Usage

1. Start the application and navigate to the Streamlit server in your web browser.
2. Select a language model for code generation.
   1. If you do not select a language model, the application will error. If you select a language model and the proper API Key is not set, the application will error.
3. In the sidebar, enter the path to your Terraform state file in Google Cloud Storage and click "Submit".
   1. If you do not have a Terraform state file gs:// path, the application will error out and you'll need to restart the application.
4. Enter your question in the chat input field and press enter to generate Terraform code.
5. If you forgot to select a language model before uploading your .tfstate file, click the "Reset" button in the sidebar to reset the application state.
6. When you're done interacting with one statefile, you can upload another one by clicking the "Reset" button in the sidebar.

## Modules

- `TF_ASSISTANT`: This is the main class that handles user input and manages the application state.
- `VectorStore`: This module handles the storage and retrieval of vector embeddings.
- `TerraformReader`: This module reads and processes Terraform state files.
- `LLMLibrary`: This module handles the interaction with the language models.

## Contributing

Contributions are welcome! Please submit a pull request or create an issue to propose changes or additions.
