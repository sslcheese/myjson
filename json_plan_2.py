#!/usr/bin/env python
# coding=utf-8
import re
from enum import Enum


class JsonE(Enum):
    JSON_NONE = 0
    JSON_BOL = 1  # BOOL类型
    JSON_NUM = 2  # 数值类型
    JSON_STR = 3  # 字符串类型
    JSON_ARR = 4  # 数组类型
    JSON_OBJ = 5  # 对象类型


class KeyValue:
    def __init__(self, key, val):
        self.key: str = key
        self.val: JSON = val

    def __str__(self):
        res = "".join(('"', self.key, '": ', str(self.val)))
        return res


class JSON:
    def __init__(self):
        self._j_type = JsonE.JSON_NONE
        self._val = None

    def __str__(self):
        return str(self._val)

    @property
    def type(self):
        return self._j_type

    @property
    def value(self):
        return self._val


    def delete(self):
        pass

    @staticmethod
    def is_key_legal(key: str):
        # 正则检查key是否合法
        try:
            k = re.findall("[a-zA-Z][a-zA-Z0-9_]*", key)[0]
            if key == k:
                return True
        except IndexError as e:
            return False


    def add_member(self, key: str, val):
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
        if self._j_type is not JsonE.JSON_OBJ:
            raise TypeError("json类型错误")
        if not isinstance(val, JSON):
            raise TypeError("val类型错误")
        if self._count > 0 and self._val is None:
            raise ValueError

        # 想想: 为啥不用assert检查val？
        # 想想：如果json中已经存在名字为key的成员，怎么办？
        # 正则检查key是否合法
        if not self.is_key_legal(key):
            return None

        for kv in self._val:
            if kv.key == key:
                kv.value = val
                return val
        new_kv = KeyValue(key, val)
        self._val.append(new_kv)
        self._count += 1

        return val


class JsonNum(JSON):
    def __init__(self):
        super().__init__()
        self._j_type: JsonE = JsonE.JSON_NUM
        self._val = 0


class JsonBool(JSON):
    def __init__(self):
        super().__init__()
        self._j_type: JsonE = JsonE.JSON_BOL
        self._val = False


class JsonString(JSON):
    def __init__(self):
        super().__init__()
        self._j_type: JsonE = JsonE.JSON_STR
        self._val = ""


class JsonArray(JSON):
    def __init__(self):
        super().__init__()
        self._j_type: JsonE = JsonE.JSON_ARR
        self._val = []
        self._count = 0

    def __str__(self):
        res = "["
        for e in self._val:
            res += str(e) + ","
        res = res.rstrip(",")
        res += "]"
        return res




class JsonObject(JSON):
    def __init__(self):
        super().__init__()
        self._j_type: JsonE = JsonE.JSON_OBJ
        self._val = []
        self._count = 0

    def __str__(self):
        res = "{"
        for kv in self._val:
            res = "".join((res, str(kv)))
            res += ","
        res = res.rstrip(",")
        res += "}"
        return res

    def get(self, key: str) -> JSON:
        '''
        从对象类型的JSON值中获取名字为key的成员(JSON值)
        :param json:对象类型的JSON值
        :param key:成员的键名
        :return:找到的成员
        '''
        assert not (self._count > 0 and self._val is None)

        for i in range(self._count):
            if self._val[i].key == key:
                return self._val[i].val
        return None

    def set(self, path: str, val: JSON):
        path_list = path.split(".")
        if len(path_list) == 1:
            self.add_member(path_list[0], val)
        else:
            key = path_list.pop(0)
            child = self.get(key)
            child.set(".".join(path_list), val)


class JsonFactory:
    @staticmethod
    def json_new(j_type: JsonE) -> JSON:
        json = None
        if j_type == JsonE.JSON_NUM:
            json = JsonNum()
        elif j_type == JsonE.JSON_BOL:
            json = JsonBool()
        elif j_type == JsonE.JSON_STR:
            json = JsonString()
        elif j_type == JsonE.JSON_ARR:
            json = JsonArray()
        elif j_type == JsonE.JSON_OBJ:
            json = JsonObject()
        return json

    @staticmethod
    def json_new_num(val: float) -> JSON:
        json = JsonFactory.json_new(JsonE.JSON_NUM)
        json.num = val
        return json

    @staticmethod
    def json_new_bool(val: bool) -> JSON:
        json = JsonFactory.json_new(JsonE.JSON_BOL)
        json.bol = val
        return json

    @staticmethod
    def json_new_str(val: str) -> JSON:
        if not val:
            raise ValueError("")
        json = JsonFactory.json_new(JsonE.JSON_STR)
        json.str = val
        return json


# 这两个方法应该存在哪一个类里作为静态方法？
def json_write(j: JSON, level: int, f):
    '''
    用于json_save函数，对已经打开的文件进行递归写入
    :param j: 将写入的JSON对象
    :param level: 当前的层级，用于计算缩进
    :param f:以及打开的文件对象
    :return:
    '''
    tab = 2
    if j.type == JsonE.JSON_NUM:
        # f.write(" "*level*tab)
        f.write(str(j.value) + "\n")
    elif j.type == JsonE.JSON_BOL:
        # f.write(" "*level*tab)
        f.write(str(j.value) + "\n")
    elif j.type == JsonE.JSON_STR:
        # f.write(" "*level*tab)
        f.write(j.value + "\n")
    elif j.type == JsonE.JSON_ARR:
        for a in j.value:
            f.write(" " * level * tab + "- ")
            if a.val.j_type == JsonE.JSON_OBJ or a.val.j_type == JsonE.JSON_ARR:
                f.write("\n")
            json_write(a, level + 1, f)
    elif j.type == JsonE.JSON_OBJ:
        for kv in j.value:
            f.write(" " * level * tab + str(kv.key) + ": ")
            if kv.val.j_type == JsonE.JSON_OBJ or kv.val.j_type == JsonE.JSON_ARR:
                f.write("\n")
            json_write(kv.val, level + 1, f)


def json_save(json: JSON, fname: str) -> int:
    with open(fname, "w+", newline="") as f:
        json_write(json, 0, f)
    return 1



if __name__ == '__main__':
    def main():
        json = JsonFactory.json_new(JsonE.JSON_OBJ)
        print(json)
        json.set("basic", JsonFactory.json_new(JsonE.JSON_OBJ))
        json.set("basic.enable", JsonFactory.json_new_bool(True))
        print(json)

    main()






