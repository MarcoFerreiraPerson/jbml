from logging import NullHandler
import os
import io
import pprint
import pandas as pd
from embedchain import App
#import random
#import string

#Given the App in question and files, it adds said files to the embeddings model
class file_adder:
    def __init__(self):
        self.app = App.from_config(config_path="config.yaml")
        file = open("FunkyFile.csv", "a")
        file.close()
        #self.app.add("FunkyFile.csv", data_type='csv')

    def add(self, uploadedFile):
        #code = ''.join(random.choices(String.ascii_uppercase + String.ascii_lowercase))
        file_name = uploadedFile.name
        location = "UploadedFiles\\" + file_name
        file = open(location, "wb")
        file.write(uploadedFile.getbuffer())
        file.close()
        
        try:

            if(".pdf" in file_name):

                self.app.add(location, data_type='pdf_file')

            elif(".csv" in file_name):

                self.app.add(location, data_type='csv')

            elif(".xls" in file_name or ".xlsx" in file_name or ".xlsm" in file_name):

                new_location = location[:location.find(".")]+".csv"
                df = pd.read_excel(location)
                df.to_csv(new_location, index=True)
                self.app.add(new_location, data_type='csv')

                #trash
                df = None
                os.remove(new_location)

            else:
                print("Error: Unexpected File Type")
    
        except PermissionError:
            print("Error: We do not have the access (" + location + ")")
        except FileNotFoundError:
            print("Error: (" + location + ")" + "was not found and was not added")
        except Exception as exception:
            print("Error: An error occured while adding (" + location + ")\n" + str(exception))
        else:
            os.remove(location)

    def reset(self):
        self.app.reset()
    
    
    def get_context(self, prompt:str, documents = 3):
        self.info = self.app.search(prompt)
        self.document_info = {
            "context": [],
            "metadata": []
        }
        for x in self.info:
            info_location = ""
            if "page" in x["metadata"]:
                info_location = "page " +  str(x["metadata"]["page"])
            elif "row" in x["metadata"]:
                info_location = "row " + str(x["metadata"]["row"])
            self.document_info["context"].append(x["context"])
            self.document_info["metadata"].append( {
                'file_name': x["metadata"]["url"][x["metadata"]["url"].rfind("\\")+1:],
                'page_label': info_location
            })
        return self.document_info
 