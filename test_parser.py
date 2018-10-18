#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from linkfinder import regex_str, parser_file

# Imitate cli_output function
def get_parse_cli(str):
    endpoints = parser_file(str, regex_str, mode=0)
    ret = []
    for endpoint in endpoints:
        ret.append(endpoint["link"])
    return ret

def test_parser_cli():
    assert get_parse_cli("\"http://example.com\"") == ["http://example.com"]
    assert get_parse_cli("\"smb://example.com\"") == ["smb://example.com"]
    assert get_parse_cli("\"https://www.example.co.us\"") == ["https://www.example.co.us"]

    assert get_parse_cli("\"/path/to/file\"") == ["/path/to/file"]
    assert get_parse_cli("\"../path/to/file\"") == ["../path/to/file"]
    assert get_parse_cli("\"./path/to/file\"") == ["./path/to/file"]
    assert get_parse_cli("\"/wrong/file/test<>b\"") == []

    assert get_parse_cli("\"/api/create.php\"") == ["/api/create.php"]
    assert get_parse_cli("\"/api/create.php?user=test\"") == ["/api/create.php?user=test"]
    assert get_parse_cli("\"/api/create.php?user=test&pass=test\"") == ["/api/create.php?user=test&pass=test"]
    assert get_parse_cli("\"/api/create.php?user=test#home\"") == ["/api/create.php?user=test#home"]

    assert get_parse_cli("\"/path/to/file\"") == ["/path/to/file"]
    assert get_parse_cli("\"../path/to/file\"") == ["../path/to/file"]
    assert get_parse_cli("\"./path/to/file\"") == ["./path/to/file"]
    assert get_parse_cli("\"/wrong/file/test<>b\"") == []

    assert get_parse_cli("\"test_1.json\"") == ["test_1.json"]
    assert get_parse_cli("\"test2.aspx?arg1=tmp1+tmp2&arg2=tmp3\"") == ["test2.aspx?arg1=tmp1+tmp2&arg2=tmp3"]

def test_parser_cli_multi():
    assert set(get_parse_cli("href=\"http://example.com\";href=\"/api/create.php\"")) == set(["http://example.com", "/api/create.php"])

def test_parser_unique():
    '''
    Should return only unique link
    '''
    assert get_parse_cli("href=\"http://example.com\";document.window.location=\"http://example.com\"") == ["http://example.com"]
    assert set(get_parse_cli("href=\"http://example.com\";<img src=\"http://example.com\">;href=\"/api/create.php\"")) == set(["http://example.com", "/api/create.php"])
