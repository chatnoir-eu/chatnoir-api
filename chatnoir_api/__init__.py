from importlib_metadata import version

__version__ = version("chatnoir-api")

from chatnoir_api import cache, model
from chatnoir_api.model import highlight, result

# Re-export child modules.
Index = model.Index
Slop = model.Slop
ShortUUID = model.ShortUUID
Highlight = highlight.Highlight
HighlightedText = highlight.HighlightedText
MinimalResult = result.MinimalResult
Explanation = result.Explanation
ExplainedMinimalResult = result.ExplainedMinimalResult
Result = result.Result
ExplainedResult = result.ExplainedResult
Meta = result.Meta
Results = result.Results
cache_contents = cache.cache_contents
