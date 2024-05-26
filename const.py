#Maximum desired chain length in characters
MAX_CHAIN_LENGTH = 7000
#Minimum prompt length to allow summarization
MIN_SUM_LENGTH = 100

language_dict = {
    "English": 0,
    "Espanol": 1,
    "Français": 2,
    "Deutsch": 3,
    "Português": 4
}
chat_selection_error_dict = {
    "English": 'An error has occured, please select a type of chat you would like',
    "Espanol": 'Se ha producido un error, seleccione el tipo de chat que desee',
    "Français": "Une erreur s'est produite, veuillez sélectionner le type de chat que vous souhaitez",
    "Deutsch": 'Er is een fout opgetreden, selecteer het type chat dat u wilt',
    "Português": 'Ocorreu um erro, selecione o tipo de chat que você deseja'
}
select_box_text_dict = {
    "English": "Select a Language",
    "Espanol": "Selecciona un idioma",
    "Français": "Sélectionnez une langue",
    "Deutsch": "Selecteer een taal",
    "Português": "Selecione um idioma"
}
button_text_dict = {
    "English": "Clear History",
    "Espanol": "Borrar historial",
    "Français": "Histoire claire",
    "Deutsch": "Geschiedenis wissen",
    "Português": "Apagar o histórico"
}
radio_text_dict = {
    "English": "Select what type of chat you would like!",
    "Espanol": "¡Selecciona qué tipo de chat te gustaría!",
    "Français": "Sélectionnez le type de chat que vous souhaitez !",
    "Deutsch": "Selecteer welk type chat je wilt!",
    "Português": "Selecione que tipo de bate-papo você gostaria!"
}
radio_list_dict = {
    "English": ["Chat", "Chat With JBML Documents", "Chat With Uploaded Documents", "Chat with the Web"],
    "Espanol": ["Charlar", "Chat con documentos JBML", "Chatear con documentos cargados", "Chatea con la Web"],
    "Français": ["Bavarder", "Discutez avec des documents JBML", "Discutez avec des documents téléchargés", "Discutez avec le Web"],
    "Deutsch": ["Praten", "Chat met JBML-documenten", "Chatten Sie mit hochgeladenen Dokumenten", "Chatten met internet"],
    "Português": ["Conversar", "Converse com documentos JBML", "Converse com documentos enviados", "Converse com a Web"],
 
}
stt_text_dict = {
    "English" : ["Start Recording", "Stop Recording"],
    "Espanol" : ["Empezar a grabar", "Para de grabar"],
    "Français" : ["Commencer l'enregistrement", "Arrête d'enregistrer"],
    "Deutsch" : ["Begin met opnemen", "Stop met opnemen"],
    "Português" : ["Comece a gravar", "Pare de gravar"],
}
messages_text_dict = {
    "English" : [{"role": "assistant", 
                 "content": "How may I help you today?"},],
    "Espanol": [{"role": "assistant", 
                "content": "¿Como puedo ayudarte hoy?"},],
    "Français": [{"role": "assistant", 
                 "content": "Comment puis-je vous aider aujourd'hui?"},],
    "Deutsch": [{"role": "assistant", 
                "content": "Hoe kan ik je vandaag helpen?"},],
    "Português": [{"role": "assistant", 
                  "content": "Como posso te ajudar, hoje?"},]
}
error_message_dict = {
    "English": "Oops! Something went wrong! Please try again later",
    "Espanol": "¡Ups! ¡Algo salió mal! Inténtalo de nuevo más tarde",
    "Français": "Oups ! Quelque chose s'est mal passé ! Veuillez réessayer plus tard",
    "Deutsch": "Oeps! Er is iets misgegaan! Probeer het later opnieuw",
    "Português": "Opa! Algo deu errado! Tente novamente mais tarde"
}
warning_text_dict ={
    "English": "You have reached the end of this conversation. Please clear chat to continue.",
    "Espanol": "Has llegado al final de esta conversación. Borra el chat para continuar.",
    "Français": "Vous avez atteint la fin de cette conversation. Veuillez effacer le chat pour continuer.",
    "Deutsch": "Je bent aan het einde van dit gesprek gekomen. Wis de chat om door te gaan.",
    "Português": "Você chegou ao fim desta conversa. Limpe o bate-papo para continuar."
}
chat_input_text_dict = {
    "English": "Your Message Here",
    "Espanol": "Su mensaje aquí",
    "Français": "Votre message ici",
    "Deutsch": "Jouw bericht hier",
    "Português": "Sua mensagem aqui"
}
file_options_dict = {
    "English": "Enter PDF, CSV, or XLSX files",
    "Espanol": "Ingrese archivos PDF, CSV o XLS",
    "Français": "Saisissez des fichiers PDF, CSV ou XLS",
    "Deutsch": "Geben Sie PDF-, CSV- oder XLS-Dateien ein",
    "Português": "Insira arquivos PDF, CSV ou XLS"
}
upload_button_dict = {
    "English": "UPLOAD",
    "Espanol": "SUBIR",
    "Français": "TÉLÉCHARGER",
    "Deutsch": "HOCHLADEN",
    "Português": "CARREGAR"
}
