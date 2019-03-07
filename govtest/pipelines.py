# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class GovtestPipeline(object):
    def __init__(self):
        # 连接MySQL数据库
        self.connect = pymysql.connect(host='localhost', user='root', password='951195', db='gov', port=3306)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # 往数据库里面写入数据
        sql = """insert into guowuyuan values ("{}","{}","{}","{}")""".format(item['url'],item['title'],item['time'],item['text'])
        self.cursor.execute(sql)
        self.connect.commit()
        return item

    # 关闭数据库
    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()



#
# class MySQLPipeline(object):
#
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # 从项目的配置文件中读取相应的参数
#         cls.MYSQL_DB_NAME = crawler.settings.get("MYSQL_DB_NAME", 'gov')
#         cls.HOST = crawler.settings.get("MYSQL_HOST", 'localhost')
#         cls.PORT = crawler.settings.get("MYSQL_PORT", 3306)
#         cls.USER = crawler.settings.get("MYSQL_USER", 'root')
#         cls.PASSWD = crawler.settings.get("MYSQL_PASSWORD", '951195')
#         return cls()
#
#     def open_spider(self, spider):
#         self.dbpool = adbapi.ConnectionPool('pymysql', host=self.HOST, port=self.PORT, user=self.USER, passwd=self.PASSWD, db=self.MYSQL_DB_NAME, charset='utf8')
#
#     def close_spider(self, spider):
#         self.dbpool.close()
#
#     def process_item(self, item, spider):
#         print item
#         self.dbpool.runInteraction(self.insert_db, item)
#
#         return item
#
#     def insert_db(self, tx, item):
#         values = (
#             item['url'],
#             item['title'],
#             item['time'],
#             item['text']
#
#         )
#         sql = 'INSERT INTO guowuyuan VALUES (%s,%s,%s,%s)'
#         tx.execute(sql, values)