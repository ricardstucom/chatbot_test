import os #caixa d’eines
import json
from typing import Any, List, Dict #Per dir quin tipus s'espera
from openai import OpenAI #Cliente OpenAi

# ---------- Config ----------
MODEL = "gpt-4o-mini"
MAX_TURNS = 20  # Nombre de torns (usuari+assistent) que mantindrem al context
HISTORY_PATH = "historial.json"

# ---------- Helpers JSON ----------
def load_json(path: str, default: Any) -> Any:
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"(Avís) No s'ha pogut llegir {path}: {e}")
    return default

def save_json(path: str, data: Any) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"(Avís) No s'ha pogut desar {path}: {e}")

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

def main():
    api_key = ensure_api_key()
    client = OpenAI(api_key=api_key)
  # 1) Carreguem historial si existeix; sinó, el creem amb system
    default_history = [
        {
            "role": "system",
            "content": "Ets un assistent amable de la UOC. Respon en català, clar i breu."
        }
    ]
    messages: List[Dict[str, str]] = load_json(HISTORY_PATH, default=default_history)
    print("Escriu 'sortir' per acabar (o Ctrl+C).")
    print("Ordres: 'reset' per iniciar conversa nova, 'guarda' per desar manualment.")


    try:
        while True:
            missatge = input("Tu: ").strip()
            if missatge.lower() == "sortir":
                 # Desem l'historial actual abans d'acabar
                save_json(HISTORY_PATH, messages)
                print("Chatbot: Adéu!")
                break

             # 3) Ordres locals útils
            if missatge.lower() == "guarda":
                save_json(HISTORY_PATH, messages)
                print("Chatbot: Conversa desada.")
                continue

            if missatge.lower() in ("reset", "nova conversa", "reinicia"):
                messages = default_history.copy() #Guardem pero reiniciat
                save_json(HISTORY_PATH, messages)
                print("Chatbot: Conversa reiniciada i desada.")
                continue

            messages.append({"role": "user", "content": missatge})
            messages = truncate_messages(messages, MAX_TURNS)

            try:
                resp = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    temperature=0.4
                )
                resposta = resp.choices[0].message.content.strip()
            except Exception as e:
                resposta = ("Sembla que hi ha un problema amb el servei d'IA. "
                            "Torna-ho a provar d'aquí una estona.")


            print("Chatbot:", resposta)
            messages.append({"role": "assistant", "content": resposta})

            # 4) Desem l'historial després de cada interacció
            save_json(HISTORY_PATH, messages)

    except KeyboardInterrupt:
            save_json(HISTORY_PATH, messages)
            print("\nChatbot: Adéu! (interromput per usuari)")

if __name__ == "__main__":
    main()

