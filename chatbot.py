import os  # caixa d’eines
import json
from typing import Any, List, Dict  # Per dir quin tipus s'espera
from openai import OpenAI  # Client OpenAI

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

def ensure_api_key() -> str:  # (-> str) : informa que retorna un string però no modifica res.
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Falta la variable d'entorn OPENAI_API_KEY.\n"
            "En PowerShell: $env:OPENAI_API_KEY=\"LA_TEVA_CLAU\"\n"
            "Torna a executar després d'establir-la."
        )
    return api_key

def truncate_messages(msgs, max_turns=MAX_TURNS):
    """
    Manté el primer missatge 'system' (si hi és) i les darreres
    2*max_turns entrades (user/assistant). Això evita que el context creixi massa.
    """
    if not msgs:
        return msgs
    system = msgs[0] if msgs[0].get("role") == "system" else None
    rest = msgs[1:] if system else msgs
    tail = rest[-2 * max_turns :]
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
    messages: List[Dict[str, str]] = load_json(HISTORY_PATH, default=default_history.copy())

    # (Opcional) Si no existeix encara el fitxer, crea'l ja
    if not os.path.exists(HISTORY_PATH):
        save_json(HISTORY_PATH, messages)

    print("Escriu 'sortir' per acabar (o Ctrl+C).")
    print("Ordres: 'reset' per iniciar conversa nova, 'guarda' per desar manualment.")

    def llegir_missatge():
        return input("Tu: ").strip()

    def gestionar_ordres(missatge, messages):
        low = missatge.lower()

        if low == "guarda":
            save_json(HISTORY_PATH, messages)
            print("Chatbot: Conversa desada.")
            return messages, True

        if low in ("reset", "nova conversa", "reinicia"):
            messages = default_history.copy()
            save_json(HISTORY_PATH, messages)
            print("Chatbot: Conversa reiniciada i desada.")
            return messages, True

        # Flux normal: afegim el missatge d'usuari i trunquem
        messages.append({"role": "user", "content": missatge})
        messages = truncate_messages(messages, MAX_TURNS)
        return messages, False

    try:
        while True:
            missatge = llegir_missatge()

            if missatge.lower() == "sortir":
                save_json(HISTORY_PATH, messages)
                print("Chatbot: Adéu!")
                break

            # 3) Ordres locals útils
            messages, handled = gestionar_ordres(missatge, messages)
            if handled:
                continue

            try:
                resp = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    temperature=0.4
                )
                resposta = resp.choices[0].message.content.strip()
            except Exception:
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
