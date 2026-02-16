🤖 Chat with PDF (GPT Style Offline)

Chat with your PDF, TXT, or PPTX files in GPT-style conversation — completely offline!
This Streamlit app allows you to upload documents, ask questions, and get concise GPT-style answers without requiring any API key.



📌 Features

Multi-file Support: Upload PDF, TXT, or PPTX files.

Offline GPT-Style Answers: Generates clean, structured answers like ChatGPT without needing any API key.

Automatic Page Number Removal: Removes isolated page numbers for cleaner context.

Relevant Context Extraction: Finds the most relevant chunks of text for your questions.

Self-Contained Answers: Provides answers in up to 6 points, covering key concepts.

Persistent Chat History: Tracks your questions and answers in the session.

Clear History Option: Easily reset the documents and chat history from the sidebar.




🛠 Installation

Clone the repository (or download files):

git clone <your-repo-link>
cd chat-with-pdf-offline


Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Install dependencies:

pip install streamlit langchain_community




🚀 Usage

Run the app:

streamlit run app.py


Upload your documents in the sidebar (PDF, TXT, or PPTX). Multiple files are supported.

Ask questions in the chat interface. The bot will respond in GPT-style points.

Clear history anytime using the "Clear History & Documents" button.




🔹 How it Works

Document Loading:

PDFs → PyPDFLoader

TXT → TextLoader

PPTX → UnstructuredPowerPointLoader

Text Processing:

Removes page numbers.

Splits text into lines and finds the most relevant chunks for the question.

Answer Generation:

Extracts relevant sentences based on keywords.


Chat Display:

Questions appear in light blue boxes.

Bot responses appear in light orange boxes.




Author : Shital Chitkalwar

Internship: Infosys Springboard 2026






