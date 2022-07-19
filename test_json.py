#!/usr/bin/env python
# coding=utf-8

import pytest
import unittest
import sys
import os

sys.path.append(os.pardir)

from myjson.json import JsonE, json_free, json_save
from myjson.json import json_new, json_new_bool, json_new_num, json_new_str
from myjson.json import json_add_member, json_add_element
from myjson.json import json_obj_get_bool, json_obj_get_num, json_obj_get_str
from myjson.json import json_arr_count
from myjson.json import json_arr_get_num, json_arr_get_bol, json_arr_get_str
from myjson.json import json_arr_add_bool, json_arr_add_num, json_arr_add_str


class TestMyJsonMethods(unittest.TestCase):
    # 完成使用场景的测试
    def test_scene(self):
        json = json_new(JsonE.JSON_OBJ)
        assert json is not None
        basic = json_new(JsonE.JSON_OBJ)
        assert basic is not None

        assert json_add_member(json, "basic", basic) is not None

        assert json_add_member(basic, "enable", json_new_bool(True)) is not None
        assert json_obj_get_bool(basic, "enable") is True

        assert json_add_member(basic, "port", json_new_num(389)) is not None
        assert json_obj_get_num(basic, "port", 0) == 389

        assert json_add_member(basic, "ip", json_new_str("200.200.3.61")) is not None
        ip = json_obj_get_str(basic, "ip", None)
        assert ip == "200.200.3.61"

        dns = json_new(JsonE.JSON_ARR)
        assert dns is not None
        assert json_add_element(dns, json_new_str("200.200.0.1")) is not None
        assert json_add_element(dns, json_new_str("200.0.0.254")) is not None
        assert json_add_member(basic, "dns", dns) is not None
        assert json_arr_get_str(dns, 0) == "200.200.0.1"
        assert json_arr_get_str(dns, 1) == "200.0.0.254"
        assert json_


        json_free(json)

    # 测试键值对存在的情况
    def test_json_obj_get_str_exist(self):
        json = json_new(JsonE.JSON_OBJ)
        self.assertTrue(json is not None)

        self.assertTrue(json_add_member(json, "ip", json_new_str("200.200.3.61")) is not None)
        ip = json_obj_get_str(json, "ip", None)
        self.assertTrue(ip is not None)
        self.assertMultiLineEqual("200.200.3.61", ip)

        json_free(json)

    # 测试键值对不存在的情况
    def test_json_obj_get_str_notexist(self):
        json = json_new(JsonE.JSON_OBJ)
        self.assertTrue(json is not None)

        self.assertTrue(json_add_member(json, "ip", json_new_str("200.200.3.61")) is not None)
        ip = json_obj_get_str(json, "ip2", None)
        self.assertTrue(ip is None)

        ip = json_obj_get_str(json, "ip3", "default")
        self.assertTrue(ip is not None)
        self.assertMultiLineEqual("default", ip)

        json_free(json)

    def test_json_save_str(self):
        expect = "hello world"
        json = json_new_str("hello world")
        self.assertEqual(0, json_save(json, "unitest.yml"))

        with open("unitest.yml", "r") as f:
            string = f.readline().strip()
        self.assertMultiLineEqual(expect, string)
        json_free(json)


if __name__ == '__main__':
    # unittest.main()
    pytest.main("-vs --cov=../myjson/ --cov-report=html   --html=htmlcov/report.html test_json.py")
