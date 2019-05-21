#coding:utf-8

import json
import try_json_class

def try_json():
    value = {
            "nonev": None,
            "strv": "something",
            "intv": 100,
            "floatv": 200.56,
            "listv": [1,2,'something'],
            "arrayv": (100, 200),
            # 集和类型不能被json
            # "setv": {300, 400},
            "dictv": {
                "key": "value"
                }
            }

    json_value = json.dumps(value)
    print(json_value)
    # {"nonev": null, "strv": "something", "intv": 100, "floatv": 200.56, "listv": [1, 2, "something"], 
    # "arrayv": [100, 200], "dictv": {"key": "value"}}
    # 可以发现列表和元祖类型都转化成js中的数组

    value_from_json = json.loads(json_value)
    print(value_from_json)


# 自定义类的json处理
def convert_to_builtin_type(obj):
    d = {}
    d.update(obj.__dict__)
    d['__class__'] = obj.__class__._name
    d['__module__'] = obj.__module__
    print(d)
    return d

def dict_to_obj(d):
    if '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        _module = __import__(module_name)
        _class = getattr(_module, class_name)
        
        ins = _class(**d)
        return ins
    else:
        return d


def try_json2():
    m = try_json_class.MyClass('laker')
    m_json = json.dumps(m, default=convert_to_builtin_type)
    # print(m_json)

    m2 = json.loads(m_json, object_hook=dict_to_obj)
    m2.say_hello()






if __name__ == '__main__':
    # try_json()
    try_json2()
