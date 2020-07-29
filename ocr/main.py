import glob
import shutil
import os
import pathlib
import sys

sys.path.insert(0, os.path.abspath(pathlib.Path.cwd()))
from ocr.module.identify.identify import Identify
from ocr.module.baiduocr.baiduocr import BaiduOcr
from ocr.module.fsocr.fsocr import FsOcr
from ocr.module.mysqldb.db import DbOperation
from ocr.docs.config import *

baiduocr_huangjx = BaiduOcr(APP_ID, API_KEY, SECRET_KEY)
baiduocr_fs1 = BaiduOcr(APP_ID_fs1, API_KEY_fs1, SECRET_KEY_fs1)
baiduocr_fs2 = BaiduOcr(APP_ID_fs2, API_KEY_fs2, SECRET_KEY_fs2)
fsocr = FsOcr(ocr_docker_url=OCR_DOCKER_URL)

identify_huangjx = Identify(baidu=baiduocr_huangjx)  # 只使用百度的ocr
identify_fs1 = Identify(baidu=baiduocr_fs1)  # 只使用百度的ocr
identify_fs2 = Identify(baidu=baiduocr_fs1)  # 只使用百度的ocr


def detect_mp4(mp4_path, frame_path, sensitive_works):
    """
    检测出视频是否存在sensitive_works中的敏感词
    :param mp4_path: 视频路径
    :param frame_path: 帧图片暂时保存路径
    :param sensitive_works: 敏感词
    :return:
    """
    try:
        try:
            wenzis = identify_fs1.mp4_indentify(mp4_path=mp4_path, frame_path=frame_path)
            all_probably_sensitive_works = identify_fs1.classify(sensitive_works=sensitive_works, wenzis=wenzis)
        except:
            wenzis = identify_fs2.mp4_indentify(mp4_path=mp4_path, frame_path=frame_path)
            all_probably_sensitive_works = identify_fs2.classify(sensitive_works=sensitive_works, wenzis=wenzis)
    except:
        wenzis = identify_huangjx.mp4_indentify(mp4_path=mp4_path, frame_path=frame_path)
        all_probably_sensitive_works = identify_huangjx.classify(sensitive_works=sensitive_works, wenzis=wenzis)
    n = len(all_probably_sensitive_works)
    shutil.rmtree(frame_path)
    if n == 0:
        # print('不存在敏感词')
        return False
    else:
        # print('可能存在以下敏感词')
        return all_probably_sensitive_works


def test_detect_mp4(path, frame_path, sensitive_works):
    """
    测试函数，璇哥不用管
    :param path:
    :param frame_path:
    :param sensitive_works:
    :return:
    """

    BaseName = os.path.abspath(path)
    BaseName = glob.glob(os.path.join(BaseName, '*.mp4'))  # 读取文件夹下面所有的文件
    for mp4 in BaseName:
        re = detect_mp4(mp4, frame_path, sensitive_works)
        with open('/home/huangjx/Projects/git-pro/ocr/ocr/docs/6月防癌.txt', 'a') as f:
            f.write(mp4 + str(re) + '\n')


if __name__ == '__main__':
    """
    使用示例
    """
    mp4_path = '/home/huangjx/视频/6月防癌.mp4'
    frame_path = './frame'
    sensitive_works = FANGAIX_ADD
    false_or_true = detect_mp4(mp4_path, frame_path, sensitive_works)
    pass
