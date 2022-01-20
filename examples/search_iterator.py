from itertools import islice

from chatnoir_api.v1 import search, search_phrases

api_key: str = input("API key: ")

results_search = search(
    api_key, "python library"
)
top_5_results_search = list(islice(results_search, 5))
print(top_5_results_search)

results_search_phrases = search_phrases(
    api_key, "python library",
    minimal=False
)
top_5_results_search_phrases = list(islice(results_search_phrases, 5))
print(top_5_results_search_phrases)

results_search_phrases_minimal = search_phrases(
    api_key, "python library",
    minimal=True
)
top_5_results_search_phrases_minimal = list(islice(
    results_search_phrases_minimal, 5
))
print(top_5_results_search_phrases_minimal)
