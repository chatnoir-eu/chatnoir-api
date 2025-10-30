[![PyPi](https://img.shields.io/pypi/v/chatnoir-api?style=flat-square)](https://pypi.org/project/chatnoir-api/)
[![CI](https://img.shields.io/github/actions/workflow/status/chatnoir-eu/chatnoir-api/ci.yml?branch=main&style=flat-square)](https://github.com/chatnoir-eu/chatnoir-api/actions/workflows/ci.yml)
[![Code coverage](https://img.shields.io/codecov/c/github/chatnoir-eu/chatnoir-api?style=flat-square)](https://codecov.io/github/chatnoir-eu/chatnoir-api/)
[![Python](https://img.shields.io/pypi/pyversions/chatnoir-api?style=flat-square)](https://pypi.org/project/chatnoir-api/)
[![Issues](https://img.shields.io/github/issues/chatnoir-eu/chatnoir-api?style=flat-square)](https://github.com/chatnoir-eu/chatnoir-api/issues)
[![Commit activity](https://img.shields.io/github/commit-activity/m/chatnoir-eu/chatnoir-api?style=flat-square)](https://github.com/chatnoir-eu/chatnoir-api/commits)
[![Downloads](https://img.shields.io/pypi/dm/chatnoir-api?style=flat-square)](https://pypi.org/project/chatnoir-api/)
[![License](https://img.shields.io/github/license/chatnoir-eu/chatnoir-api?style=flat-square)](LICENSE)

# ![🔍](https://www.chatnoir.eu/static/ui/img/chatnoir-icon%4032x32.png) chatnoir-api

Simple, type-safe access to the [ChatNoir](https://www.chatnoir.eu/) [search API](https://www.chatnoir.eu/api/v1/).

Working with PyTerrier? Check out the [`chatnoir-pyterrier`](https://pypi.org/project/chatnoir-pyterrier/) package.

## Installation

Install the package from PyPI:

```shell
pip install chatnoir-api
```

## Usage

The ChatNoir API offers two main features: [search](#search) with BM25F and [retrieving document contents](#retrieve-document-contents).

### Search

You can use our Python client to search for documents.
The `results` object is an iterable wrapper of the search results which handles pagination for you.
List-style indexing is supported to access individual results or sub-lists of results:

```python
from chatnoir_api.v1 import search

results = search("python library", api_key="<YOUR_API_KEY>")

top10_results = results[:10]
print(top10_results)

result_1234 = results[1234]
print(result_1234)
```

#### Search a specific index

To limit your search requests to a single index (e.g., ClueWeb22 category B), set the `index` parameter like this:

```python
from chatnoir_api.v1 import search

results = search("python library", index="clueweb22/b", api_key="<YOUR_API_KEY>")
```

#### Phrase search

To search for phrases, use the `search_phrases` method in the same way as normal `search`:

```python
from chatnoir_api.v1 import search_phrases

results = search_phrases("python library")
```

#### API key

The public, shared, default API key comes with a limited request budget.
To use the ChatNoir API more extensively, please request a dedicated [API key](https://chatnoir.web.webis.de/apikey/).

Then, use the `api_key` parameter to add it to your requests like this:

```python
results = search("python library", api_key="<YOUR_API_KEY>")
```

### Retrieve document contents

Often the title and ID of a document is not enough to effectively re-rank a list of search results.
To retrieve the full content or plain text for a given document you can use the `html_contents` helper function.
The `html_contents` function expects a ChatNoir-internal UUID, shorthand UUID, or a TREC ID and the index from which to retrieve the document.

#### Retrieve by TREC ID

You can retrieve a document by its TREC ID like this:

```python
from chatnoir_api import cache_contents, Index

contents = cache_contents(
    "clueweb09-en0051-90-00849",
    index="clueweb09",
)
print(contents)

plain_contents = cache_contents(
    "clueweb09-en0051-90-00849",
    index="clueweb09",
    plain=True,
)
print(plain_contents)
```

#### Retrieve by ChatNoir-internal short UUID

For newer ChatNoir versions, you can also retrieve a document by its ChatNoir-internal _short_ UUID like this:

```python
from chatnoir_api import cache_contents, Index, ShortUUID

contents = cache_contents(
    ShortUUID("MzOlTIayX9ub7c13GLPr_g"),
    index="clueweb22/b",
)
print(contents)

plain_contents = cache_contents(
    ShortUUID("MzOlTIayX9ub7c13GLPr_g"),
    index="clueweb22/b",
    plain=True,
)
print(plain_contents)
```

## Indexing

Head over to the [ChatNoir `ir_datasets` indexer](https://github.com/chatnoir-eu/chatnoir-ir-datasets-indexer) to learn more on how new `ir_datasets`-compatible datasets are indexed into ChatNoir.

## Citation

If you use this package, please cite the [paper](https://webis.de/publications.html#bevendorff_2018)
from the [ChatNoir](https://github.com/chatnoir-eu) authors. 
You can use the following BibTeX information for citation:

```bibtex
@InProceedings{bevendorff:2018,
  address =   {Berlin Heidelberg New York},
  author =    {Janek Bevendorff and Benno Stein and Matthias Hagen and Martin Potthast},
  booktitle = {Advances in Information Retrieval. 40th European Conference on IR Research (ECIR 2018)},
  editor =    {Leif Azzopardi and Allan Hanbury and Gabriella Pasi and Benjamin Piwowarski},
  month =     mar,
  publisher = {Springer},
  series =    {Lecture Notes in Computer Science},
  site =      {Grenoble, France},
  title =     {{Elastic ChatNoir: Search Engine for the ClueWeb and the Common Crawl}},
  year =      2018
}
@InProceedings{merker:2025a,
  address =   {Cham, Switzerland},
  author =    {Jan Heinrich Merker and Janek Bevendorff and Maik Fr{\"o}be and Tim Hagen and Harrisen Scells and Matti Wiegmann and Benno Stein and Matthias Hagen and  Martin Potthast},
  booktitle = {Advances in Information Retrieval. 47th European Conference on IR Research (ECIR 2025)},
  doi =       {10.1007/978-3-031-88720-8_17},
  editor =    {Claudia Hauff and Craig Macdonal and Dietmar Jannach and Gabriella Kazai and Franco Maria Nardini and Fabio Pinelli and Fabrizio Silvestri and Nicola Tonellotto},
  month =     apr,
  pages =     {96--104},
  publisher = {Springer Nature},
  series =    {Lecture Notes in Computer Science},
  site =      {Lucca, Italy},
  title =     {{Web-scale Retrieval Experimentation with chatnoir-pyterrier}},
  volume =    15576,
  year =      2025
}
```

## Development

To build this package and contribute to its development you need to install the `build`, and `setuptools` and `wheel` packages:

```shell
pip install build setuptools wheel
```

(On most systems, these packages are already pre-installed.)

### Developer installation

Install package and test dependencies:

```shell
pip install -e .[tests]
```

### Testing

Configure the API keys for testing:

```shell
export CHATNOIR_API_KEY="<API_KEY>"
export CHATNOIR_API_KEY_CHAT="<API_KEY>"
```

Verify your changes against the test suite to verify.

```shell
ruff check .                   # Code format and LINT
mypy .                         # Static typing
bandit -c pyproject.toml -r .  # Security
pytest .                       # Unit tests
```

Please also add tests for your newly developed code.

### Build wheels

Wheels for this package can be built with:

```shell
python -m build
```

## Support

If you hit any problems using this package, please file an [issue](https://github.com/chatnoir-eu/chatnoir-api/issues/new).
We're happy to help!

## License

This repository is released under the [MIT license](LICENSE).
