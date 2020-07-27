import time
from .DB import MysqlAlchemy


class DbOperation(object):
    def __init__(self, HOST, PORT, PASSWORD, DB, USER):
        """
        初始化连接数据库
        """
        self.db = MysqlAlchemy(host=HOST,
                               port=PORT,
                               password=PASSWORD,
                               db=DB,
                               user=USER)

    @property
    def findall(self):
        """
        查找今天以内的所有视频，返回一个列表
        :return:
        """
        today = time.strftime("'%Y-%m-%d'", time.localtime(time.time()))
        sql = "SELECT upload_date, material_url, video_url from tb_insurance_delivery WHERE advertisement ='微保' " \
              "and upload_date >= " + today + ";"

        return self.db.fetch_all(sql)

    @property
    def jpgs_mp4s(self):
        """
        返回查找到的所有图片路径和所有视频路径
        :return:
        """
        results = self.findall
        jpgs = []
        mp4s = []
        for i, item in enumerate(results):
            jpgs.append(item["material_url"])
            mp4s.append(item["video_url"])
        jpgs = list(set(jpgs))
        mp4s = list(set(mp4s))
        return jpgs, mp4s


if __name__ == '__main__':
    # db_operation = Db_Operation()
    # a, b = db_operation.jpgs_mp4s
    pass
