import pytest
from paper_forms import conf


@pytest.fixture
def paper_conf():
    original = {
        key: getattr(conf, key)
        for key in dir(conf)
        if key.upper()
    }

    yield conf

    for key, value in original.items():
        setattr(conf, key, value)
