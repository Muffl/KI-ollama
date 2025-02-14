

import requests
import json

def query_ollama(prompt, model="llama3.1:8b-instruct-q6_K"):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 256,
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

def main():
    while True:
        prompt = input("Gib deinen Prompt ein (oder 'exit' zum Beenden): ")
        if prompt.lower() in ["exit", "quit"]:
            print("Programm beendet.")
            break
        antwort = query_ollama(prompt)
        print("\nAntwort von Ollama:")
        print(antwort)
        print("\n---")  # Trenner zwischen den Antworten

if __name__ == '__main__':
    main()
