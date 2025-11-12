import unittest
from chatnoir_api.irds import ChatNoirDocs


class TestIrDatasets(unittest.TestCase):
    def test_owi_2025(self):
        docs = ChatNoirDocs("wows-owi/2025")
        docs_store = docs.docs_store()
        self.assertIsNotNone(docs_store)

        actual_doc = docs_store.get("7ad51188193e0e9453857aae906da17a929c2c1d339f056e0e8c37a92f7d4d42")
        self.assertIsNotNone(actual_doc)
        self.assertEqual("about Vim : vim online", actual_doc.title)
        self.assertIn("about Vim : vim online", actual_doc.default_text())
        self.assertEqual("https://www.vim.org/about.php", actual_doc.url)
