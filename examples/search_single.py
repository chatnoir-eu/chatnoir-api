from chatnoir_api.v1 import search, search_phrases

top_result_search = next(iter(search("python library")))
print(top_result_search)

top_result_search_phrases = next(iter(search_phrases("python library")))
print(top_result_search_phrases)
