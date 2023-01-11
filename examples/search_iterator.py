from chatnoir_api.v1 import search, search_phrases

api_key: str = input("API key: ")

results_search = search(api_key, "python library")
top_5_results_search = list(results_search[:5])
print(top_5_results_search)

results_search_phrases = search_phrases(api_key, "python library")
top_5_results_search_phrases = list(results_search_phrases[:5])
print(top_5_results_search_phrases)
