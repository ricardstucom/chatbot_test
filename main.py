import os
from typing import List, Dict
from openai import OpenAI

from config import MODEL, MAX_TURNS, HISTORY_PATH
from storage import load_json, guardar_historial
from logic import truncate_messages, gestionar_ordres, generar_resposta
from io_utils import llegir_missatge

def ensure_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Falta la variable d'entorn OPENAI_API_KEY.\n"
            "En PowerShell: $env:OPENAI_API_KEY=\"LA_TEVA_CLAU\"\n"
            "Torna a executar després d'establir-la."
        )
    return api_key

def main():
    api_key = ensure_api_key()
    client = OpenAI(api_key=api_key)

    default_history: List[Dict[str, str]] = [
        {"role": "system", "content": "Ets un assistent amable de la UOC. Respon en català, clar i breu."}
    ]

    # Carrega historial o inicia amb system
    messages: List[Dict[str, str]] = load_json(HISTORY_PATH, default=default_history.copy())

    # Si no existeix el fitxer, crea'l d'entrada
    if not os.path.exists(HISTORY_PATH):
        guardar_historial(messages)

    print("Escriu 'sortir' per acabar (o Ctrl+C).")
    print("Ordres: 'reset' (nova conversa) · 'guarda' (desar manual)")

    try:
        while True:
            missatge = llegir_missatge()

            # 1) Ordres locals
            messages, accio = gestionar_ordres(missatge, messages, default_history)
            if accio == "exit":
                break
            if accio == "handled":
                continue

            # 2) Flux normal: afegir missatge i truncar
            messages.append({"role": "user", "content": missatge})
            messages = truncate_messages(messages, MAX_TURNS)

            # 3) Cridar el model
            resposta = generar_resposta(client, messages, model=MODEL, temperature=0.4)
            print("Chatbot:", resposta)

            # 4) Guardar resposta i persistir
            messages.append({"role": "assistant", "content": resposta})
            guardar_historial(messages)

    except KeyboardInterrupt:
        guardar_historial(messages)
        print("\nChatbot: Adéu! (interromput per usuari; conversa desada)")

if __name__ == "__main__":
    main()
