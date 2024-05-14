import re
import translators as ts



def translate_to(text: str, current_language: str):
      """Translate text from English

      :param text: Text to translate.
      :param current_language: Language to translate to.

      :Returns str:
            if current_language == "English": text
            else: Translated text
      """
      if not current_language == "English":
        try:
            markdown_list = re.split("(```.+?```)",text,flags=re.DOTALL)
            output=""
            #Retains MARKDOWN in English
            for split in markdown_list:
                if not split[0]== "`":
                    output += ts.translate_text(split, 'google', 'auto', conv_language(current_language))
                
                else:
                    output+=split
           
            return output
        
        except:
            return text
      
      else:
        return text
    


def translate_from(text: str, current_language:str ):
    """Translate to English
    :param text: Text to translate.
    :param current_language: Language to translate from.

    :Returns str:
            if current_language == "English": text
            else: Translated text
    """
    if not current_language == "English":
        try:
            output = ts.translate_text(text, 'google','auto','en')
            return output
        except:
            return text
    return text

def conv_language(language: str):
    """Converts language to language code
    :param language: language

    :Returns str: language code
    """
    match language:
        case "English":
            converted_language = 'en'
        case "Espanol":
            converted_language = 'es'
        case "Français":
            converted_language = 'fr'
        case "Deutsch":  
            converted_language = 'de'
        case "Português":
            converted_language = 'pt'
        case _:
            converted_language = 'en'
    return converted_language
