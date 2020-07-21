import hashlib
import re
import time
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip


class GenInfor(object):
    # ['/home/huangjx/Projects/git-pro/changegrounp/changegrounp/master/pictrue/2020-06-22/heng/6.jpg',
    # '/home/huangjx/Projects/git-pro/changegrounp/changegrounp/master/video/2020-06-22/heng/WBFA720-LHD202005.mov']
    def __init__(self, background_path, mov_path):
        self.background_path = background_path
        self.mov_path = mov_path
        self.clip = VideoFileClip(self.mov_path)

    @property
    def gen_background_path(self):
        return self.background_path

    @property
    def gen_background_date(self):
        mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", self.background_path)
        background_date = mat.group(0)
        return background_date

    @property
    def gen_background_md5(self):
        """生成图片md5"""
        m = hashlib.md5()  # 创建md5对象
        with open(self.background_path, 'rb') as fobj:
            while True:
                data = fobj.read(4096)
                if not data:
                    break
                m.update(data)  # 更新md5对象
        return m.hexdigest()  # 返回md5对象

    @property
    def gen_mov_path(self):
        return self.mov_path

    @property
    def gen_mov_date(self):
        mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", self.mov_path)
        mov_date = mat.group(0)
        return mov_date

    @property
    def gen_mov_md5(self):
        """生成MOVmd5"""
        m = hashlib.md5()  # 创建md5对象
        with open(self.mov_path, 'rb') as fobj:
            while True:
                data = fobj.read(4096)
                if not data:
                    break
                m.update(data)  # 更新md5对象
        return m.hexdigest()  # 返回md5对象

    @property
    def gen_mp4_path(self):
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        dase_dir = self.background_path.split('/p', 1)[0]
        jpg_name = self.background_path.split("/")[-1]
        jpg_name = jpg_name.split('.', 1)[0]

        mov_name = self.mov_path.split('/')[-1]
        mov_name = mov_name.split('.', 1)[0]

        name = mov_name + '-' + jpg_name

        if '（' in self.mov_path:
            var_2 = mov_name.split('（', 1)[-1]
            var_3 = var_2.split('-', 1)[0]
        else:
            var_3 = mov_name.split('-', 1)[0]

        path = dase_dir + '/output/' + today + '/' + var_3 + '/'
        whole_path = path + name + '.mp4'
        return whole_path

    @property
    def gen_mp4_date(self):
        mp4_date = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        return mp4_date

    @property
    def gen_width(self):
        size = self.clip.size
        width = size[0]
        return width

    @property
    def gen_high(self):
        size = self.clip.size
        high = size[1]
        return high

    @property
    def gen_advertiser(self):
        (filepath, tempfilename) = os.path.split(self.mov_path)
        filename = tempfilename.split(".")[0]
        advertiser = filename.split("-")[0]
        return advertiser

    @property
    def gen_author(self):
        (filepath, tempfilename) = os.path.split(self.mov_path)
        filename = tempfilename.split(".")[0]
        author = filename.split("-")[1]
        return author

    @property
    def gen_duration(self):
        return self.clip.duration

    @property
    def gen_item(self):
        item = dict()
        item['background_path'] = self.gen_background_path
        item['background_date'] = self.gen_background_date
        item['background_md5'] = self.gen_background_md5

        item['mov_path'] = self.gen_mov_path
        item['mov_date'] = self.gen_mov_date
        item['mov_md5'] = self.gen_mov_md5

        item['mp4_path'] = self.gen_mp4_path
        item['mp4_date'] = self.gen_mp4_date

        item['width'] = self.gen_width
        item['high'] = self.gen_high

        item['advertiser'] = self.gen_advertiser
        item['author'] = self.gen_author
        item['duration'] = self.gen_duration

        return item


# gen_info = GenInfor(
#     background_path='/home/huangjx/Projects/git-pro/changegrounp/changegrounp/master/pictrue/2020-06-22/heng/6.jpg',
#     mov_path='/home/huangjx/Projects/git-pro/changegrounp/changegrounp/master/video/2020-06-22/heng/WBFA720-LHD202005.mov')
# item = gen_info.gen_item
# pass