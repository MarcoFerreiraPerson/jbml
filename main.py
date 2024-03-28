import streamlit as st
from chain import LLM_Chain
import time
import json
import translate as ts

#Maximum desired chain length in characters
MAX_CHAIN_LENGTH = 9000

st.set_page_config(
    page_title="JBML Chat"
)

st.header("JBML Chat")

@st.cache_resource
def get_pubs():
    file_path = 'pubs.json'
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Unable to parse JSON from '{file_path}'.")
        return {}


def create_chain(system_prompt):
    llm_chain = LLM_Chain(system_prompt)

    return llm_chain

system_prompt = """The following is a friendly conversation between a human and an AI. The AI answers prompts given in a simple and consise manor that is full of important and related information. 
If the AI does not know the answer to a question, it truthfully says it does not know. 
You are made for the Joint Military Base in Lakehurst (JBML). Dont complete what I am saying, simply respond to it. Just respond like you were talking to another person. Do not do User: response formatting.
You are simply answering the questions given based on the context given, if the context doesnt give enough information to answer the question then simply use your information and mention it is not mentioned in the text. Make sure you cite your sources as you go.
If the prompt is unrelated to the text like a "thank you" then just respond to the prompt simply. Do not show your response to thinking, simply just respond to the prompt simply and consisely. 
"""

if 'llm_chain' not in st.session_state:
    st.session_state['llm_chain'] = create_chain(system_prompt)

if 'language' not in st.session_state:
    st.session_state['language'] = 'en'

def remove_pdf_suffix(string):
    if string.endswith('.pdf'):
        return string[:-len('.pdf')]
    return string

def get_citation(metadata):
    pubs = get_pubs()
    citation = []
    for i, meta in enumerate(metadata):
        try:
            filename = remove_pdf_suffix(meta['file_name'])
            page = meta['page_label']

            cite = f"\n\nSource {i+1}:\n\n{pubs[filename]['product_title']} page {page}\n\nPDF: [{pubs[filename]['product_number']}]({pubs[filename]['url']})\n"

            citation.append(cite)
        except:
            citation.append(f"Error grabbing source details: {meta['file_name']} page {meta['page_label']}")


    return citation
    
def clear_history():
   global input_state
   st.session_state.messages = [
        {"role": "assistant", "content": "How may I help you today?"}]
   st.session_state['llm_chain'] = create_chain(system_prompt)
   st.session_state.input_state=False

with st.sidebar:
    st.radio(
        "Select what type of chat you would like!",
        ["Chat", "Chat with JBML Documents!"],
        key="chat_choice",
        horizontal=True,
    )
    language = st.selectbox(
        "Select a Language",
        ["English", "Espanol", "Français", "Deutsch", "Português"],
    )
    st.button("Clear History", on_click=clear_history)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I help you today?"}
    ]

if "current_response" not in st.session_state:
    st.session_state.current_response = ""

if "input_state" not in st.session_state:
    st.session_state.input_state = False

# We loop through each message in the session state and render it as
# a chat message.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if st.session_state.input_state:
    st.warning("You have reached the end of this conversation. Please clear chat to continue.")

# We take questions/instructions from the chat input to pass to the LLM
if user_prompt := st.chat_input("Your message here", key="user_input", disabled=st.session_state.input_state):

    def set_language(language):
        if language == "English":
            st.session_state['language'] = "en"
        if language == "Espanol":
            st.session_state['language'] = "es"
        if language == "Français":
            st.session_state['language'] = "fr"
        if language == "Deutsch":
            st.session_state['language'] = "de"
        if language == "Português":
            st.session_state['language'] = "pt"
    
    
    # Add our input to the session state
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    # Add our input to the chat window
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    response = ''
    
    # Translate user prompt to English before calling model
    set_language(language)
    if not language == "English":
        translated_user_prompt = ts.translate_from(user_prompt, st.session_state['language'])
    else:
        translated_user_prompt = user_prompt

    match st.session_state['chat_choice']:
        case 'Chat':
            response = st.session_state['llm_chain'].call(translated_user_prompt)
        case 'Chat with JBML Documents!':
            response = ''
            airesponse, context, metadata = st.session_state['llm_chain'].call_jbml(user_prompt)
            citation = get_citation(metadata)
            sources = ''.join(citation)
            response = f"Quoted text:\n\n"
            for c in context:
                response += f"\n\n \"{c}\"\n\n"
            
            response +=  "Sources: \n"
            
            response += f"\n{sources} \n\n"
            response += f"\n\n{ts.translate_to(airesponse, st.session_state['language'])}"
        case _:
            response = 'An error has occured, please select a type of chat you would like'
    
    # Translate back to selected language after calling model
    if not language == "English":
        translated_response = ts.translate_to(response, st.session_state['language'])
    else:
        translated_response = response
    try: 
        response_char_list = [char for char in translated_response]
    except:
        response_char_list = [char for char in response]
        translated_response = response
        print(translated_response)
    # Add the response to the session state
    st.session_state.messages.append(
        {"role": "assistant", "content": translated_response}
    )

    with st.chat_message("assistant"):
        box = st.empty()
        ai_response = ""
        for char in response_char_list:
            ai_response += char
            box.write(ai_response)
            time.sleep(0.007)
    
    if len(st.session_state['llm_chain'].chain) > MAX_CHAIN_LENGTH: 
        if  st.session_state['llm_chain'].summarize_chain(MAX_CHAIN_LENGTH):
            st.session_state.input_state = True
            st.rerun()

   
