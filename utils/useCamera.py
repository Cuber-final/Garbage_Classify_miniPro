from rest_framework.views import APIView
from rest_framework.response import Response
import numpy as np
import paddle
import paddle.fluid as fluid
from PIL import Image, ImageEnhance
import json

target_size = [3, 224, 224]
mean_rgb = [127.5, 127.5, 127.5]
use_gpu = True
place = fluid.CUDAPlace(0) if use_gpu else fluid.CPUPlace()
exe = fluid.Executor(place)
save_freeze_dir = "D:\\Django_dvn\\gc_backend\\utils\\trained_model"
paddle.enable_static()  # paddle 2.x 启动静态图
[inference_program, feed_target_names, fetch_targets] = fluid.io.load_inference_model(dirname=save_freeze_dir,
                                                                                      executor=exe)


def crop_image(img, target_size):
    width, height = img.size
    w_start = (width - target_size[2]) / 2
    h_start = (height - target_size[1]) / 2
    w_end = w_start + target_size[2]
    h_end = h_start + target_size[1]
    img = img.crop((w_start, h_start, w_end, h_end))
    return img


def resize_img(img, target_size):
    ret = img.resize((target_size[1], target_size[2]), Image.BILINEAR)
    return ret


def read_image(img_path):
    img = Image.open(img_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = crop_image(img, target_size)
    img = np.array(img).astype('float32')
    img -= mean_rgb
    img = img.transpose((2, 0, 1))  # HWC to CHW
    img *= 0.007843
    img = img[np.newaxis, :]
    return img


def infer(image_path):
    tensor_img = read_image(image_path)
    label = exe.run(inference_program, feed={feed_target_names[0]: tensor_img}, fetch_list=fetch_targets)
    return np.argmax(label)


def inferImg(img_path):
    label_path = 'D:\\Django_dvn\\gc_backend\\utils\\dicts.json'
    with open(label_path, 'r', encoding='utf-8') as f:
        dicMap = json.load(f)
    predict_label = infer(img_path)
    # print('预测垃圾类别：{}\n'.format(dicMap[str(predict_label)]))
    res = dicMap[str(predict_label)]
    return res


class CameraRec(APIView):
    def get(self, request):
        return Response("success")

    def post(self, request):
        # 获取图像
        save_dir = 'D:\\Django_dvn\\gc_backend\\utils\\testImgs\\upLoadImg.jpg'
        image = request.FILES.get('file')
        if not image:
            return Response({'msg': '图片上传出错', 'code': 0})
        username = request.POST.get('username')
        with open(save_dir, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        f.close()
        res = inferImg(save_dir)
        strList = str(res).split('_')
        # print(strList)
        pcName = strList[0]
        tcName = strList[1]
        fb_msg = {'name': tcName, 'pc_name': pcName, 'msg': '识别结果如下', 'code': 1}
        # print(fb_msg)
        return Response(fb_msg)
