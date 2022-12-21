from uuid import UUID

from pytest import fixture

from chatnoir_api.model import ShortUUID


@fixture
def short_uuid() -> ShortUUID:
    return ShortUUID("6svePe3PXteDeGPk1XqTLA")


@fixture
def uuid() -> UUID:
    return UUID("eacbde3d-edcf-5ed7-8378-63e4d57a932c")


def test_document_id(short_uuid, uuid: UUID):
    assert short_uuid == uuid
