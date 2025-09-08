from typing import List, Dict, Tuple
from config import MAX_TURNS
from storage import guardar_historial

def truncate_messages(msgs: List[Dict[str, str]], max_turns: int = MAX_TURNS) -> List[Dict[str, str]]:
    """
    Manté el primer missatge 'system' (si hi és) i les darreres 2*max_turns entrades.
    """
    if not msgs:
        return msgs
    system = msgs[0] if msgs[0].get("role") == "system" else None
    rest = msgs[1:] if system else msgs
    tail = rest[-2 * max_turns :]
    return [system] + tail if system else tail

def gestionar_ordres(missatge: str,
                     messages: List[Dict[str, str]],
                     default_history: List[Dict[str, str]]
                    ) -> Tuple[List[Dict[str, str]], str]:
    """
    Processa ordres locals. Retorna (messages, accio):
      - accio = "exit"    → cal acabar
      - accio = "handled" → ordre gestionada; no cal cridar el model
      - accio = "none"    → no és ordre; seguim flux normal
    """
    low = missatge.lower()

    if low in ("sortir", "adeu", "adéu"):
        guardar_historial(messages)
        print("Chatbot: Adéu! (conversa desada)")
        return messages, "exit"

    if low == "guarda":
        guardar_historial(messages)
        print("Chatbot: Conversa desada.")
        return messages, "handled"

    if low in ("reset", "nova conversa", "reinicia"):
        messages = default_history.copy()
        guardar_historial(messages)
        print("Chatbot: Conversa reiniciada i desada.")
        return messages, "handled"

    return messages, "none"

def generar_resposta(client,  # objecte OpenAI
                     messages: List[Dict[str, str]],
                     model: str,
                     temperature: float = 0.4) -> str:
    """Crida l'API amb l'historial i retorna el text de resposta."""
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return ("Sembla que hi ha un problema amb el servei d'IA. "
                "Torna-ho a provar d'aquí una estona.")
