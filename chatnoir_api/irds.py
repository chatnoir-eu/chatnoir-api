from ir_datasets.formats import BaseDocs
from ir_datasets.indices.base import Docstore
from chatnoir_api.model import Index
from chatnoir_api.cache import cache_contents
from typing import NamedTuple
import json


class ChatNoirOwiDoc(NamedTuple):
    doc_id: str
    text: str
    url: str
    main_content: str
    title: str
    description: str

    def default_text(self):
        return self.text


class ChatNoirDocsStore(Docstore):
    def __init__(self, index: Index):
        self.index = index
        super().__init__(ChatNoirOwiDoc)

    def get_many_iter(self, doc_ids):
        for doc_id in doc_ids:
            ret = cache_contents(doc_id, self.index, plain=True)
            ret = json.loads(ret)
            fields = ret["original_document"]

            yield ChatNoirOwiDoc(ret["docno"], ret["text"], fields["url"], fields["main_content"], fields["title"], fields["description"])


class ChatNoirDocs(BaseDocs):
    def __init__(self, index: Index):
        self._docs_store = ChatNoirDocsStore(index)

    def docs_store(self):
        return self._docs_store
