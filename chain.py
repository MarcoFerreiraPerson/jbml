import requests
import re
from transformers import AutoTokenizer
import time
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
server_url = "https://penguin-true-cow.ngrok-free.app"
endpoint = "/generate/"
retrieve_endpoint = '/jbml_retrieve/'
summary_endpoint = '/summarize/'

class LLM_Chain:
    def __init__(self, system_prompt) -> None:
        self.chain = f"<s>[INST]{system_prompt}[/INST]Model answer</s> [INST] Follow-up instruction [/INST]"

    def call(self, prompt):
        self.chain += f"[INST]{prompt}[/INST]"
        encoded_prompt = requests.utils.quote(self.chain)
        response = requests.get(f"{server_url}{endpoint}?prompt={encoded_prompt}")
        if response.status_code == 200:
            result = response.json()
            self.chain += result
        else:
            print("Error:", response.status_code, response.text)
            result = None
        return result
    def call_jbml(self, prompt): 
        context, metadata = get_rag_prompt(prompt)        
        source_str = ''
        for i, c in enumerate(context):
            source_str += f"Source {i}: {c} \n\n\n"
        
        self.chain += f"[INST]{prompt} \nOnly use context from here for your response: \n{source_str} [End of context][/INST]"
        encoded_prompt = requests.utils.quote(self.chain)
        response = requests.get(f"{server_url}{endpoint}?prompt={encoded_prompt}")
        if response.status_code == 200:
            result = response.json()
            self.chain += result
            
        else:
            print("Error:", response.status_code, response.text)
            result = None
        return result, context, metadata
    
    @DeprecationWarning
    def stream(self, prompt):
        self.chain += f"[INST]{prompt}[/INST]"
        encoded_prompt = requests.utils.quote(self.chain)
        response = requests.get(f"{server_url}{endpoint}?prompt={encoded_prompt}")
        if response.status_code == 200:
            result = response.json()
            for char in result[0]:
                self.chain += char
        else:
            print("Error:", response.status_code, response.text)
            result = None
        yield result

    def summarize_chain(self):
        responses = list()
        responses = re.split(r"\[INST\].+?\[/INST\]", self.chain,flags=re.DOTALL)
        for i in range(3,len(responses)):
            
            start = time.time()
            summary_response = get_summary(responses[i])
            end = time.time()
            
            #Summary Time
            print(f"Summary Time: {end-start}")
            
            if summary_response.status_code == 200:
                summary = str(summary_response.json())
                replaced = responses[i].replace("\\n","\n")
                
                #Original-Summary Comparison
                print("Original: " + replaced)
                print("\nSummary: " + summary + "\n")

                self.chain = self.chain.replace(replaced, summary)
            else:
                print("Summarization Error: " + summary_response.status_code)
        
        #Shortened Chain
        print("New Chain: " + self.chain)


def get_rag_prompt(prompt):
    system_prompt = "You are an AI designed to take apart the important part of the prompt for Retrieval Search. Simplify the prompt given into a phrase used for search. Do not asnwer the question but simply rewrite them in an easier way for search"
    retrieval = f"<s>[INST]{system_prompt}[/INST] Model answer</s> [INST] Follow-up instruction [/INST]"
    
    
    retrieval += f"[INST]{prompt}[/INST]"
    encoded_retrieval = requests.utils.quote(retrieval)
    
    response = requests.get(f"{server_url}{endpoint}?prompt={encoded_retrieval}")
    
    if response.status_code == 200:
            result = response.json()
            print(result)
    else:
        print("Error:", response.status_code, response.text)
        result = prompt
    
    encoded_prompt = requests.utils.quote(result)
    context_json = requests.get(f"{server_url}{retrieve_endpoint}?prompt={encoded_prompt}")
    if context_json.status_code == 200:
        context = context_json.json()[0]
        metadata = context_json.json()[1]
    else:
        print("Error:", context.status_code, context.text)
        context, metadata = 'An error has occured', {}
    return context, metadata

def get_summary(text):
        encoded_text = requests.utils.quote(text)
        response = requests.get(f"{server_url}{summary_endpoint}?prompt={encoded_text}")
        return response