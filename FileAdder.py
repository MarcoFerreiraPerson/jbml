from logging import NullHandler
import os
import io
import pprint
import pandas as pd
from embedchain import App

#Given the App in question and files, it adds said files to the embeddings model
class FileAdder:
    def __init__(self):
        self.app = App.from_config(config_path="config.yaml")

    def add(self, uploadedFile):
        try:
            fileName = uploadedFile.name
            location = os.getcwd() + "\\UploadedFiles" + fileName
            file = open(location, "wb")
            file.write(uploadedFile.getValue())
            file.close()   

            if(".pdf" in fileName):

                self.app.add(location, data_type='pdf_file')

            elif(".csv" in fileName):

                self.app.add(location, data_type='csv')

            elif(".xls" in fileName or ".xlsx" in fileName or ".xlsm" in fileName):

                newLocation = location[:location.find(".")]+".csv"
                df = pd.read_excel(location)
                df.to_csv(newLocation, index=True)
                self.app.add(newLocation, data_type='csv')

                #trash
                df = None
                os.remove(newLocation)

            else:
                print("Error: Unexpected File Type (learn how to throw errors in python)")
        except PermissionError:
            print("Error: We do not have the access (" + location + ")")
        except FileNotFoundError:
            print("Error: (" + location + ")" + "was not found and was not added")
        except:
            print("Error: An error occured while adding (" + location + ")")
        else:
            os.remove(location)
    
    def getContext(self, prompt, documents = 3):
        self.info = self.app.search(prompt, num_documents = documents)
        self.context = []
        self.metaData = []
        for x in self.info:
            self.context.append(x["context"])
            self.metaData.append(x["metadata"])
        return self.context,self.metaData
        
            