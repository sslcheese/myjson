#!/usr/bin/env python
# coding=utf-8


from myjson.json import *

def main():

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

    print(json)
    json_save(json, "./test.yml")

if __name__ == '__main__':
    main()
