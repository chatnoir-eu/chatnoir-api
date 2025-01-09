from chatnoir_api.cache import term_vectors


def test_ms_marco_document_1() -> None:
    contents = term_vectors(
        trec_id="msmarco_doc_16_4126868268",
        index="msmarco-document-v2",
    )

    assert contents is not None
    assert "term_vectors" in contents
    assert "body_lang_en" in contents["term_vectors"]
    assert "terms" in contents["term_vectors"]["body_lang_en"]
    terms = contents["term_vectors"]["body_lang_en"]["terms"]

    assert "hidden" in terms
    assert 25730 == terms["hidden"]["doc_freq"]
    assert 37614 == terms["hidden"]["ttf"]
    assert 1 == terms["hidden"]["term_freq"]


def test_ms_marco_document_2() -> None:
    contents = term_vectors(
        trec_id="msmarco_doc_56_310927995",
        index="msmarco-document-v2",
    )

    assert contents is not None
    assert "term_vectors" in contents
    assert "body_lang_en" in contents["term_vectors"]
    assert "terms" in contents["term_vectors"]["body_lang_en"]
    terms = contents["term_vectors"]["body_lang_en"]["terms"]

    assert "classifier" in terms
    assert 132 == terms["classifier"]["doc_freq"]
    assert 442 == terms["classifier"]["ttf"]
    assert 6 == terms["classifier"]["term_freq"]
