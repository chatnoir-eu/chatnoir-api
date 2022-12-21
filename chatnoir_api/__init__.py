__version__ = "1.0.0"

from chatnoir_api import cache, model
from chatnoir_api.model import highlight, result

# Re-export child modules.
Index = model.Index
Slop = model.Slop
ShortUUID = model.ShortUUID
Highlight = highlight.Highlight
HighlightedText = highlight.HighlightedText
Result = result.Result
Results = result.Results
ResultsMeta = result.ResultsMeta
SearchResult = result.SearchResult
PhraseSearchResult = result.PhraseSearchResult
MinimalPhraseSearchResult = result.MinimalPhraseSearchResult
cache_contents = cache.cache_contents
