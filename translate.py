import translators as ts


def translate_to(text, current_language):
    if not current_language == "English":
        try:
            output = ts.translate_text(text, 'google', 'auto', conv_language(current_language))
            return output
        except:
            return text
    else:
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
