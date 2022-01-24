__version__ = "1.0.0"

from chatnoir_api import html, model
from chatnoir_api.model import highlight, result

# Re-export child modules.
Index = model.Index
Slop = model.Slop
Highlight = highlight.Highlight
HighlightedText = highlight.HighlightedText
Result = result.Result
Results = result.Results
ResultsMeta = result.ResultsMeta
SearchResult = result.SearchResult
PhraseSearchResult = result.PhraseSearchResult
MinimalPhraseSearchResult = result.MinimalPhraseSearchResult
html_contents = html.html_contents
