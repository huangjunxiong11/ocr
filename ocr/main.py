from ocr.module.identify.identify import Identify
from ocr.module.baiduocr.baiduocr import BaiduOcr
from ocr.module.fsocr.fsocr import FsOcr
from ocr.module.mysqldb.db import DbOperation

APP_ID = "16001050"
API_KEY = "qq2hZITa1wlg1rWjdnDTkGeS"
SECRET_KEY = "GwpL4s5HGE4DHSQrpN1YSBn2laeGaagL"
baiduocr = BaiduOcr(APP_ID, API_KEY, SECRET_KEY)

fsocr = FsOcr(ocr_docker_url='http://192.168.8.126:5010')
identify = Identify(baidu=baiduocr, fs=fsocr)
wenzi = identify.jpg_indentify(jpg='/home/huangjx/文档/项目和集/ocr/frame/00775.jpg')
identify.write_wenzi(wenzi=wenzi, wenzi_path='/home/huangjx/Projects/git-pro/ocr/ocr/docs/00775.txt')

pass
