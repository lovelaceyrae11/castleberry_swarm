import requests
try:
    res = requests.get("http://localhost:11434/api/tags")
    print("Available local models:", [m['name'] for m in res.json().get('models', [])])
except Exception as e:
    print("Error connecting to Ollama:", e)
