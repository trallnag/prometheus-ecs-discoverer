from prometheus_ecs_discoverer import toolbox


# ==============================================================================
# Misc tests


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


# ------------------------------------------------------------------------------


def test_extract_set():
    dct = {
        "descr1": {"att1": "fefefe", "att2": "fefegtrafgrgr"},
        "descr2": {"att1": "OGOGOGO", "att2": "fefegtrafgrgr"},
        "descr3": {"att1": "OGOGOGO", "att2": "fefegtrafgrgr"},
    }

    extract = toolbox.extract_set(dct, "att1")

    assert len(extract) == 2
    assert extract == {"fefefe", "OGOGOGO"}


# ------------------------------------------------------------------------------


def test_list_to_dict():
    lst = [{"key1": "hallo", "key2": "my"}, {"key1": "old", "key2": "friend"}]

    dct = toolbox.list_to_dict(lst, "key1")

    assert dct == {
        "hallo": {"key1": "hallo", "key2": "my"},
        "old": {"key1": "old", "key2": "friend"},
    }
