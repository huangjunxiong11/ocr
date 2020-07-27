# -*- coding: utf-8 -*-
import base64
import requests
from flask_jsonrpc.proxy import ServiceProxy


class FsOcr:

    def __init__(self, ocr_docker_url):
        if not str(ocr_docker_url).startswith('http://'):
            ocr_docker_url = 'http://' + ocr_docker_url
        self.service = ServiceProxy('{}/session'.format(ocr_docker_url))

    def img_from_url(self, url):
        r = requests.get(url, timeout=20).content
        return base64.b64encode(r).decode()

    def img_from_path(self, file_path):
        return base64.b64encode(open(file_path, 'rb').read()).decode()

    def ocr(self, file_path=None, url=None, binary_content=None, split_str='<br>'):
        if url is not None:
            img = self.img_from_url(url)
        elif file_path is not None:
            img = self.img_from_path(file_path)
        elif binary_content is not None:
            img = base64.b64encode(binary_content).decode()
        else:
            raise ValueError('You should set url or file_path or binary_content.')
        try:
            response = self.service.ocr(img)
        except:
            print('Error:url is {} , file_path is {}'.format(url, file_path))
            response = list()
        text_list = list()
        try:
            # response有可能出现返回错误值
            for j in response:
                if j['text'] != '':
                    text_list.append(j['text'])
        except:
            text_list = []

        # return '{}'.format(split_str).join(text_list)
        return ''.join(text_list)

    def ocr_list(self, file_path_list=None, url_list=None, binary_content_list=None, split_str='<br>'):
        img_list = list()
        if url_list is not None:
            for url in url_list:
                img = self.img_from_url(url)
                img_list.append(img)
        elif file_path_list is not None:
            for file_path in file_path_list:
                img = self.img_from_path(file_path)
                img_list.append(img)
        elif binary_content_list is not None:
            for binary_content in binary_content_list:
                img = base64.b64encode(binary_content).decode()
                img_list.append(img)
        else:
            raise ValueError('You should set url or file_path or binary_content.')

        response_list = self.service.ocr_list(img_list)

        obj = list()
        for response in response_list:
            text_list = list()
            for j in response:
                if j['text'] != '':
                    text_list.append(j['text'])
            obj.append('{}'.format(split_str).join(text_list))
        return obj

    def ocr_video(self, url=None, binary_content=None):
        r = self.service.ocr_video(url=url, binary_content=binary_content)
        if isinstance(r, dict) and 'error' in r.keys():
            raise ValueError(r['error']['stack'])
        return r

    def speech_video(self, url=None, binary_content=None):
        r = self.service.speech_video(url=url, binary_content=binary_content)
        if isinstance(r, dict) and 'error' in r.keys():
            raise ValueError(r['error']['stack'])
        return r

    def video_append(self, image_content, movie_content, download_path=None, cover_position='first', cover_hold_sec=2):
        print('开始执行视频添加图片首帧（尾帧）功能，正在执行中...')
        r = self.service.video_append(image_content=image_content,
                                      movie_content=movie_content, cover_position=cover_position,
                                      cover_hold_sec=cover_hold_sec)
        if isinstance(r, dict) and 'error' in r.keys():
            raise ValueError(r['error']['stack'])

        if download_path is not None:
            with open(download_path, 'wb') as f:
                f.write(base64.b64decode(r))
        print('添加图片首帧（尾帧）执行成功')
        return r

    def video_resize(self, movie_content, percent=None, resize=None, download_path=None):
        """

        :param movie_content: [bytes] 视频二进制流
        :param percent: [float]放缩比例，按0.5倍数相乘
        :param resize: [tuple](width,height)
        :param download_path: [str] 下载路径
        :return: [bytes] 返回的视频二进制流
        """
        print('开始执行视频等比例修改尺寸功能，正在执行中..')

        r = self.service.video_resize(movie_content=movie_content, percent=percent, resize=resize)

        if isinstance(r, dict) and 'error' in r.keys():
            raise ValueError(r['error']['stack'])

        if download_path is not None:
            with open(download_path, 'wb') as f:
                f.write(base64.b64decode(r))
        print('视频等比例修改尺寸功能执行成功')
        return r

    def get_video_size(self, movie_content):
        r = self.service.get_video_size(movie_content=movie_content)
        if isinstance(r, dict) and 'error' in r.keys():
            raise ValueError(r['error']['stack'])

        return r

    def sr_picture(self, img_content, multiple=2, download_path=None):
        r = self.service.sr_picture(img_content=img_content, multiple=multiple)
        if isinstance(r, dict) and 'error' in r.keys():
            raise ValueError(r['error']['stack'])

        if download_path is not None:
            with open(download_path, 'wb') as f:
                f.write(base64.b64decode(r))
        return r


if __name__ == '__main__':
    pass
