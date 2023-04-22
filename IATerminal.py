import openai
import os

openai.api_key = 'pon tu api key de openai aquí (debes tener habilitado el uso de gpt-4)'
model_id = 'gpt-4'

def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation

def execute_command(command):
    try:
        result = os.popen(command).read()
        return result
    except Exception as e:
        return f"Error al ejecutar el comando: {str(e)}"

conversation = []
conversation.append({'role': 'system', 'content': 'Eres una ia que puede ejecutar comandos en la terminal de una mac usando el comando ejecuta:comando. Un usuario te pedirá que hacer y tu responderás con el comando unicamente y nada más, si te pide varias cosas hazlo en un solo comando. Ejemplo: Usuario: Crea una carpeta en escritorio IA:ejecuta:mkdir ~/Desktop/NOMBRE_DE_LA_CARPETA Ahora inicia la conversación:'})
conversation = ChatGPT_conversation(conversation)
print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))

while True:
    prompt = input('User:')
    conversation.append({'role': 'user', 'content': prompt})
    conversation = ChatGPT_conversation(conversation)
    response = conversation[-1]['content'].strip()
    print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), response))

    # Ejecutar comandos si la respuesta es un comando de terminal
    if response.startswith("Ejecuta:") or response.startswith("ejecuta:"):
        command = response[8:].strip()
        print("Ejecutando comando:", command)
        command_result = execute_command(command)
        print("Resultado del comando:\n", command_result)
