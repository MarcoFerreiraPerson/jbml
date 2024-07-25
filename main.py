import streamlit as st
from chain import LLM_Chain
from chain import get_len
import time
import json
from webSearch import get_web_search
from langchain_community.tools import DuckDuckGoSearchResults
import translate as ts
from streamlit_mic_recorder import speech_to_text
import const
from file_adder import *

def clear_history():
   """Clears session_state and chain.
   """
   st.session_state.messages = const.messages_text_dict[st.session_state.language].copy()
   st.session_state['llm_chain'] = create_chain()
   st.session_state.input_state=False
   st.session_state.uploaded_files = []
   try:
       if(st.session_state.file_adder is not None):
            st.session_state.file_adder.reset() 
   except:
       pass

def create_chain():
    """Creates a new chain for the session_state.
    """
    llm_chain = LLM_Chain()
    return llm_chain

def get_jbml_citation(metadata):
    pubs = get_pubs()
    citation = []
    for i, meta in enumerate(metadata):
        try:
            filename = remove_suffix(meta['file_name'])
            page = meta['page_label']

            cite = f"\n\nSource {i+1}:\n\n{pubs[filename]['product_title']} page {page}\n\nPDF: [{pubs[filename]['product_number']}]({pubs[filename]['url']})\n"

            citation.append(cite)
        except:
            citation.append(f"Error grabbing source details: {meta['file_name']} page {meta['page_label']}")


    return citation

def get_web_citation(metadata):
    citation = []
    for i, source in enumerate(metadata.keys()):
        try:

            cite = f"\n\nSource {i+1}:\n {metadata[source]['title']} \n{metadata[source]['link']}\n"

            citation.append(cite)
        except:
            citation.append(f"Error grabbing source details")

    return citation

def get_uploaded_citation(metadata):
    citation = []
    for i, meta in enumerate(metadata):
        try:
            filename = remove_suffix(meta['source'])
            filename = remove_prefix(filename)

            cite = f"\n\nSource {i+1}: {filename} [{meta['location']}]\n"

            citation.append(cite)
        except:
            citation.append(f"Error grabbing source details: {meta['source']} {meta['location']}")


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

def remove_suffix(string):
    if string.endswith('.pdf'):
        return string[:-len('.pdf')]
    if string.endswith('.csv'):
        return string[:-len('.csv')]
    return string

def remove_prefix(string):
    prefix_index = string.rfind("\\")+1
    if(prefix_index > 0 and prefix_index < len(string)):
        return string[prefix_index:]
    return string


def update(isStartup: bool):
    """Initializes session_state values on startup and updates page text upon language selection.
    """
    if not st.session_state.language == st.query_params.language or isStartup:
        clear_history()
        st.query_params.language = st.session_state.language
        st.session_state.button_text = const.button_text_dict[st.query_params.language]
        st.session_state.radio_text = const.radio_text_dict[st.query_params.language]
        st.session_state.radio_list = const.radio_list_dict[st.query_params.language]
        st.session_state.chat_input_text = const.chat_input_text_dict[st.query_params.language]
        st.session_state.warning_text = const.warning_text_dict[st.query_params.language]
        st.session_state.error_message = const.error_message_dict[st.query_params.language]
        st.session_state.stt_text = const.stt_text_dict[st.query_params.language]
        st.session_state.messages[0] = const.messages_text_dict[st.query_params.language][0]
        st.session_state.file_options = const.file_options_dict[st.query_params.language]
        st.session_state.upload_button = const.upload_button_dict[st.query_params.language]



st.set_page_config(
    page_title="JBML Chat",
    page_icon="images/logo.ico"
)

#Initializes session_state values on startup
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

if 'web_engine' not in st.session_state:
    st.session_state['web_engine'] = DuckDuckGoSearchResults()

if "messages" not in st.session_state:
    st.session_state.messages = const.messages_text_dict[st.session_state.language].copy()

if 'select_box_text' not in st.session_state:
    st.session_state.select_box_text = const.select_box_text_dict[st.session_state.language]

if "stt" not in st.session_state:
    st.session_state.stt = ""
    update(True)

if 'file_adder' not in st.session_state:
    st.session_state.file_adder = FileAdder()
    st.session_state.file_adder.reset()

if 'uploded_files' not in st.session_state:
    st.session_state.uploaded_files = []

#Sets page title text
st.header("JBML Chat")

#Creates sidebar
with st.sidebar:
    
    #Creates language selection dropdown
    st.selectbox (
        const.select_box_text_dict[st.session_state.language],
        const.language_dict.keys(), 
        key='language',
        index = const.language_dict[st.session_state.language],
        on_change=update(False)
    )
   
   #Creates "chat_choice" dropdown
    st.radio(
       st.session_state.radio_text, 
        st.session_state.radio_list,
        key="chat_choice",
        horizontal=True,
    )

    #Creates a form used to upload files
    with st.form("upload_form", clear_on_submit=True):
        st.session_state.uploaded_files = st.file_uploader(
            st.session_state.file_options, 
            accept_multiple_files=True,
        )
        submitted = st.form_submit_button(st.session_state.upload_button)

        #adds the uploaded files to file_adder, which embeds them
        if submitted and st.session_state.uploaded_files is not None:
            for x in st.session_state.uploaded_files:
                st.session_state.file_adder.add(x)

    #Creates speach to text button
    st.session_state.stt = speech_to_text(just_once=True, start_prompt=st.session_state.stt_text[0],stop_prompt=st.session_state.stt_text[1])
   
    #Creates clear history button
    st.button(st.session_state.button_text, on_click=clear_history)



# We loop through each message in the session state and render it as
# a chat message.
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message["content"],)

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
    
    # try: 

    translated_chat_choice = const.radio_list_dict["English"][st.session_state.radio_list.index(st.session_state.chat_choice)]
    
    #Selecting operating procedure based on "chat_choice"
    match translated_chat_choice:
        
        case "Chat":
            response = st.session_state['llm_chain'].call(translated_user_prompt)
        
        case "Chat With JBML Documents":
            response = ''
            airesponse, context, metadata = st.session_state['llm_chain'].call_jbml(user_prompt)
            citation = get_jbml_citation(metadata)
            sources = ''.join(citation)
            for c in context:
                response += f"\n\n \"{c}\"\n\n"
            
            response +=  "Sources: \n"
            
            response += f"\n{sources} \n\n"
            response += f"\n\n{ts.translate_to(airesponse, st.session_state['language'])}"

        case "Chat with the Web":
            results, over_rate_limit = get_web_search(st.session_state['web_engine'] , user_prompt)



            airesponse = st.session_state['llm_chain'].call_web(user_prompt, results)
            airesponse = st.session_state['llm_chain'].call_web(user_prompt, results)

            citation = get_web_citation(results)
            response = f"{ts.translate_to(airesponse, st.session_state['language'])}"
            sources = ''.join(citation)
            
            response +=  "\n\nSources: \n"
            
            response += f"\n{sources} \n\n"
        case "Chat With Uploaded Documents":
            response = ''
            info = st.session_state.file_adder.get_stored()
            if len(info) == 0:
                response = "I can not answer a document question without any uploaded documents. Please upload some documents before asking me again."
            else:
                json_data = {"query":user_prompt, "docs":[]}
                location = ""
                for doc in info:
                    if "row" in doc.metadata:
                        location = "Row: " + str(doc.metadata["row"])
                    elif "page" in doc.metadata:
                        location = "Page: " + str(doc.metadata["page"])
                    else:
                        location = "unknown"
                    json_data["docs"].append({"page_content":doc.page_content,"metadata":{"source":doc.metadata["source"], "location":location}})
                
                airesponse, relevant_data = st.session_state['llm_chain'].call_uploaded(user_prompt, json_data)
                context = []
                metadata = []
                for data in relevant_data["docs"]:
                    context.append(data["page_content"])
                    metadata.append(data["metadata"])
                citation = get_uploaded_citation(metadata)
                sources = ''.join(citation)
                for c in context:
                    response += f"\n\n \"{c}\"\n\n"
                
                response +=  "Sources: \n"
                
                response += f"\n{sources} \n\n"
                
                response += f"\n\n{ts.translate_to(airesponse, st.session_state['language'])}"


        case _:
            response = const.chat_selection_error_dict[st.query_params.language]
  
   #Translate back to selected language after calling model
    translated_response = ts.translate_to(response, st.query_params['language'])
    def stream_data():
        for word in translated_response.split(" "):
            yield word + " "
            time.sleep(0.01)

   #Add the response to the session state
    st.session_state.messages.append(
        {"role": "assistant", "content": translated_response}
    )

    with st.chat_message("assistant"):
        box = st.empty()
        box.write_stream(stream_data)

    #Check to see if the chain exceeds the maximum length
    if get_len(st.session_state['llm_chain'].chain) > const.MAX_CHAIN_LENGTH: 
        
        print("Summarizing Chain: \n")
        st.session_state['llm_chain'].summarize_chain(const.MIN_SUM_LENGTH)
        
        #Check to see if the chain still exceeds the maximum length
        if get_len(st.session_state['llm_chain'].chain) > const.MAX_CHAIN_LENGTH:
            
            print("Chain Too Long - Ending Session")
            #Disable chat input
            st.session_state.disabled = True
            st.rerun()
    #Check to see if the chain exceeds the maximum length
    if get_len(st.session_state['llm_chain'].chain) > const.MAX_CHAIN_LENGTH: 
        
        print("Summarizing Chain: \n")
        st.session_state['llm_chain'].summarize_chain(const.MIN_SUM_LENGTH)
        
        #Check to see if the chain still exceeds the maximum length
        if get_len(st.session_state['llm_chain'].chain) > const.MAX_CHAIN_LENGTH:
            
            print("Chain Too Long - Ending Session")
            #Disable chat input
            st.session_state.disabled = True
            st.rerun()

    # except:
    #     st.warning(st.session_state.error_message)
    

