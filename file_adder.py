from logging import NullHandler
import os
from pprint import pprint
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document


#Given the App in question and files, it adds said files to the embeddings model
class FileAdder:
    def __init__(self, chunk=2500, overlap=150):
        self.stored_info = []
        
        self.text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk,
        chunk_overlap=overlap,
        length_function=len,
        is_separator_regex=False)
        

#Given the file location (Do websites have files? Is it on a file in the server the website is running on?) adds the file to the app
#csv/excel of a certain size will break this, depends on LLM, add ability to divide into chunks
#Possible Error when location doesn't exist, need to handle it
#might be a better way to remove the new csv files
    def add(self, uploadedFile):

        #code = ''.join(random.choices(String.ascii_uppercase + String.ascii_lowercase))
        file_name = uploadedFile.name
        location = "UploadedFiles\\" + file_name
        file = open(location, "wb")
        file.write(uploadedFile.getbuffer())
        file.close()

        try:

            if(".pdf" in file_name):
                
                loader = PyPDFLoader(location)
                docs = loader.load_and_split(text_splitter=self.text_splitter)
                
                for doc in docs:
                    self.stored_info.append(doc)

            elif(".csv" in file_name):

                loader = CSVLoader(file_path=location)
                docs = loader.load()
                
                for doc in docs:
                    self.stored_info.append(doc)

            elif(".xls" in file_name or ".xlsx" in file_name or ".xlsm" in file_name):

                newLocation = location[:location.find(".")]+".csv"
                df = pd.read_excel(location)
                df.to_csv(newLocation, index=True)
                loader = CSVLoader(file_path=newLocation)
                docs = loader.load()

                for doc in docs:
                    self.stored_info.append(doc)

                #trash
                df = None
                os.remove(newLocation)

            else:
                print("Unexpected File Type")

            os.remove(location)
            
        except PermissionError:
            print("We do not have the access (" + file_name + ")")
        except FileNotFoundError:
            print("(" + file_name + ")" + "was not found and was not added")
        except:
            print("An error occured while adding (" + file_name + ")")
            os.remove(location)
            
    def get_stored(self):
        return self.stored_info

    def reset(self):
        self.stored_info = []
