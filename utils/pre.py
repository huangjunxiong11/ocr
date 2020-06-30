import cv2
import numpy as np
from PIL import Image
from io import BytesIO


class Pre():
    def __init__(self):
        pass

    def four_cut(self, file_name):
        ref = cv2.imread(filename=file_name)
        h, w, c = ref.shape
        ref_son1 = ref[0:int(h / 4), :, :]
        ref_son2 = ref[int(h / 4):int(h / 2), :, :]
        ref_son3 = ref[int(h / 2):3 * int(h / 4), :, :]
        ref_son4 = ref[3 * int(h / 4):h, :, :]

        img_bin1 = self.np_to_bin(ref_son1)
        img_bin2 = self.np_to_bin(ref_son2)
        img_bin3 = self.np_to_bin(ref_son3)
        img_bin4 = self.np_to_bin(ref_son4)

        cv2.imwrite('ref_son1.png', ref_son1)
        return [img_bin1, img_bin2, img_bin3, img_bin4]
        pass

    def np_to_bin(self, np_data):
        ret, buf = cv2.imencode(".jpg", np_data)
        img_bin = Image.fromarray(np.uint8(buf)).tobytes()
        return img_bin


if __name__ == '__main__':
    pre = Pre()
    pre.four_cut('/home/huangjx/Projects/git-pro/ocr/银行卡/浦发银行-字体限制/吉利.png')
