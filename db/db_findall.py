import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))).split('db')[0])
from Db import MysqlAlchemy
import MySQLdb
from db.config import HOST, PORT, PASSWORD, DB, USER


class Db_Operation():
    def __init__(self):
        self.db = MysqlAlchemy(host=HOST,
                               port=PORT,
                               password=PASSWORD,
                               db=DB,
                               user=USER)

    @property
    def findall(self):
        today = time.strftime("'%Y-%m-%d'", time.localtime(time.time()))
        sql = "SELECT upload_date, material_url, video_url from tb_insurance_delivery WHERE advertisement ='微保' " \
              "and upload_date >= " + today + ";"

        return self.db.fetch_all(sql)

    @property
    def jpgs_mp4s(self):
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
    db_operation = Db_Operation()
    a, b = db_operation.jpgs_mp4s
    pass
