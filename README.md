[![PyPi](https://img.shields.io/pypi/v/chatnoir-api?style=flat-square)](https://pypi.org/project/chatnoir-api/)
[![CI](https://img.shields.io/github/actions/workflow/status/chatnoir-eu/chatnoir-api/ci.yml?branch=main&style=flat-square)](https://github.com/chatnoir-eu/chatnoir-api/actions/workflows/ci.yml)
[![Code coverage](https://img.shields.io/codecov/c/github/chatnoir-eu/chatnoir-api?style=flat-square)](https://codecov.io/github/chatnoir-eu/chatnoir-api/)
[![Python](https://img.shields.io/pypi/pyversions/chatnoir-api?style=flat-square)](https://pypi.org/project/chatnoir-api/)
[![Issues](https://img.shields.io/github/issues/chatnoir-eu/chatnoir-api?style=flat-square)](https://github.com/chatnoir-eu/chatnoir-api/issues)
[![Commit activity](https://img.shields.io/github/commit-activity/m/chatnoir-eu/chatnoir-api?style=flat-square)](https://github.com/chatnoir-eu/chatnoir-api/commits)
[![Downloads](https://img.shields.io/pypi/dm/chatnoir-api?style=flat-square)](https://pypi.org/project/chatnoir-api/)
[![License](https://img.shields.io/github/license/chatnoir-eu/chatnoir-api?style=flat-square)](LICENSE)

# 🔍 chatnoir-api

Simple, type-safe access to the [ChatNoir](https://chatnoir.eu/) [search API](https://chatnoir.eu/doc/api/).

## Installation

```shell
pip install chatnoir-api
```

## Usage
The ChatNoir API offers two main features: [search](#search) with BM25F and [retrieving document contents](#retrieve-document-content).

### Search
To search with the ChatNoir API you need to request an [API key](https://chatnoir.eu/apikey/).
Then you can use our Python client to search for documents.
The `results` object is an iterable wrapper of the search results which handles pagination for you.
List-style indexing is supported to access individual results or sub-lists of results:

```python
from chatnoir_api.v1 import search

api_key: str = "<API_KEY>"
results = search(api_key, "python library")

top10_results = results[:10]
print(top10_results)

result_1234 = results[1234]
print(result_1234)
```

#### Search the new ChatNoir
There's a [new](https://chatnoir.web.webis.de/) ChatNoir version with the same API interface. To run your search requests against the new API (e.g., if you want to search the ClueWeb22), set `staging=True` like this:

```python
from chatnoir_api.v1 import search

api_key: str = "<API_KEY>"
results = search(api_key, "python library", staging=True)
```

#### Phrase Search
To search for phrases, use the `search_phrases` method in the same way as normal `search`:

```python
from chatnoir_api.v1 import search_phrases

api_key: str = "<API_KEY>"
results = search_phrases(api_key, "python library", staging=True)
```

### Retrieve Document Content
Often the title and ID of a document is not enough to effectively re-rank a list of search results.
To retrieve the full content or plain text for a given document you can use the `html_contents` helper function.
The `html_contents` function expects a ChatNoir-internal UUID, shorthand UUID, or a TREC ID 
and the index from which to retrieve the document.

#### Retrieve by TREC ID
You can retrieve a document by its TREC ID like this:

```python
from chatnoir_api import cache_contents, Index

contents = cache_contents(
    "clueweb09-en0051-90-00849",
    Index.ClueWeb09,
)
print(contents)

plain_contents = cache_contents(
    "clueweb09-en0051-90-00849",
    Index.ClueWeb09,
    plain=True,
)
print(plain_contents)
```

#### Retrieve by ChatNoir-internal UUID
You can also retrieve a document by its ChatNoir-internal UUID like this:

```python
from uuid import UUID

from chatnoir_api import cache_contents, Index

contents = cache_contents(
    UUID("e635baa8-7341-596a-b3cf-b33c05954361"),
    Index.CommonCrawl1511,
)
print(contents)

plain_contents = cache_contents(
    UUID("e635baa8-7341-596a-b3cf-b33c05954361"),
    Index.CommonCrawl1511,
    plain=True,
)
print(plain_contents)
```

#### Retrieve by ChatNoir-internal short UUID
For newer ChatNoir versions, you can also retrieve a document by its ChatNoir-internal _short_ UUID like this:

```python
from chatnoir_api import cache_contents, Index, ShortUUID

contents = cache_contents(
    ShortUUID("6svePe3PXteDeGPk1XqTLA"),
    Index.ClueWeb22,
    staging=True,
)
print(contents)

plain_contents = cache_contents(
    ShortUUID("6svePe3PXteDeGPk1XqTLA"),
    Index.ClueWeb22,
    plain=True,
    staging=True,
)
print(plain_contents)
```

## Citation

If you use this package, please cite the [paper](https://webis.de/publications.html#bevendorff_2018)
from the [ChatNoir](https://github.com/chatnoir-eu) authors. 
You can use the following BibTeX information for citation:

```bibtex
@InProceedings{bevendorff:2018,
  address =               {Berlin Heidelberg New York},
  author =                {Janek Bevendorff and Benno Stein and Matthias Hagen and Martin Potthast},
  booktitle =             {Advances in Information Retrieval. 40th European Conference on IR Research (ECIR 2018)},
  editor =                {Leif Azzopardi and Allan Hanbury and Gabriella Pasi and Benjamin Piwowarski},
  ids =                   {potthast:2018c,stein:2018c},
  month =                 mar,
  publisher =             {Springer},
  series =                {Lecture Notes in Computer Science},
  site =                  {Grenoble, France},
  title =                 {{Elastic ChatNoir: Search Engine for the ClueWeb and the Common Crawl}},
  year =                  2018
}
```

## Development

To build and develop this package you need to install the `build` package:

```shell
pip install build
```

### Installation

Install package dependencies:

```shell
pip install -e .
```

### Testing

Install test dependencies:

```shell
pip install -e .[test]
```

Verify your changes against the test suite to verify.

```shell
flake8 chatnoir_api examples
pylint -E chatnoir_api examples
CHATNOIR_API_KEY="<API_KEY>" pytest chatnoir_api examples
```

Please also add tests for your newly developed code.

### Build wheels

Wheels for this package can be built by:

```shell
python -m build
```

## License

This repository is released under the [MIT license](LICENSE).
