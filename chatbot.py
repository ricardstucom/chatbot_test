import os #Variables de entorno
from openai import OpenAI #CLiente OpenAi

api_key = os.environ.get("OPENAI_API_KEY") #Busca en el entorno la variable 'OPENAI_API_KEY'
client = OpenAI(api_key=api_key) #Creas el cliente

print("Escriu 'sortir' per acabar.") #Informativo para que el usuario sepa cerrar el chat

messages = [
    {"role": "system", "content": "Ets un assistent amable de la UOC. Respon en català, clar i breu."} #Marco el comportamiento del modelo / System: personalidad del bot
]

while True: #Bucle conversación
    missatge = input("Tu: ").strip() #Leo y limpio espacios

    if missatge.lower() == "sortir": #Comando salida
        print("Chatbot: Adéu!")
        break

    messages.append({"role": "user", "content": missatge}) #Guardo mensaje en el historial para recordar contexto

    resp = client.chat.completions.create(
        model="gpt-4o-mini",      # Llamada al modelo
        messages=messages,         # Envio todo el historial
        temperature=0.4 #Variabilidad de las respuestas
    )

    #El cliente retorna resp que és un objeto con una lista de choices (en este caso 1)
    resposta = resp.choices[0].message.content.strip() #Extraigo el contenido y limpio
    print("Chatbot:", resposta)

    messages.append({"role": "assistant", "content": resposta}) #Guardo la respuesta en el historialcl