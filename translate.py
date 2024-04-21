import re
import translators as ts



def translate_to(text, current_language):
        # Regular expression to match markdown code blocks
        
        converted_text = text
        
        special_code = "567876545678"
        pattern = r'```(?:[^`]+|`(?!``))*```'
        code_blocks = re.findall(pattern, text, re.DOTALL)
        for code_block in code_blocks:
            converted_text = converted_text.replace(code_block, special_code)
    
        try:
            output = ts.translate_text(converted_text, 'google', 'auto', conv_language(current_language))
            for code_block in code_blocks: 
                output = output.replace(special_code, code_block)
            return output
        except:
            return text
    


def translate_from(text, current_language):
    if not current_language == "English":
        try:
            output = ts.translate_text(text, 'google', conv_language(current_language), 'auto')
            return output
        except:
            return text
    else:
        return text

def conv_language(language):
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
