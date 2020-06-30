import glob
import os

from ocr_tool import Judge
from baidu_ocr import BaiduOcr

baiduOcr = BaiduOcr()
judge = Judge()


def ocr_file(img_path):
    try:
        flag1 = baiduOcr.judge_card_baidu(img_path)
    except:
        flag1 = None
    if flag1 is None:
        flag2 = judge.judge_card(img_path)
        if flag2 is None:
            # return "异常"
            print('<{}>存在异常'.format(img_path))

        else:
            print('<{}>的类别是：{}'.format(img_path, flag2))
            # return flag2
    else:
        print('<{}>的类别是：{}'.format(img_path, flag1))
        # return flag1


def ocr_path(dir_path):
    bash_dir = os.path.abspath(dir_path)
    images = []
    images += glob.glob(os.path.join(bash_dir, '*.png'))
    images += glob.glob(os.path.join(bash_dir, '*.jpg'))
    images += glob.glob(os.path.join(bash_dir, '*.jpeg'))

    for num, img_path in enumerate(images):
        print(img_path)
        ocr_file(img_path)


def baidu_ocr_file(img_path):
    try:
        flag1 = baiduOcr.get_four_text(img_path)
    except:
        flag1 = None
    if flag1 is None:
        flag2 = judge.judge_card(img_path)
        if flag2 is None:
            # return "异常"
            print('<{}>存在异常'.format(img_path))

        else:
            print('<{}>的类别是：{}'.format(img_path, flag2))
            # return flag2
    else:
        print('<{}>的类别是：{}'.format(img_path, flag1))


ocr_path('huifeng')  # 检测文件夹下面所有图片
ocr_file("/home/huangjx/Projects/Thursday_yolo3/bank_logo/JH800_FH17122205.jpg")  # 检测一张图片
