import os
import re
import traceback
from sqlalchemy import create_engine
from .exception import *


class Single(object):
    """
    单例模式
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Single, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance


class MysqlAlchemy(Single):
    def __init__(self, **kwargs):
        self.conn_config = kwargs
        self.db_connect_string = "mysql://{user}:{password}@{host}:{port}/{db_name}?charset={charset}".format(
            host=self.conn_config["host"],
            user=self.conn_config["user"],
            password=self.conn_config["password"],
            db_name=self.conn_config["db"],
            port=int(self.conn_config["port"]) if self.conn_config["port"] else 3306,
            charset=self.conn_config["charset"] if "charset" in self.conn_config else 'utf8',
        )
        # 创建数据库引擎,echo为True,会打印所有的sql语句
        self.engine = create_engine(self.db_connect_string,
                                    echo=True if kwargs.get('debug', True) else False)
        self.logger = None
        self.log_rpc = None

        # 使用orm
        # 创建会话类
        # self.db_session = sessionmaker(bind=self.engine)

    def execute(self, sql):
        conn = self.engine.connect()
        try:
            conn.execute(sql)
            # conn.commit()
        except Exception as e:
            self.logger_db(logger=getattr(self, 'logger', None), message=e, mod='error')
            self.rpc_log_db(logger=getattr(self, 'logger', None), rpc=getattr(self, 'log_rpc', None),
                            message=e, error=traceback.format_exc())
            MySQLException(e, traceback.format_exc())
        finally:
            conn.close()

    def query(self, sql, args=None):
        conn = self.engine.connect()
        try:
            if re.search("^SELECT", sql, re.IGNORECASE) is not None:
                data = conn.execute(sql).fetchall()
                # conn.commit()
                return data
            elif re.search("^INSERT\s+INTO[\s\S]+VALUES", sql, re.IGNORECASE) is not None:
                conn.execute(sql)
                # conn.commit()
                return
            else:
                if args:
                    conn.execute(sql, args)
                    # conn.commit()
                else:
                    conn.execute(sql)
                    # conn.commit()
                return None
        except Exception as e:
            conn.rollback()
            self.logger_db(logger=getattr(self, 'logger', None), message=e, mod='error')
            self.rpc_log_db(logger=getattr(self, 'logger', None), rpc=getattr(self, 'log_rpc', None),
                            message=e, error=traceback.format_exc())
        finally:
            conn.close()

    def insert_update(self, table, data, unique_index: list, primary_key='id'):
        """
        根据唯一索引判断是否重复插入,如果有即更新,无即即插入
        :param table: 表名
        :param data: 数据
        :param unique_index: 唯一索引
        :param primary_key: 主键,默认为id
        :return:
        """
        conn = self.engine.connect()
        try:
            keys = ""
            values = ""
            duplicate_key = list()

            for key, value in data.items():
                if key not in unique_index and key != primary_key:
                    duplicate_key.append("`" + key + '`=VALUES(' + key + ')')
                keys += ",`" + key + "`" if len(keys) > 0 else "`" + key + "`"
                values += ",%s" if len(values) > 0 else "%s"
            sql_query_duplicate_key = ','.join(duplicate_key)
            sql = "INSERT INTO " + table + " (" + keys + ") VALUES (" + values + ")" + \
                  " ON DUPLICATE KEY UPDATE " + sql_query_duplicate_key
            arg = tuple(data.values())
            print(sql)
            conn.execute(sql, arg)
            return
        except Exception as e:
            self.logger_db(logger=getattr(self, 'logger', None), message=e, mod='error')
            self.rpc_log_db(logger=getattr(self, 'logger', None), rpc=getattr(self, 'log_rpc', None),
                            message=e, error=traceback.format_exc())
            raise e
        finally:
            conn.close()

    def insert(self, table, data):
        """
        插入操作
        :param table:
        :param data:
        :return:
        """
        # INSERT INTO table_name (列1, 列2,...) VALUES (值1, 值2,....)
        conn = self.engine.connect()
        try:
            keys = ""
            values = ""
            for key, value in data.items():
                keys += "," + key if len(keys) > 0 else key
                values += ",%s" if len(values) > 0 else "%s"
            sql = "INSERT INTO " + table + " (" + keys + ") VALUES (" + values + ")"
            conn.execute(sql, tuple(data.values()))
            # conn.commit()
        except Exception as e:
            self.logger_db(logger=getattr(self, 'logger', None), message=e, mod='error')
            self.rpc_log_db(logger=getattr(self, 'logger', None), rpc=getattr(self, 'log_rpc', None),
                            message=e, error=traceback.format_exc())

            MySQLException(e, traceback.format_exc())
        finally:
            conn.close()

    def fetch_one(self, sql):
        conn = self.engine.connect()
        try:
            data = conn.execute(sql).fetchone()
            if data:
                res = {c[0]: c[1] for c in data.items()}
            else:
                res = {}
            return res
        except Exception as e:
            self.logger_db(logger=getattr(self, 'logger', None), message=e, mod='error')
            self.rpc_log_db(logger=getattr(self, 'logger', None), rpc=getattr(self, 'log_rpc', None),
                            message=e, error=traceback.format_exc())
        finally:
            conn.close()

    def fetch_all(self, sql):
        conn = self.engine.connect()
        rsp = None
        try:
            data = conn.execute(sql).fetchall()
            # rsp = {c[0]: c[1] for c in data.items()}
            rsp = []
            for item in data:
                rsp.append({c[0]: c[1] for c in item.items()})
        except:
            rsp = None
        finally:
            conn.close()
            return rsp

    def logger_db(self, logger, message, mod='info'):
        if logger:
            if mod == 'info':
                logger.info(message)
            else:
                logger.error(message)
        else:
            print(message)

    def rpc_log_db(self, rpc, message, logger, error):
        if rpc:
            rpc.logger_rpc(level=10, pattern=1,
                           message=message, context=error)
        else:
            self.logger_db(logger, message, mod='error')

    def insert_update_batch(self, table, data, unique_index: list, primary_key='id'):
        """
        根据唯一索引判断是否重复插入,如果有即更新,无即即插入
        :param table: 表名
        :param data: 数据
        :param unique_index: 唯一索引
        :param primary_key: 主键,默认为id
        :return:
        """
        conn = self.engine.connect()
        try:
            keys = ""
            values = ""
            sql_query_duplicate_key = ','.join([unique + '=values(' + unique + ')' for unique in unique_index])

            for key, value in data[0].items():
                keys += ",`" + key + "`" if len(keys) > 0 else "`" + key + "`"

            args = [str(tuple(data[i].values())) for i in range(len(data))]
            values = ','.join(args)

            sql = "INSERT INTO " + table + " (" + keys + ") VALUES " + values + "" + \
                  " ON DUPLICATE KEY UPDATE " + sql_query_duplicate_key
            conn.execute(sql)
            return
        except Exception as e:
            raise (e)
        finally:
            conn.close()

    def update(self, table, data, condition):
        conn = self.engine.connect()
        try:
            update_fields = []
            condition_fields = []
            for key, value in data.items():
                field_text = " {k} = '{v}' ".format(k=key, v=value)
                if field_text:
                    update_fields.append(field_text)
            if not update_fields:
                return
            for k, v in condition.items():
                if k and v:
                    condit = " {k} = '{v}' ".format(k=k, v=v)
                    condition_fields.append(condit)
            if not condition_fields:
                return
            condition_fields_text = ' and '.join(condition_fields)
            update_fields_text = ','.join(update_fields)
            sql = "update {table} set {update_fields} where {condition_fields_text}".format(table=table,
                                                                                            update_fields=update_fields_text,
                                                                                            condition_fields_text=condition_fields_text)
            print(sql)
            conn.execute(sql)
        except Exception as e:
            print("update", e)
        finally:
            conn.close()


if __name__ == '__main__':
    pass
