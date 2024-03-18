import translators as ts


def translate_to(text, current_language):
    output = ts.translate_text(text, 'google', 'auto', current_language)
    return output


def translate_from(text, current_language):
    output = ts.translate_text(text, 'google', current_language, 'en')
    return output
