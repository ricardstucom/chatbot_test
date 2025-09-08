import os
import json
from typing import Any, List, Dict
from config import HISTORY_PATH

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

def guardar_historial(messages: List[Dict[str, str]]) -> None:
    """Desa l'historial global al fitxer HISTORY_PATH."""
    save_json(HISTORY_PATH, messages)
