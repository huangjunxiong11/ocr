import os
import shutil
import time

from db.db_findall import Db_Operation
from mp4_ocr import WeiBao
from config import yilx_sensitive_works


class Run():
    def __init__(self):
        self.db_operation = Db_Operation()
        self.weibao = WeiBao(frame_path='./frame')  # 这里暂时缓冲一个文件夹，使用过后需要删除
        pass

    def mp4_identify(self, mp4_path, sensitive_works):
        """
        判断输入的视频是否包含自己所指定的敏感词，
        True表示包含敏感词
        False表示不包含敏感词
        :param mp4_path: 例如：‘～/123.mp4’
        :param sentitive_works: 例如['防癌', '防癌险', '200万', '3元', '4.1元', '人保', '中国人保', '售完即止', '再买就没了']
        :return: True或False
        """
        self.weibao.from_mp4_get_frame(mp4_path)
        flag = self.weibao.mp4_works_identify(sensitive_works)
        shutil.rmtree('./frame')  # 检测一个视频之后要将缓冲的帧图片删除掉
        return flag

    def test_case(self, sensitive_works):
        """
        从数据库中读取今天所有的视频目录并进行去重，然后进行检测
        :param sensitive_works:
        :return:
        """
        try:
            jpgs, mp4s = self.db_operation.jpgs_mp4s
        except:
            print('读取数据库路径失败')
            jpgs = []
            mp4s = []
        if not (jpgs is None and mp4s is None):
            for i, mp4 in enumerate(mp4s):
                mp4 = os.path.join(r'http://adsys.gzfsnet.com/python/Api/gdt_v3', mp4)
                try:
                    # print(mp4)
                    flag = self.mp4_identify(mp4_path=mp4, sensitive_works=sensitive_works)
                except:
                    # print(mp4)
                    flag = False
                if flag:
                    print("视频{}包含敏感词{}".format(mp4, sensitive_works))


def timer(func):
    def wrapper(*args, **kwds):
        t0 = time.time()
        func(*args, **kwds)
        t1 = time.time()
        print('耗时%0.3f' % (t1 - t0,))

    return wrapper


@timer
def main():
    """
    示例入门代码
    :return:
    """
    run = Run()
    result = run.mp4_identify("/home/huangjx/Projects/git-pro/ocr/data/heng.mp4", yilx_sensitive_works)
    # run.test_case(yilx_sensitive_works)
    # print(result)
    # run.test_case(sensitive_works=yilx_sensitive_works)


if __name__ == '__main__':
    main()
