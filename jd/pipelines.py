# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request
from jd import settings
import pymysql


class JdPipeline(object):
    # 电影封面命名：序号加电影名
    def _createmovieImageName(self, item):
        lengh = len(item['topid'])
        return [item['topid'][i] + "-" + item['title_ch'][i] + ".jpg" for i in range(lengh)]

    def process_item(self, item, spider):
        namelist = self._createmovieImageName(item)
        dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)
        # print('dir_path', dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for i in range(len(namelist)):
            image_url = item['image_urls'][i]
            file_name = namelist[i]
            file_path = '%s/%s' % (dir_path, file_name)
            if os.path.exists(file_path):
                print("重复，跳过：" + image_url)
                continue
            with open(file_path, 'wb') as file_writer:
                print("正在下载：" + image_url)
                conn = request.urlopen(image_url)
                file_writer.write(conn.read())
        return item




class Douban_moviePipeline(object):
    def __init__(self):
        # 创建数据库连接,格式为utf8
        self.conn = pymysql.connect(
            host='localhost',
            user="root",
            passwd="****",
            db='testdb',
            charset="utf8"
        )

        self.cursor = self.conn.cursor()

    def creat_tables(self):
        # 使用execute方法执行这条sql语句: 如果ysw表已经存在，则删除
        #self.cursor.execute("drop table if exists DOUBANTOPMOVIE")
        # 创建ysw表,格式为utf8
        create_ysw = '''
                           CREATE TABLE DOUBANTOPMOVIE (
          topid int(3) PRIMARY KEY ,
          title_ch VARCHAR(50) ,
          rating_num FLOAT(1),
          rating_count INT(9),
          quote VARCHAR(100),
          createdTime TIMESTAMP(6) not NULL DEFAULT CURRENT_TIMESTAMP(6),
          updatedTime TIMESTAMP(6) not NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8;'''
        # 执行create_ysw语句
        self.cursor.execute(create_ysw)


    def process_item(self, item, spider):

        #self.creat_tables()

        sql = "insert into doubantopmovie(topid,title_ch,rating_num,rating_count) values(%s,%s,%s,%s)"
        lengh = len(item['topid'])
        for i in range(lengh):
            params = (item["topid"][i], item["title_ch"][i], item["rating_num"][i], item["rating_count"][i])

            try:
                self.cursor.execute(sql, params)
                self.conn.commit()
            except Exception as e:
                print(e)

        return item

















