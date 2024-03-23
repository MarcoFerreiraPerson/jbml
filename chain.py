import requests
import re

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
        self.chain += f"[INST]{prompt} \nOnly use context from here for your response: \n{context} [End of context][/INST]"
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

    def summarize_chain(self,MAX_CHAIN_LENGTH):
        responces = list()
        responces = re.split("\[INST\].+?\[/INST\]", self.chain,flags=re.DOTALL)
        for i in range(3,len(responces)):
            summary_responce = get_summary(responces[i])
            if summary_responce.status_code == 200:
                summary = str(summary_responce.json()[0])
                print(responces[i]+"\n")
                summary = summary.lstrip("{'summary_text': '")
                summary = summary.rstrip("'}")
                self.chain.replace(responces[i],summary[0])
        print(self.chain)
        if len(self.chain) > MAX_CHAIN_LENGTH:
            return True
        else:
            return False
            


def get_rag_prompt(prompt):
    system_prompt = "You are an AI designed to take apart the important part of the prompt for Retrieval Search. Return the phrase or words that are unknown to you or you need more information about."
    retrieval = f"<s>[INST]{system_prompt}[/INST] Model answer</s> [INST] Follow-up instruction [/INST]"
    
    
    retrieval += f"[INST]{prompt}[/INST]"
    encoded_prompt = requests.utils.quote(prompt)
    context_json = requests.get(f"{server_url}{retrieve_endpoint}?prompt={encoded_prompt}")
    if context_json.status_code == 200:
        context = context_json.json()[0]
        metadata = context_json.json()[1]
    else:
        print("Error:", context.status_code, context.text)
        context, metadata = 'An error has occured', {}
    return context, metadata

def get_summary(text):
        response = requests.get(f"{server_url}{summary_endpoint}?prompt={text}")
        return response