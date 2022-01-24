from chatnoir_api.v1 import (
    search as search_requests, search_phrases as search_phrases_requests
)

# Re-export child modules.
search = search_requests.search
search_page = search_requests.search_page
search_phrases = search_phrases_requests.search_phrases
search_phrases_page = search_phrases_requests.search_phrases_page
