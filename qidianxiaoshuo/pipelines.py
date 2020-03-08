# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os


class QidianxiaoshuoPipeline(object):
    def process_item(self, item, spider):
        path = 'C:/ruanjian'
        if not os.path.exists(path):
            os.mkdir(path)

        if not os.path.exists(path + '/小说'):
            os.mkdir(path + '/小说')

        path2 = path + '/小说'
        if not os.path.exists(path2 + '/' + item['novel_name']):
            os.mkdir(path2 + '/' + item['novel_name'])

        path3 = path2 + '/' + item['novel_name']
        novel = '{}.txt'.format(item['c_name'])
        # 动态创建小说的文件
        self.file = open(path3 + '/' + novel, 'a', encoding='utf-8')
        self.file.write(item['c_name'] + '\n' + item['content'])
        self.file.close()
        print("<<<<<<<<<<<爬取结束<<<<<<<<")
