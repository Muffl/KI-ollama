import requests
import json
import tkinter as tk
from tkinter import scrolledtext

def query_ollama(prompt, model="llama3.1:8b-instruct-q6_K"):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 4096,
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    # Jede Zeile einzeln parsen und die "response" zusammenfügen
    result_lines = []
    for line in response.text.splitlines():
        try:
            data_line = json.loads(line)
            result_lines.append(data_line.get("response", ""))
        except json.JSONDecodeError as e:
            print("Fehler beim Parsen einer Zeile:", e)
    
    return "".join(result_lines)

def on_submit():
    prompt = prompt_entry.get("1.0", tk.END).strip()
    if prompt.lower() in ["exit", "quit"]:
        root.destroy()
    else:
        antwort = query_ollama(prompt)
        response_text.config(state=tk.NORMAL)
        response_text.insert(tk.END, "\nAntwort von Ollama:\n" + antwort + "\n---\n")
        response_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Ollama Dialog")

prompt_label = tk.Label(root, text="Gib deinen Prompt ein:")
prompt_label.pack()

prompt_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
prompt_entry.pack()

submit_button = tk.Button(root, text="Senden", command=on_submit)
submit_button.pack()

response_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
response_text.pack()

root.mainloop()
