import glob
import os
import time

from ocr_tool import Judge
from baidu_ocr import BaiduOcr
from utils.pre import Pre
from config import FLAGS

baiduOcr = BaiduOcr()
judge = Judge()
pre = Pre()


def ocr_file(img_path):
    """
    输入的是一张图片，输入图片归属类别结果
    :param img_path:
    :return:
    """
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
    """
    输入的是一个文件夹，输出的是这个文件夹里面所有图片的检测结果
    :param dir_path:
    :return:
    """
    bash_dir = os.path.abspath(dir_path)
    images = []
    images += glob.glob(os.path.join(bash_dir, '*.png'))
    images += glob.glob(os.path.join(bash_dir, '*.jpg'))
    images += glob.glob(os.path.join(bash_dir, '*.jpeg'))
    # imgs = os.listdir(dir_path)
    # new_imgs = [int(i.split('.', 1)[0]) for i in imgs]
    # new_imgs.sort()
    for num, img_path in enumerate(images):
        # print(img_path)
        # ocr_file(img_path)
        # img_path = os.path.join(bash_dir, (str(img_path)).zfill(4) + '.png')
        ocr_file_from_bin(img_path)
        time.sleep(2)


def bin_ocr_file(img_path):
    """
    输入的是一张图片的二进制表示，输出这张图片的类别
    :param img_path:
    :return:
    """

    try:
        flag1 = baiduOcr.from_bin(img_path)
    except:
        flag1 = None
    if flag1 is None:
        flag2 = judge.ocr_bin(img_path)
        if flag2 is None:
            return None
            # print('<{}>存在异常'.format(img_path))

        else:
            # print('<{}>的类别是：{}'.format(img_path, flag2))
            return flag2
    else:
        # print('<{}>的类别是：{}'.format(img_path, flag1))
        return flag1


def ocr_file_from_bin(img_path):
    """
    输入一张图片，通过bin的方式输出这张图片的类别
    :param img_path:
    :return:
    """
    four_bin = pre.four_cut(img_path)

    for m, n in enumerate(four_bin):
        a = bin_ocr_file(n)
        if a is not None:
            print('<{}>的类别是：{}'.format(img_path, a))
            return a

    print('<{}>识别不了'.format(img_path))


def dir(dir):
    bash_dir = os.path.abspath(dir)
    images = []
    images += glob.glob(os.path.join(bash_dir, '*.png'))
    images += glob.glob(os.path.join(bash_dir, '*.jpg'))
    images += glob.glob(os.path.join(bash_dir, '*.jpeg'))
    # imgs = os.listdir(dir)
    # new_imgs = [int(i.split('.', 1)[0]) for i in imgs]
    # new_imgs.sort()
    for m, n in enumerate(images):
        names = os.path.join(bash_dir, str(n))
        new_name = os.path.join(bash_dir, (str(m)).zfill(4) + '.png')
        os.rename(names, new_name)


if __name__ == '__main__':
    # 图片
    # ocr_file_from_bin("/home/huangjx/Projects/git-pro/ocr/银行卡/上海银行-素材/0000.png")

    # 文件夹路径
    ocr_path("/home/huangjx/Projects/git-pro/ocr/银行卡/广发银行-素材")
