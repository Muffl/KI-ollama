import requests
import json
import tkinter as tk
from tkinter import scrolledtext
from tkinter import Menu

current_model = "llama3.1:8b-instruct-q6_K"

def query_ollama(prompt, model=current_model):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 4096,
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    result_lines = []
    for line in response.text.splitlines():
        try:
            data_line = json.loads(line)
            result_lines.append(data_line.get("response", ""))
        except json.JSONDecodeError as e:
            print("Fehler beim Parsen einer Zeile:", e)
    
    return "".join(result_lines)
"""
def get_available_models():
    url = "http://localhost:11434/api/models"
    try:
        response = requests.get(url)
        raw_data = response.text  # Debugging: Inspect raw data
        print("Rohdaten der API:", raw_data)  # Ausgabe der Rohdaten für die Fehlerdiagnose
        models = json.loads(raw_data)  # Parse der JSON-Daten
        return models
    except Exception as e:
        print("Fehler beim Abrufen der Modelle:", e)
        return []
"""
def on_submit():
    prompt = " " +  prompt_entry.get("1.0", tk.END).strip()
    if prompt.lower() in ["exit", "quit"]:
        root.destroy()
    else:
        antwort = query_ollama(prompt)
        response_text.config(state=tk.NORMAL)
        response_text.delete("1.0", tk.END)
        response_text.insert(tk.END, " " + "\nAntwort von Ollama:\n" + antwort + "\n---\n")
        response_text.config(state=tk.DISABLED)

def exit_app():
    root.destroy()

def show_help():
    help_window = tk.Toplevel(root)
    help_window.title("Hilfe")
    help_label = tk.Label(help_window, text="Dies ist ein einfacher Dialog mit Ollama.")
    help_label.pack(padx=10, pady=10)

def select_model():
    global current_model
    
    model_window = tk.Toplevel(root)
    model_window.title("Modell auswählen")
    model_label = tk.Label(model_window, text="Wähle ein Modell aus:")
    model_label.pack(padx=10, pady=10)
    
    available_models = get_available_models()
    
    def set_model(selected_model):
        global current_model
        current_model = selected_model
        print(f"Gewähltes Modell: {current_model}")
        model_window.destroy()

    for model in available_models:
        model_button = tk.Button(model_window, text=model, command=lambda m=model: set_model(m))
        model_button.pack(padx=5, pady=5)

root = tk.Tk()
root.title("Ollama Dialog")

menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Beenden", command=exit_app)
menu_bar.add_cascade(label="Datei", menu=file_menu)
"""
model_menu = Menu(menu_bar, tearoff=0)
model_menu.add_command(label="Modell auswählen", command=select_model)
menu_bar.add_cascade(label="Modelle", menu=model_menu)
"""
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Hilfe", command=show_help)
menu_bar.add_cascade(label="Hilfe", menu=help_menu)

prompt_label = tk.Label(root, text="Gib deinen Prompt ein:")
prompt_label.pack(padx=11)

prompt_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
prompt_entry.pack(padx=11)

submit_button = tk.Button(root, text="Senden", command=on_submit)
submit_button.pack(padx=11)

response_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
response_text.pack(padx=11)

root.mainloop()
