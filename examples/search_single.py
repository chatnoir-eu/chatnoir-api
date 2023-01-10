from chatnoir_api.v1 import search, search_phrases

api_key: str = input("API key: ")

top_result_search = next(iter(
    search(api_key, "python library")
))
print(top_result_search)

top_result_search_phrases = next(iter(
    search_phrases(api_key, "python library", )
))
print(top_result_search_phrases)
