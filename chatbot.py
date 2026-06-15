import ollama

print("🤖 Your Local Chatbot is Ready!")
print("Model: gemma3:4b")
print("Type 'exit' to quit.\n")

messages = []

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
        print("👋 Goodbye! See you next time!")
        break
    
    if not user_input:
        continue

    messages.append({'role': 'user', 'content': user_input})
    
    print("Bot: ", end="", flush=True)
    response = ""
    
    for chunk in ollama.chat(model="gemma3:4b", messages=messages, stream=True):
        content = chunk['message']['content']
        print(content, end="", flush=True)
        response += content
    
    print("\n")
    messages.append({'role': 'assistant', 'content': response})
