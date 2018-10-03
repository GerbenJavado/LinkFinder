#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from linkfinder import regex, parser_file

# Imitate cli_output function
def get_parse(str):
    endpoints = parser_file(str, regex)
    ret = []
    for endpoint in endpoints:
        ret.append(endpoint[1])
    return ret

def test_parser():
    assert get_parse("\"http://example.com\"") == ["http://example.com"]
    assert get_parse("\"smb://example.com\"") == ["smb://example.com"]
    assert get_parse("\"https://www.example.co.us\"") == ["https://www.example.co.us"]

    assert get_parse("\"/path/to/file\"") == ["/path/to/file"]
    assert get_parse("\"../path/to/file\"") == ["../path/to/file"]
    assert get_parse("\"./path/to/file\"") == ["./path/to/file"]
    assert get_parse("\"/wrong/file/test<>b\"") == []

    assert get_parse("\"/api/create.php\"") == ["/api/create.php"]
    assert get_parse("\"/api/create.php?user=test\"") == ["/api/create.php?user=test"]
    assert get_parse("\"/api/create.php?user=test&pass=test\"") == ["/api/create.php?user=test&pass=test"]
    assert get_parse("\"/api/create.php?user=test#home\"") == ["/api/create.php?user=test#home"]

    assert get_parse("\"/path/to/file\"") == ["/path/to/file"]
    assert get_parse("\"../path/to/file\"") == ["../path/to/file"]
    assert get_parse("\"./path/to/file\"") == ["./path/to/file"]
    assert get_parse("\"/wrong/file/test<>b\"") == []

    assert get_parse("\"test_1.json\"") == ["test_1.json"]
    assert get_parse("\"test2.aspx?arg1=tmp1+tmp2&arg2=tmp3\"") == ["test2.aspx?arg1=tmp1+tmp2&arg2=tmp3"]


def test_parser_multi():
    assert set(get_parse("href=\"http://example.com\";href=\"/api/create.php\"")) == set(["http://example.com", "/api/create.php"])
