import streamlit as st
from chain import LLM_Chain
from chain import get_len
import time
import json
import translate as ts
from streamlit_mic_recorder import speech_to_text


#Maximum desired chain length in characters
MAX_CHAIN_LENGTH = 7000
#Minimum prompt length to allow summarization
MIN_SUM_LENGTH = 100



language_dict = {
    "English": 0,
    "Espanol": 1,
    "Français": 2,
    "Deutsch": 3,
    "Português": 4
}
radio_list = [
    "Chat",
    "Chat With JBML Documents"
]

def clear_history():
   st.session_state.messages = [
        {"role": "assistant", "content": "How may I help you today?"}]
   st.session_state['llm_chain'] = create_chain()
   st.session_state.input_state=False

def create_chain():
    llm_chain = LLM_Chain()
    return llm_chain

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

def remove_pdf_suffix(string):
    if string.endswith('.pdf'):
        return string[:-len('.pdf')]
    return string

def update():
        st.query_params.language = st.session_state.language
        st.session_state.header = ts.translate_to("JBML Chat", st.query_params.language)
        st.session_state.button_text = ts.translate_to("Clear History", st.query_params.language)
        st.session_state.radio_text = ts.translate_to("Select what type of chat you would like!", st.query_params.language)
        st.session_state.radio_list = [ts.translate_to(radio_list[0], st.query_params.language),
                                       ts.translate_to(radio_list[1], st.query_params.language)
                                        ]
        st.session_state.select_box_text = ts.translate_to("Select a Language",st.query_params.language)
        st.session_state.chat_input_text = ts.translate_to("Your Message Here", st.query_params.language)
        st.session_state.warning_text = ts.translate_to("You have reached the end of this conversation. Please clear chat to continue.",st.query_params['language'])


if "current_response" not in st.session_state:
    st.session_state.current_response = ""

if "disabled" not in st.session_state:
    st.session_state.disabled = False

if 'language' not in st.query_params:
    st.query_params['language'] = 'English'
    
if 'language' not in st.session_state:
        st.session_state.language = "English"

if 'llm_chain' not in st.session_state:
    st.session_state['llm_chain'] = create_chain()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I help you today?"}
    ]

if "stt" not in st.session_state:
    st.session_state.stt = ""


update()

st.set_page_config(
    page_title="JBML Chat",
    page_icon="images/logo.ico"
)


with st.sidebar:
    st.selectbox (
        st.session_state.select_box_text,
        language_dict.keys(), 
        key='language',
        index = language_dict[st.session_state.language]
    )
    st.radio(
       st.session_state.radio_text, 
        st.session_state.radio_list,
        key="chat_choice",
        horizontal=True,
    )
    st.session_state.stt = speech_to_text(just_once=True)
   
    st.button(st.session_state.button_text, on_click=clear_history)
st.header(st.session_state.header)


# We loop through each message in the session state and render it as
# a chat message.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(ts.translate_to(message["content"],st.query_params['language']))


#Push warning message to screen if chain length can no longer be shortened 
if st.session_state.disabled:
    st.warning(st.session_state.warning_text)

# We take questions/instructions from the chat input to pass to the LLM
if user_prompt := st.chat_input(st.session_state.chat_input_text, key="user_input", disabled=st.session_state.disabled) or st.session_state.stt != "" and st.session_state.stt != None:

    if st.session_state.stt != "" and st.session_state.stt != None:
        user_prompt = st.session_state.stt

    # Add our input to the session state
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    # Add our input to the chat window
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    response = ''
    
    # Translate user prompt to English before calling model
    translated_user_prompt = ts.translate_from(user_prompt, st.query_params['language'])
    
    
    match st.session_state.radio_list.index(st.session_state.chat_choice):
        case 0:
            response = st.session_state['llm_chain'].call(translated_user_prompt)
        case 1:
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
            response = ts.translate_to('An error has occured, please select a type of chat you would like', st.query_params.language)
    
    # Translate back to selected language after calling model
    translated_response = ts.translate_to(response, st.query_params['language'])
   
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
            time.sleep(0.0035)
    

    #Check to see if the chain exceeds the maximum length
    if get_len(st.session_state['llm_chain'].chain) > MAX_CHAIN_LENGTH: 
        
        print("Summarizing Chain: \n")
        st.session_state['llm_chain'].summarize_chain(MIN_SUM_LENGTH)
        
        #Check to see if the chain still exceeds the maximum length
        if get_len(st.session_state['llm_chain'].chain) > MAX_CHAIN_LENGTH:
            
            print("Chain Too Long - Ending Session")
            #Disable chat input
            st.session_state.disabled = True
            st.rerun()



