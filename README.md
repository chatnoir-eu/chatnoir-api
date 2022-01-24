[![PyPi](https://img.shields.io/pypi/v/chatnoir-api?style=flat-square)](https://pypi.org/project/chatnoir-api/)
[![CI](https://img.shields.io/github/workflow/status/chatnoir-eu/chatnoir-api/CI?style=flat-square)](https://github.com/chatnoir-eu/chatnoir-api/actions?query=workflow%3A"CI")
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

```python
from chatnoir_api.v1 import search

api_key: str = "<API_KEY>"
results = search(api_key, "python library")

top10_results = results[:10]
print(top10_results)

result_1234 = results[1234]
print(result_1234)
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
