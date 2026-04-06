import Ollma

client = Ollma(base_url="http://localhost:11434")

response = client.chat(model="llama3.2", messages=[{"role": "user", "content": "Hello, how are you?"}])

print(response)