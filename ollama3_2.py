import requests
import json
import tkinter as tk
from tkinter import scrolledtext
from tkinter import Menu

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

def exit_app():
    root.destroy()

def show_help():
    help_window = tk.Toplevel(root)
    help_window.title("Hilfe")
    help_label = tk.Label(help_window, text="Dies ist ein einfacher Dialog mit Ollama.")
    help_label.pack(padx=10, pady=10)

def select_model():
    model_window = tk.Toplevel(root)
    model_window.title("Modell auswählen")
    model_label = tk.Label(model_window, text="Wähle ein Modell aus:")
    model_label.pack(padx=10, pady=10)
    # Hier können weitere Widgets hinzugefügt werden, um ein Modell auszuwählen

root = tk.Tk()
root.title("Ollama Dialog")

# Menüleiste hinzufügen
menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Beenden", command=exit_app)
menu_bar.add_cascade(label="Datei", menu=file_menu)

model_menu = Menu(menu_bar, tearoff=0)
model_menu.add_command(label="Modell auswählen", command=select_model)
menu_bar.add_cascade(label="Modell", menu=model_menu)

help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Hilfe", command=show_help)
menu_bar.add_cascade(label="Hilfe", menu=help_menu)

prompt_label = tk.Label(root, text="Gib deinen Prompt ein:")
prompt_label.pack()

prompt_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
prompt_entry.pack()

submit_button = tk.Button(root, text="Senden", command=on_submit)
submit_button.pack()

response_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
response_text.pack()

root.mainloop()
