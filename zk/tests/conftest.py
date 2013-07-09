import pytest

@pytest.fixture()
def sqlite(monkeypatch):
    from factories import session
    from zk.model import meta
    monkeypatch.setattr(meta, 'Session', session)
