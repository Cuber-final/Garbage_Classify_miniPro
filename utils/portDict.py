import django
import json
import os
from wx.models import TcCate

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gc_backend.settings')
# django.setup()
dir_path = os.path.join("D:\\Django_dvn\\gc_backend\\utils", "dicts.json")


def InputCates():
    with open(dir_path, 'r', encoding="utf-8") as f:
        data = json.load(f)

    dict_len = len(data)
    print("type length is {}".format(dict_len))
    print(type(data))

    pc_name = ['其他垃圾', '厨余垃圾', '可回收物', '有害垃圾']
    id_dict = [0, 1, 2, 3]
    # 父类ID
    index = 0
    for parent_id in id_dict:
        TcCate.objects.create(tc_id=parent_id, tc_name=pc_name[index], tc_parent_id=parent_id)
        index = index + 1

    for key in data:
        class_id = int(key) + 4
        class_str = data[key]
        parent_str = class_str[0:4]
        class_str = class_str[5:]
        if (parent_str == pc_name[0]):
            parent_id = id_dict[0]
        if (parent_str == pc_name[1]):
            parent_id = id_dict[1]
        if (parent_str == pc_name[2]):
            parent_id = id_dict[2]
        if (parent_str == pc_name[3]):
            parent_id = id_dict[3]
        # print(key + " : " + data[key])
        # print("id : {} name : {} pid : {} par_name : {}".format(class_id, class_str, parent_id, parent_str))
        TcCate.objects.create(tc_id=class_id, tc_name=class_str, tc_parent_id=parent_id)
    print('成功')


def PcIdentify(parent_name):
    pc_name = ['其他垃圾', '厨余垃圾', '可回收物', '有害垃圾']
    id_dict = [0, 1, 2, 3]
    parent_id = 0
    if (parent_name == pc_name[0]):
        parent_id = id_dict[0]
    if (parent_name == pc_name[1]):
        parent_id = id_dict[1]
    if (parent_name == pc_name[2]):
        parent_id = id_dict[2]
    if (parent_name == pc_name[3]):
        parent_id = id_dict[3]
    return parent_id
