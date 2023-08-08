from chatnoir_api.chat import chat

api_key: str = input("API key: ")
input_sentence: str = input("Input: ")

response = chat(api_key, input_sentence)
print(f"Response: {response}")
