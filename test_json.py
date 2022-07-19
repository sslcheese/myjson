#!/usr/bin/env python
# coding=utf-8

import pytest
import unittest
import sys
import os

sys.path.append(os.pardir)

from myjson.json import JsonE, json_free, json_save, json_num, json_bool, json_str, json_type
from myjson.json import json_new, json_new_bool, json_new_num, json_new_str
from myjson.json import json_add_member, json_add_element
from myjson.json import json_get_member, json_get_element
from myjson.json import json_obj_get_bool, json_obj_get_num, json_obj_get_str
from myjson.json import json_obj_set_bool, json_obj_set_num, json_obj_set_str
from myjson.json import json_arr_count
from myjson.json import json_arr_get_num, json_arr_get_bol, json_arr_get_str
from myjson.json import json_arr_add_bool, json_arr_add_num, json_arr_add_str


class TestMyJsonMethods(unittest.TestCase):
    # 完成使用场景的测试
    def test_scene(self):
        # 验证json_new功能
        json = json_new(JsonE.JSON_OBJ)
        assert json is not None
        basic = json_new(JsonE.JSON_OBJ)
        assert basic is not None

        """
        json_add_member
        json_obj_get_bool
        json_obj_get_num
        json_obj_get_str
        """
        assert json_add_member(json, "basic", basic) is not None
        assert json_add_member(basic, "enable", json_new_bool(True)) is not None
        assert json_obj_get_bool(basic, "enable") is True
        assert json_add_member(basic, "port", json_new_num(389)) is not None
        assert json_obj_get_num(basic, "port", 0) == 389
        assert json_add_member(basic, "ip", json_new_str("200.200.3.61")) is not None
        ip = json_obj_get_str(basic, "ip", None)
        assert ip == "200.200.3.61"

        dns = json_new(JsonE.JSON_ARR)

        assert json_add_member(basic, "dns", dns) is not None
        assert json_add_element(dns, json_new_str("200.200.0.1")) is not None
        assert json_arr_add_str(dns, "200.0.0.254") is not None
        assert json_arr_get_str(dns, 0) == "200.200.0.1"
        assert json_arr_get_str(dns, 1) == "200.0.0.254"

        assert json_num(json_get_member(basic, "port")) == 389
        assert json_bool(json_get_member(basic, "enable")) is True
        assert json_str(json_get_member(basic, "ip")) == "200.200.3.61"

        advance = json_new(JsonE.JSON_OBJ)
        portpool = json_new(JsonE.JSON_ARR)
        json_add_member(json, "advance", advance)
        json_add_member(advance, "portpool", portpool)

        assert json_arr_add_num(portpool, 130) == 130
        assert json_arr_add_num(portpool, 131) == 131
        assert json_arr_add_num(portpool, 132) == 132

        """
        json_obj_set_num
        json_obj_set_bool
        json_obj_set_str
        """
        assert json_obj_set_num(basic, "timeout", 10) == 10
        assert json_obj_set_str(basic, "basedn", "aaa") == "aaa"
        assert json_obj_set_bool(basic, "enable", False) == False

        """
        json_arr_count
        json_arr_get_num
        json_arr_get_bool
        json_arr_add_num
        json_arr_add_bool
        """
        assert json_arr_count(portpool) == 3
        assert json_arr_add_num(portpool, 133)
        assert json_arr_count(portpool) == 4

        assert json_arr_get_num(portpool, 0) == 130

        bool_list = json_new(JsonE.JSON_ARR)
        assert json_arr_add_bool(bool_list, True) is True
        assert json_arr_add_bool(bool_list, False) is False
        assert json_arr_add_bool(bool_list, True) is True
        assert json_arr_get_bol(bool_list, 0) is True
        assert json_arr_get_bol(bool_list, 1) is False
        assert json_arr_get_bol(bool_list, 2) is True

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

    def test_json_save(self):
        json = json_new(JsonE.JSON_OBJ)
        basic = json_new(JsonE.JSON_OBJ)

        json_add_member(json, "basic", basic)
        json_add_member(basic, "enable", json_new_bool(True))
        json_add_member(basic, "port", json_new_num(389))
        json_add_member(basic, "timeout", json_new_num(10))
        json_add_member(basic, "basedn", json_new_str("aaa"))
        json_add_member(basic, "fd", json_new_num(-1))
        json_add_member(basic, "maxcnt", json_new_num(133333333333))

        dns = json_new(JsonE.JSON_ARR)
        json_add_element(dns, json_new_str("200.200.0.1"))
        json_add_element(dns, json_new_str("200.0.0.254"))
        json_add_member(basic, "dns", dns)

        advance = json_new(JsonE.JSON_OBJ)
        dns = json_new(JsonE.JSON_ARR)
        tmp = json_new(JsonE.JSON_OBJ)
        json_add_member(tmp, "name", json_new_str("huanan"))
        json_add_member(tmp, "ip", json_new_str("200.200.0.1"))
        json_add_element(dns, tmp)

        tmp = json_new(JsonE.JSON_OBJ)
        json_add_member(tmp, "name", json_new_str("huabei"))
        json_add_member(tmp, "ip", json_new_str("200.0.0.254"))
        json_add_element(dns, tmp)

        protpool = json_new(JsonE.JSON_ARR)
        json_add_element(protpool, json_new_num(130))
        json_add_element(protpool, json_new_num(131))
        json_add_element(protpool, json_new_num(132))
        json_add_member(advance, "dns", dns)
        json_add_member(advance, "protpool", protpool)
        json_add_member(advance, "url", json_new_str("http://200.200.0.4/main"))
        json_add_member(advance, "path", json_new_str("/etc/sinfors"))
        json_add_member(advance, "value", json_new_num(3.14))
        json_add_member(json, "advance", advance)

        assert 1 == json_save(json, "./test.yml")

    def test_json_type(self):
        json = json_new(JsonE.JSON_OBJ)
        assert json_type(json) == JsonE.JSON_OBJ
        assert json_type(json_new_num(5)) == JsonE.JSON_NUM
        assert json_type(json_new_bool(True)) == JsonE.JSON_BOL
        assert json_type(json_new_str("111")) == JsonE.JSON_STR
        assert json_type(json_new(JsonE.JSON_ARR)) == JsonE.JSON_ARR

    # 测试对JSON对象使用print或str方法时的输出状况 __str__
    def test_json_print(self):
        json = json_new(JsonE.JSON_OBJ)
        assert str(json) == "{}"
        basic = json_new(JsonE.JSON_OBJ)
        dns = json_new(JsonE.JSON_ARR)
        assert str(dns) == "[]"

        json_add_member(json, "basic", basic)
        assert str(json) == '{"basic": {}}'
        json_add_member(json, "dns", dns)
        assert str(json) == '{"basic": {},"dns": []}'

        json_add_element(dns, json_new_str("200.200.2.254"))
        json_add_element(dns, json_new_str("192.168.1.1"))
        assert str(json) == '{"basic": {},"dns": ["200.200.2.254","192.168.1.1"]}'
        json_add_member(basic, "enable", json_new_bool(True))
        assert str(json) == '{"basic": {"enable": True},"dns": ["200.200.2.254","192.168.1.1"]}'
        json_add_member(basic, "fd", json_new_num(-1))
        assert str(json) == '{"basic": {"enable": True,"fd": -1},"dns": ["200.200.2.254","192.168.1.1"]}'

        json_free(json)
        basic = json_get_member(json, "basic")  # basic对应的对象
        dns = json_get_member(json, "dns")  # dns对应的数组：["200.200.0.1","200.0.0.254"]
        ip0 = json_get_element(dns, 0)  # 数组中第0个IP地址："200.200.0.1"
        assert str(basic.val) == '{"enable": True,"fd": -1}'
        assert str(ip0) == '"200.200.2.254"'

    # 测试json_num json_bool json_str 的异常情况
    def test_json_num_bool_str(self):
        test_num = json_new_num(1)
        test_bool = json_new_bool(True)
        test_str = json_new_str("aaa")

        assert json_num(test_bool, 5) == 5
        assert json_bool(test_str, True) is True
        assert json_str(test_num, "bbb") == "bbb"

    def test_json_get_element_error(self):
        test_num = json_new_num(5)
        with pytest.raises(TypeError) as exc_info:
            json_get_element(test_num, 0)
        assert exc_info.type is TypeError

        test_arr = json_new(JsonE.JSON_ARR)
        json_add_element(test_arr, json_new_num(5))
        json_add_element(test_arr, json_new_num(6))
        json_add_element(test_arr, json_new_num(7))
        with pytest.raises(ValueError) as exc_info:
            json_get_element(test_arr, 99)
        assert exc_info.type is ValueError

        test_arr.arr.elems = None
        with pytest.raises(ValueError) as exc_info:
            json_get_element(test_arr, 1)
        assert exc_info.type is ValueError

    def test_is_key_legal(self):
        json = json_new(JsonE.JSON_OBJ)
        assert json_add_member(json, "0004444", json_new_num(66)) is None

    def test_json_add_member_error(self):
        test_num = json_new_num(1)
        test_bool = json_new_bool(True)
        test_str = json_new_str("aaa")
        test_json = json_new(JsonE.JSON_OBJ)

        # 验证json为None的情况
        with pytest.raises(ValueError) as exc_info:
            json_add_member(None, "11", test_num)
        assert exc_info.type is ValueError

        # 验证json类型错误的情况
        with pytest.raises(TypeError) as exc_info:
            json_add_member(test_bool, "11", test_num)
        assert exc_info.type is TypeError

        # 验证val类型错误的情况
        with pytest.raises(TypeError) as exc_info:
            json_add_member(test_json, "11", "abc")
        assert exc_info.type is TypeError

        # 验证json对象丢失的情况
        json_add_member(test_json, "num", test_num)
        test_json.obj.kvs = None
        with pytest.raises(ValueError) as exc_info:
            json_add_member(test_json, "11", test_str)
        assert exc_info.type is ValueError

    def test_json_add_element_error(self):
        test_arr = json_new(JsonE.JSON_ARR)
        test_json = json_new(JsonE.JSON_OBJ)

        # 验证Json为None 或 Json类型错误的情况
        with pytest.raises(ValueError) as exc_info:
            json_add_element(None, json_new_num(1))
        assert exc_info.type is ValueError

        with pytest.raises(ValueError) as exc_info:
            json_add_element(test_json, json_new_num(1))
        assert exc_info.type is ValueError

        # 验证array数组丢失的情况
        json_add_element(test_arr, json_new_num(1))
        test_arr.arr.elems = None
        with pytest.raises(ValueError) as exc_info:
            json_add_element(test_arr, json_new_num(1))
        assert exc_info.type is ValueError




if __name__ == '__main__':
    # unittest.main()
    pytest.main("-vs --cov=../myjson/ --cov-report=html   --html=htmlcov/report.html test_json.py")
