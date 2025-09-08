# 🤖 Chatbot UOC

Un petit projecte de chatbot en **Python** utilitzant l'API d'**OpenAI**, creat com a exercici d'aprenentatge.
El bot respon en català, recorda les converses i ofereix ordres bàsiques de gestió.

---

## ✨ Funcionalitats

- Respostes generades amb el model `gpt-4o-mini`.
- Persistència de conversa en `historial.json` (recorda entre sessions).
- Truncat de context (`MAX_TURNS`) per fer el bot més eficient.
- Ordres disponibles:
  - `guarda` → desa manualment la conversa.
  - `reset` / `nova conversa` / `reinicia` → reinicia l'historial.
  - `sortir` → surt i desa.
- Gestió neta de `Ctrl+C` (interrupció manual).

---

## 🛠️ Estructura del projecte

chatbot_uoc/
├─ main.py # punt d'entrada
├─ config.py # configuració (MODEL, MAX_TURNS, HISTORY_PATH)
├─ storage.py # persistència JSON
├─ logic.py # lògica de xat i ordres
├─ io_utils.py # entrada d'usuari
└─ requirements.txt

---

## ▶️ Execució

1. Instal·la dependències:

   ```bash
   pip install -r requirements.txt

   ```

2. Defineix la teva clau d'API:

$env:OPENAI_API_KEY="LA_TEVA_CLAU"

3. Executa el programa:

python main.py

Exemple d'ús

Tu: Hola
Chatbot: Hola! Com estàs?

Tu: guarda
Chatbot: Conversa desada.

Tu: reset
Chatbot: Conversa reiniciada i desada.

Tu: sortir
Chatbot: Adéu! (conversa desada)
