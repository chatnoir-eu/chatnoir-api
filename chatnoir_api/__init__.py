__version__ = "0.1.11"

from logging import getLogger

from chatnoir_api import html, model

logger = getLogger("chatnoir-api")

# Re-export child modules.
html_contents = html.html_contents
Index = model.Index
Slop = model.Slop
