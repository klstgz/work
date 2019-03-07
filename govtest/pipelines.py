# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import mysql.connector
import pandas as pd  #用来读MySQL
import redis
from scrapy.exceptions import DropItem
redis_db = redis.Redis(host='localhost', port=6379, db=4) #连接redis，相当于MySQL的conn
redis_data_dict = "f_url"  #key的名字，写什么都可以，这里的key相当于字典名称，而不是key值。


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




class DuplicatesPipeline(object):
    conn = mysql.connector.connect(user = 'root', password='951195', database='gov', charset='utf8')

    def __init__(self):
        redis_db.flushdb() #删除全部key，保证key为0，不然多次运行时候hlen不等于0，刚开始这里调试的时候经常出错。
        if redis_db.hlen(redis_data_dict) == 0: #
            sql = "SELECT url FROM guowuyuan;"  #从你的MySQL里提数据，我这里取url来去重。
            df = pd.read_sql(sql, self.conn) #读MySQL数据
            for url in df['url'].get_values(): #把每一条的值写入key的字段里
                redis_db.hset(redis_data_dict, url, 0) #把key字段的值都设为0，你要设成什么都可以，因为后面对比的是字段，而不是值。


    def process_item(self, item, spider):
        if redis_db.hexists(redis_data_dict, item['url']): #取item里的url和key里的字段对比，看是否存在，存在就丢掉这个item。不存在返回item给后面的函数处理
             raise DropItem("Duplicate item found: %s" % item)

        return item