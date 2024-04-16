import streamlit as st
from chain import LLM_Chain
import time
import json
import translate as ts

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
    metadata = [metadata]
    for i, meta in enumerate(metadata):
        try:
            filename = remove_pdf_suffix(meta['file_name'])
            page = meta['page_label']

            cite = f"\n\nSource {i+1}:\n\n{pubs[filename]['product_title']} page {page}\n\nPDF: [{pubs[filename]['product_number']}]({pubs[filename]['url']})\n"

            citation.append(cite)
        except:
            citation.append(f"Error grabbing source details: {meta['file_name']} page {meta['page_label']}")


    return citation

uploaded_files = []
#is called whenever a file/files are uploaded
def uploadFiles():
    for x in uploaded_files:
        pass


with st.sidebar:
    st.radio(
        "Select what type of chat you would like!",
        ["Chat", "Chat with JBML Documents!","Chat with Uploaded Documents"],
        key="chat_choice",
        horizontal=True,
    )
    uploaded_files = st.file_uploader(
        "Enter and PDF, CSV, or XLS file", 
        accept_multiple_files=True,
        on_change = uploadFiles
    )
    language = st.selectbox(
        "Select a Language",
        ["English", "Espanol", "Français", "Deutsch", "Português"],
    )

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I help you today?"}
    ]

if "current_response" not in st.session_state:
    st.session_state.current_response = ""

# We loop through each message in the session state and render it as
# a chat message.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# We take questions/instructions from the chat input to pass to the LLM
if user_prompt := st.chat_input("Your message here", key="user_input"):

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
            response, context, metadata = st.session_state['llm_chain'].call_jbml(user_prompt)
            citation = get_citation(metadata)
            sources = ''.join(citation)
            response = f"Quoted text:\n\n \"{context}\"\n\n Sources: \n{sources} \n\n{ts.translate_to(response, st.session_state['language'])}"
        case "Chat with Uploaded Documents":
            response, context, metadata = st.session_state['llm_chain'].call_uploaded(user_prompt)
            citation = get_citation(metadata)
            sources = ''.join(citation)
            response = f"Quoted text:\n\n \"{context}\"\n\n Sources: \n{sources} \n\n{ts.translate_to(response, st.session_state['language'])}"
        case _:
            response = 'An error has occured, please select a type of chat you would like'
    
    # Translate back to selected language after calling model
    if not language == "English":
        translated_response = ts.translate_to(response, st.session_state['language'])
    else:
        translated_response = response

    response_char_list = [char for char in translated_response]

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
            time.sleep(0.01)

