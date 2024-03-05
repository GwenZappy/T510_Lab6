# Lab 6 - ESL Genie Chatbot

This chatbot is intended to help ESL users understand articles with difficult vocabularies.
Please try it with the Test_PDF.pdf!

## https://eslgenie.azurewebsites.net/

## Getting Started

- `python -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `streamlit run app.py`

## Lessons Learned

### 1. use openai api and configure the chatbot

OpenAI(): This is initializing an instance of the OpenAI API. It requires an API key (OPENAI_API_KEY), a base URL (OPENAI_API_BASE), and specifies the model to be used (gpt-3.5-turbo-0125). 

Additionally, we will need to set parameters like temperature.

Then we edit the system prompt to customize the chatbot

```bash
llm = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
    model="gpt-3.5-turbo-0125",
    temperature=0.0,
    system_prompt="You are an expert on the document and experienced in instructing English as a second language student, provide answers in concise and simple language to the questions. Always explain and elaborate on a difficult concept with simple language if there's any in the document.",
    )
```

### 2. st.session_state
1. Initialization: When you first access st.session_state, Streamlit automatically creates a session state object for the current user session. This object behaves like a Python dictionary.

2. Storing Data: You can store data in st.session_state using standard dictionary syntax. 

3. Retrieving Data: You can retrieve data from st.session_state using standard dictionary syntax as well. If the specified key exists, you can access its value.

4. Persistence: The data stored in st.session_state persists across different interactions within the same session of your Streamlit application. You can store data in one part of the app and access it later in another part of the app, as long as it's within the same session.

#### Example Usage

```bash
def increment_counter():
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    st.session_state.counter += 1

# Main application code
def main():
    st.title('Streamlit Session State Example')
    
    # Display the current value of the counter
    st.write('Counter:', st.session_state.get('counter', 0))
    
    # Button to increment the counter
    if st.button('Increment Counter'):
        increment_counter()

if __name__ == '__main__':
    main()
```

### 3. st.markdown to change color and font

```bash
st.markdown('''
    :green[Sample Questions:]  
            *1. What are some difficult concepts in this article?*   
            *2. Explain this concept.*
            ''')
```


