__version__ = "2.0.0"

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
MinimalResultStaging = result.MinimalResultStaging
ExplainedMinimalResultStaging = result.ExplainedMinimalResultStaging
ResultStaging = result.ResultStaging
ExplainedResultStaging = result.ExplainedResultStaging
Meta = result.Meta
MetaIndex = result.MetaIndex
ExtendedMeta = result.ExtendedMeta
Results = result.Results
cache_contents = cache.cache_contents
