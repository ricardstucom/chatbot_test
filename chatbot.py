import os #Variables de entorno
from openai import OpenAI #CLiente OpenAi

def ensure_api_key() -> str: #(-> str) : informa que retorna un string pero no modicia res. Només és per programadors o i eines
    api_key = os.environ.get("OPENAI_API_KEY") #Busca en el entorno la variable 'OPENAI_API_KEY'

    if not api_key:
        # Missatge clar si falta la clau
        raise RuntimeError(
            "Falta la variable d'entorn OPENAI_API_KEY.\n"
            "En PowerShell: $env:OPENAI_API_KEY=\"LA_TEVA_CLAU\"\n"
            "Torna a executar després d'establir-la."
        )
    return api_key

def truncate_messages(msgs, max_turns=MAX_TURNS): #msgs: és tot l'historial  max-turns serveix per enviar X blocks de converses posteriors pel context. Aixi no envies cada vegada tot l'historial
    """
    Manté el primer missatge 'system' (si hi és) i les darreres
    2*max_turns entrades (user/assistant). Això evita que el context creixi massa.
    """
    if not msgs:
        return msgs
    system = msgs[0] if msgs[0].get("role") == "system" else None #Mira el primer missatge per si te role 'system'
    rest = msgs[1:] if system else msgs #Si hi havia system llavors mira rest desde l'1 cap endavant. Si system no te res llavors passa tota la llista
    tail = rest[-2*max_turns:] #Agafa els darrers missatges per no haver d'estar enviant l'historial tota l'estona.
    return [system] + tail if system else tail


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

    messages.append({"role": "assistant", "content": resposta}) #Guardo la respuesta en el historial