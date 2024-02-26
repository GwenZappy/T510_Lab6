import re
from tempfile import NamedTemporaryFile
import os

import streamlit as st
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PDFReader
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Chat with the PDF",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

# Initialize the chat messages history
if "messages" not in st.session_state.keys():  
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about your document!"}
    ]

uploaded_file = st.file_uploader("Upload a file")
if uploaded_file:
    bytes_data = uploaded_file.read()
    with NamedTemporaryFile(delete=False) as tmp:  
        tmp.write(bytes_data)  
        with st.spinner(
            text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."
        ):
            reader = PDFReader()
            docs = reader.load_data(tmp.name)
            llm = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_API_BASE"),
                model="gpt-3.5-turbo",
                temperature=0.0,
                system_prompt="You are an expert on the content of the document, provide detailed answers to the questions. Use the document to support your answers.",
            )
            index = VectorStoreIndex.from_documents(docs)
    os.remove(tmp.name)  

    if "chat_engine" not in st.session_state.keys():  
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode="condense_question", verbose=False, llm=llm
        )

# Function to extract difficult words
def extract_difficult_words(docs):
    difficult_words = set()
    for doc in docs:
        text = doc.text
        # Remove punctuation marks and special characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # Split text into words using whitespace as delimiter
        words = text.split()
        for word in words:
            # Check if the word contains only alphabetic characters and is not a URL
            if word.isalpha() and not word.startswith("http") and len(word) > 10:  
                difficult_words.add(word)
    return difficult_words

# Chatbot interaction
prompt = st.text_input("Your question")
if prompt:  
    st.session_state.messages.append({"role": "user", "content": prompt})

if "messages" in st.session_state.keys() and st.session_state.messages[-1]["role"] == "user":
    with st.spinner("Thinking..."):
        response = st.session_state.chat_engine.stream_chat(st.session_state.messages[-1]["content"])
        st.write_stream(response.response_gen)
        message = {"role": "assistant", "content": response.response}
        st.session_state.messages.append(message)

for message in st.session_state.messages:  
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.button("Extract Difficult Words"):
    difficult_words = extract_difficult_words(docs)
    st.subheader("Difficult Words:")
    st.write(", ".join(difficult_words))