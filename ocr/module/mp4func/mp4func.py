import os
from moviepy.editor import VideoFileClip
from PIL import Image


class Mp4Func(object):
    def __init__(self):
        pass

    def get_frame_from_mp4(self, mp4_path, frame_path=None):
        """
        :param mp4_path: 视频目录
        :param frame_path: 帧保存目录
        :return: 返回帧图片文件夹保存路径
        """
        if frame_path is None:
            frame_path = os.path.basename(mp4_path).split('.')[0]
        if not os.path.exists(frame_path):
            os.makedirs(frame_path)

        clip = VideoFileClip(mp4_path)
        i = 1
        fps = clip.fps
        for frame in clip.iter_frames():
            if i % fps == 0:
                img = Image.fromarray(frame)
                save_name = os.path.join(frame_path, "%05d.jpg" % i)
                img.save(save_name)
            i += 1
        return os.path.abspath(frame_path)
