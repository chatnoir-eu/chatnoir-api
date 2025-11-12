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


class ChatNoirDocsStore():
    def __init__(self, index: Index):
        self._index = index
        self._doc_cls = ChatNoirOwiDoc
        self._id_field = "doc_id"
        self._id_field_idx = self._doc_cls._fields.index(self._id_field)

    def get(self, doc_id, field=None):
        result = self.get_many([doc_id], field)
        if result:
            return result[doc_id]
        raise KeyError(f'doc_id={doc_id} not found')

    def get_many(self, doc_ids, field=None):
        result = {}
        field_idx = self._doc_cls._fields.index(field) if field is not None else None
        for doc in self.get_many_iter(doc_ids):
            if field is not None:
                result[getattr(doc, self._id_field)] = doc[field_idx]
            else:
                result[getattr(doc, self._id_field)] = doc
        return result

    def get_many_iter(self, doc_ids):
        for doc_id in doc_ids:
            ret = cache_contents(doc_id, self._index, plain=True)
            ret = json.loads(ret)
            fields = ret["original_document"]

            yield ChatNoirOwiDoc(ret["docno"], ret["text"], fields["url"], fields["main_content"], fields["title"], fields["description"])

