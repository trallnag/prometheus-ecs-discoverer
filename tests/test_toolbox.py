import pytest
from prometheus_ecs_discoverer import toolbox


def test_chunk_list_with_even_size():
    big_list = list(range(100))
    chunks = toolbox.chunk_list(big_list, 10)
    assert len(chunks) == 10
    for chunk in chunks:
        assert len(chunk) <= 10


def test_chunk_list_with_uneven_size():
    big_list = list(range(103))
    chunks = toolbox.chunk_list(big_list, 10)
    assert len(chunks) == 11
    for chunk in chunks:
        assert len(chunk) <= 10
    assert len(chunks[-1]) == 3


def test_extract_set():
    dct = {
        "descr1": {"att1": "fefefe", "att2": "fefegtrafgrgr"},
        "descr2": {"att1": "OGOGOGO", "att2": "fefegtrafgrgr"},
        "descr3": {"att1": "OGOGOGO", "att2": "fefegtrafgrgr"},
    }

    extract = toolbox.extract_set(dct, "att1")

    assert len(extract) == 2
    assert extract == {"fefefe", "OGOGOGO"}


def test_list_to_dict():
    lst = [{"key1": "hallo", "key2": "my"}, {"key1": "old", "key2": "friend"}]

    dct = toolbox.list_to_dict(lst, "key1")

    assert dct == {
        "hallo": {"key1": "hallo", "key2": "my"},
        "old": {"key1": "old", "key2": "friend"},
    }


def test_print_structure():
    lst = [{"key1": "hallo", "key2": "my"}, {"key1": "old", "key2": "friend"}]
    toolbox.pstruct(lst)
    assert True


def test_validate_min_len():
    lst = [{"this": "dict", "is": "too long"}, {"good": {"dict": "only", "len": "one"}}]

    with pytest.raises(ValueError):
        toolbox.validate_min_len(min_len=10, collections=lst)

    toolbox.validate_min_len(min_len=1, collections=lst)
    assert True


def test_extract_env_var():
    container = {
        "random": {"random": "random"},
        "environment": [
            {"name": "PROMETHEUS_PORT", "value": "80"},
            {"name": "SOMETINGELSE", "value": "fefefwe"},
        ],
    }

    assert "80" == toolbox.extract_env_var(container, "PROMETHEUS_PORT")
    assert None is toolbox.extract_env_var(container, "does not exist")


def test_extract_env_var_no_environment():
    container = {"random": {"random": "random"}}

    assert None is toolbox.extract_env_var(container, "does not exist")
