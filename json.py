#!/usr/bin/env python
# coding=utf-8
import logging
import re
from enum import Enum



class JsonE(Enum):
    JSON_NONE = 0
    JSON_BOL = 1  # BOOL类型
    JSON_NUM = 2  # 数值类型
    JSON_STR = 3  # 字符串类型
    JSON_ARR = 4  # 数组类型
    JSON_OBJ = 5  # 对象类型


class Array:
    def __init__(self):
        self.elems = []
        self.count = 0

    def __str__(self):
        res = "["
        for e in self.elems:
            res += str(e) + ","
        res = res.rstrip(",")
        res += "]"
        return res


class Keyvalue:
    def __init__(self, key, val):
        self.key: str = key
        self.val: JSON = val

    def __str__(self):
        res = "".join(('"', self.key, '": ', str(self.val)))
        return res


class Obj:
    def __init__(self):
        self.kvs = []
        self.count = 0

    def __str__(self):
        res = "{"
        for kv in self.kvs:
            res = "".join((res, str(kv)))
            res += ","
        res = res.rstrip(",")
        res += "}"
        return res


class Value:
    def __init__(self, j_type):
        self.j_type: JsonE = j_type

    def __str__(self):
        res = ""
        if self.j_type == JsonE.JSON_NUM:
            res = str(self.num)
        elif self.j_type == JsonE.JSON_BOL:
            res = str(self.bol)
        elif self.j_type == JsonE.JSON_STR:
            res = '"' + self.str + '"'
        elif self.j_type == JsonE.JSON_ARR:
            res = str(self.arr)
        elif self.j_type == JsonE.JSON_OBJ:
            res = str(self.obj)
        return res


class JSON:
    def __init__(self):
        self.j_type: JsonE
        self.val: Value

    def __str__(self):
        return str(self.val)

    @property
    def num(self):
        return self.val.num

    @num.setter
    def num(self, val):
        self.val.num = val

    @property
    def bol(self):
        return self.val.bol

    @bol.setter
    def bol(self, val):
        self.val.bol = val

    @property
    def str(self):
        return self.val.str

    @str.setter
    def str(self, val):
        self.val.str = val

    @property
    def arr(self):
        return self.val.arr

    @property
    def obj(self):
        return self.val.obj


def json_new(j_type: JsonE) -> JSON:
    json = JSON()
    if not json:
        return
    json.j_type = j_type
    json.val = Value(j_type)
    if j_type == JsonE.JSON_NUM:
        json.val.num = 0
    elif j_type == JsonE.JSON_BOL:
        json.val.bol = False
    elif j_type == JsonE.JSON_STR:
        json.val.str = ""
    elif j_type == JsonE.JSON_ARR:
        json.val.arr = Array()
    elif j_type == JsonE.JSON_OBJ:
        json.val.obj = Obj()
    return json


def json_type(json: JSON) -> JsonE:
    assert json
    return json.j_type if json else JsonE.JSON_NONE


def json_free(json: JSON) -> None:
    if json.j_type == JsonE.JSON_ARR:
        for a in json.arr.elems:
            json_free(a)
    elif json.j_type == JsonE.JSON_OBJ:
        for kv in json.obj.kvs:
            json_free(kv.val)
    del json


def json_write(j: JSON, level: int, f):
    '''
    用于json_save函数，对已经打开的文件进行递归写入
    :param j: 将写入的JSON对象
    :param level: 当前的层级，用于计算缩进
    :param f:以及打开的文件对象
    :return:
    '''
    tab = 2
    if j.j_type == JsonE.JSON_NUM:
        # f.write(" "*level*tab)
        f.write(str(j.num) + "\n")
    elif j.j_type == JsonE.JSON_BOL:
        # f.write(" "*level*tab)
        f.write(str(j.bol) + "\n")
    elif j.j_type == JsonE.JSON_STR:
        # f.write(" "*level*tab)
        f.write(j.str + "\n")
    elif j.j_type == JsonE.JSON_ARR:
        for a in j.arr.elems:
            f.write(" " * level * tab + "- ")
            if a.val.j_type == JsonE.JSON_OBJ or a.val.j_type == JsonE.JSON_ARR:
                f.write("\n")
            json_write(a, level + 1, f)
    elif j.j_type == JsonE.JSON_OBJ:
        for kv in j.obj.kvs:
            f.write(" " * level * tab + str(kv.key) + ": ")
            if kv.val.j_type == JsonE.JSON_OBJ or kv.val.j_type == JsonE.JSON_ARR:
                f.write("\n")
            json_write(kv.val, level + 1, f)


def json_save(json: JSON, fname: str) -> int:
    with open(fname, "w+", newline="") as f:
        json_write(json, 0, f)
    return 1


def json_num(json: JSON, default: float=0.0) -> float:
    """
    获取JSON_NUM类型JSON值的数值
    :param json:数值类型的JSON值
    :param default:类型不匹配时返回的缺省值
    :return:double 如果json是合法的JSON_NUM类型，返回其数值，否则返回缺省值def
    """
    if json and  json.j_type == JsonE.JSON_NUM:
        res = json.num
    else:
        res = default
    return res


def json_bool(json: JSON, default: bool=False) -> bool:
    """
    获取JSON_BOOL类型JSON值的布尔值
    :param json:布尔值类型的JSON值
    :param default:
    :return:如果json是合法的JSON_BOL类型，返回其数值，否则返回FALSE
    """
    if json and  json.j_type == JsonE.JSON_BOL:
        res = json.bol
    else:
        res = default
    return res


def json_str(json: JSON, default: str="") -> str:
    if json and  json.j_type == JsonE.JSON_STR:
        res = json.str
    else:
        res = default
    return res


def json_new_num(val: float) -> JSON:
    json = json_new(JsonE.JSON_NUM)
    json.num = val
    return json


def json_new_bool(val: bool) -> JSON:
    json = json_new(JsonE.JSON_BOL)
    json.bol = val
    return json


def json_new_str(val: str) -> JSON:
    assert val
    json = json_new(JsonE.JSON_STR)
    json.str = val
    return json


def json_get_member(json: JSON, key: str) -> JSON:
    '''
    从对象类型的JSON值中获取名字为key的成员(JSON值)
    :param json:对象类型的JSON值
    :param key:成员的键名
    :return:找到的成员
    '''
    assert json
    assert json.j_type == JsonE.JSON_OBJ
    assert not (json.obj.count > 0 and json.obj.kvs is None)
    assert key

    for i in range(json.obj.count):
        if json.obj.kvs[i].key == key:
            return json.obj.kvs[i].val
    return None


def json_get_element(json: JSON, idx: int) -> JSON:
    if not (json and json.j_type == JsonE.JSON_ARR):
        raise TypeError
    if json.arr.count > 0 and json.arr.elems is None:
        raise ValueError

    if isinstance(idx, int) and json.arr.count > idx >= 0:
        return json.arr.elems[idx]
    else:
        raise ValueError("idx不合法")


def is_key_legal(key: str):
    # 正则检查key是否合法
    try:
        k = re.findall("[a-zA-Z][a-zA-Z0-9_]*", key)[0]
        if key == k:
            return True
    except IndexError as e:
        return False


def json_add_member(json: JSON, key: str, val: JSON) -> JSON:
    '''
     @brief 往对象类型的json中增加一个键值对，键名为key，值为val
 *
 * @param json JSON对象
 * @param key 键名，符合正则：[a-zA-Z_][a-zA-Z_-0-9]*
 * @param val 键值，必须是堆分配拥有所有权的JSON值
 * @return JSON* 成功返回val，失败返回NULL
 * @details
 *  json_add_member会转移val的所有权，所以调用json_add_member之后不用考虑释放val的问题
 * 因为需要支持如下写法：
 *  json_add_member(json, "port", json_new_num(80));
 * 所以需要做到：
 *  1) 允许val为NULL；
 *  2) 当json_add_member内部发生失败时，需要释放val，满足将val的所有权转让给json_add_member的语义设定
 */
    '''
    if not json:
        raise ValueError
    if json.j_type is not JsonE.JSON_OBJ:
        raise TypeError("json类型错误")
    if not isinstance(val, JSON):
        raise TypeError("val类型错误")
    if json.obj.count > 0 and json.obj.kvs is None:
        raise ValueError

    # 想想: 为啥不用assert检查val？
    # 想想：如果json中已经存在名字为key的成员，怎么办？
    # 正则检查key是否合法
    if not is_key_legal(key):
        return None

    for kv in json.obj.kvs:
        if kv.key == key:
            kv.value = val
            return val
    new_kv = Keyvalue(key, val)
    json.obj.kvs.append(new_kv)
    json.obj.count += 1

    return val


def json_add_element(json: JSON, val: JSON) -> JSON:
    '''
    /**
 * @brief 往数组类型的json中追加一个元素
 *
 * @param json JSON数组
 * @param val 加入到数组的元素，必须是堆分配拥有所有权的JSON值
 * @details
 *  json_add_element会转移val的所有权，所以调用json_add_element之后不用考虑释放val的问题
 */
    '''
    if not (json and json.j_type == JsonE.JSON_ARR):
        raise ValueError

    if json.arr.count > 0 and json.arr.elems is None:
        raise ValueError

    json.arr.elems.append(val)
    json.arr.count += 1
    return val


def get_child(json: JSON, key: str, expect_type: JsonE):
    """
    获取名字为key，类型为expect_type的子节点（JSON值）
    :param json:对象类型的JSON值
    :param key:键名
    :param except_type:期望类型
    :return:找到的JSON值
    """
    child = json_get_member(json, key)
    if not child:
        return None
    if child.j_type is not expect_type:
        return None
    return child


def json_obj_get_num(json: JSON, key: str, default: float=0.0) -> float:
    """
    * 获取JSON对象中键名为key的数值，如果获取不到，或者类型不对，返回def
     * @param json json对象
     * @param key  成员键名
     * @param def  取不到结果时返回的默认值
     * @return double 获取到的数值
    """
    child = get_child(json, key, JsonE.JSON_NUM)
    if not child:
        return default
    return child.num


def json_obj_get_bool(json: JSON, key: str) -> bool:
    """
     * 获取JSON对象中键名为key的BOOL值，如果获取不到，或者类型不对，返回false
     * @param json json对象
     * @param key  成员键名
     * @return BOOL 获取到的键值
    """
    child = get_child(json, key, JsonE.JSON_BOL)
    if not child:
        return False
    return child.bol


def json_obj_get_str(json: JSON, key: str, default: str="") -> str:
    """
    * 获取JSON对象中键名为key的值，如果获取不到，则返回缺省值def
     * @param json 对象类型的JSON值
     * @param key  键名
     * @param def  找不到时返回的缺省值
     * @return 获取到的字符串结果
     * @details
     * 如果json不是对象类型，则返回def
     * 如果对应的值不是字符串类型，则返回def
     * 如:
     *  json: {"key": "str"}
     *  json_obj_get_str(json, "key", NULL) = "str"
     *  json_obj_get_str(json, "noexist", NULL) = NULL
     *  json_obj_get_str(json, "noexist", "") = ""
    """
    child = get_child(json, key, JsonE.JSON_STR)
    if not child:
        return default
    return child.str


def json_obj_set_num(json: JSON, key: str, val: float) -> int:
    if isinstance(val, int) or isinstance(val, float):
        new_json = json_new(JsonE.JSON_NUM)
        new_json.val = json_new_num(val)
        json_add_member(json, key, new_json)
        return val
    else:
        return None


def json_obj_set_bool(json: JSON, key: str, val: bool) -> bool:
    if isinstance(val, bool):
        new_json = json_new(JsonE.JSON_BOL)
        new_json.val = json_new_bool(val)
        json_add_member(json, key, new_json)
        return val
    else:
        return None


def json_obj_set_str(json: JSON, key: str, val: str) -> str:
    if isinstance(val, str):
        new_json = json_new(JsonE.JSON_STR)
        new_json.val = json_new_str(val)
        json_add_member(json, key, new_json)
        return val
    else:
        return None


def json_arr_count(json: JSON) -> int:
    if not json or json.j_type is not JsonE.JSON_ARR:
        return -1
    return json.arr.count


def json_arr_get_num(json: JSON, idx: int, default: float=0.0) -> float:
    res = json_get_element(json, idx)
    if res.j_type == JsonE.JSON_NUM:
        return res.num
    return default


def json_arr_get_bol(json: JSON, idx: int) -> bool:
    res = json_get_element(json, idx)
    if res.j_type == JsonE.JSON_BOL:
        return res.bol
    return False


def json_arr_get_str(json: JSON, idx: int, default: str="") -> str:
    res = json_get_element(json, idx)
    if res.j_type == JsonE.JSON_STR:
        return res.str
    return default


def json_arr_add_num(json: JSON, val: float) -> int:
    if isinstance(val, float) or isinstance(val, int):
        new_json = json_new(JsonE.JSON_NUM)
        new_json.val = json_new_num(val)
        json_add_element(json, new_json)
        return val
    else:
        raise TypeError


def json_arr_add_bool(json: JSON, val: bool) -> int:
    if isinstance(val, bool):
        new_json = json_new(JsonE.JSON_BOL)
        new_json.val = json_new_bool(val)
        json_add_element(json, new_json)
        return val
    else:
        raise TypeError


def json_arr_add_str(json: JSON, val: str) -> int:
    if isinstance(val, str):
        new_json = json_new(JsonE.JSON_STR)
        new_json.val = json_new_str(val)
        json_add_element(json, new_json)
        return val
    else:
        raise TypeError


def json_arr_pop(json: JSON, idx: int) -> JSON:
    json_get_element(json, idx)
    return json.arr.elems.pop(idx)


def json_obj_pop(json: JSON, key: str) -> JSON:
    json_get_member(json, key)
    i = 0
    for kv in json.obj.kvs:
        if kv.key == key:
            break
        i += 1
    kv = json.obj.kvs.pop(i)
    return kv.val
