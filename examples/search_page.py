from chatnoir_api.v1 import search_page, search_phrases_page

top_5_results_search = search_page("python library", start=0, size=5)
print(top_5_results_search)

top_5_results_search_phrases = search_phrases_page("python library", start=0, size=5)
print(top_5_results_search_phrases)
