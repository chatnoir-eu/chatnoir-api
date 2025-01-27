from chatnoir_api.v1 import search, search_phrases

query: str = input("Query: ")

print("Search results:")
print()
results_search = search(query)
for i, result in enumerate(results_search[:10]):
    print(i + 1, result.title.text[:50], result.score, result.target_uri)
    print("\t", result.snippet.text[:200])
    print()

print("Phrases results:")
print()
results_search = search_phrases(query, minimal=False)
for i, result in enumerate(results_search[:10]):
    print(i + 1, result.title.text[:50], result.score, result.target_uri)
    print("\t", result.snippet.text[:200])
    print()
