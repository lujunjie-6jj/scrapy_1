# -*- coding: utf-8 -*-
import scrapy
import re
from jd.items import JdItem

class LagouSpider(scrapy.Spider):
    name = 'douban'
    #allowed_domains = ['https://movie.douban.com']
    base_url='https://movie.douban.com/top250?start='
    def start_requests(self):
        new_url='&filter='

        headers={
            'Cookie':'bid=TbT8Hnzp6Kk; _vwo_uuid_v2=D08DE015CCB7512E18141700B2447FC7D|36e0d48549549a6d2e8e7244dd233ad0; gr_user_id=2d411ea5-084f-4c48-8618-586377c2ce74; ll="118172"; __yadk_uid=oOwoNVOAOh4P9htR1gCk4ZPQiE0N7DG0; viewed="1139426_25902102_19952400_1885170_20432061"; ps=y; douban-fav-remind=1; ap_v=1,6.0; __utmc=30149280; __utmz=30149280.1535295055.30.12.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=223695111; __utmz=223695111.1535295055.13.6.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); Hm_lvt_1cf880de4bc3c11500482f152b3353c0=1535084888,1535295061,1535295089,1535295198; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1535297264%2C%22https%3A%2F%2Fwww.google.com.hk%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.856879701.1527341793.1535295055.1535297264.31; __utmb=30149280.0.10.1535297264; __utma=223695111.1842961209.1527473115.1535295055.1535297265.14; __utmb=223695111.0.10.1535297265; _pk_id.100001.4cf6=7cba1bc61a5b2cd2.1527473116.14.1535297377.1535295232.; Hm_lpvt_1cf880de4bc3c11500482f152b3353c0=1535297383',
            'Referer':'https: // movie.douban.com / top250?start = 50 & filter =',
           ' Accept - Language': 'zh - CN, zh;q = 0.9',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }

        for i in range(0,226,25):
            url=self.base_url+str(i)+new_url
            yield scrapy.Request(url=url,headers=headers,callback=self.parse)

    def parse(self, response):
        item = JdItem()
        item['title_ch'] = response.xpath('//div[@class="hd"]//span[@class="title"][1]/text()').extract()

        # 本想按title-title-other 取出3个名字，但有的只有title-other，例如霸王别姬。所以只取一个名字
        # en_list = response.xpath('//div[@class="hd"]//span[@class="title"][2]/text()').extract()
        # item['title_en'] = [en.replace('\xa0/\xa0','').replace('  ','') for en in en_list]
        # ht_list = response.xpath('//div[@class="hd"]//span[@class="other"]/text()').extract()
        # item['title_ht'] = [ht.replace('\xa0/\xa0','').replace('  ','') for ht in ht_list]
        # detail_list = response.xpath('//div[@class="bd"]/p[1]/text()').extract()
        # item['detail'] = [detail.replace('  ', '').replace('\xa0', '').replace('\n', '') for detail in detail_list]
        # 注意：有的电影没有quote！！！！！！！！！！
        # item['quote'] = response.xpath('//span[@class="inq"]/text()').extract()

        item['rating_num'] = response.xpath('//div[@class="star"]/span[2]/text()').extract()
        # 评价数格式：“XXX人评价”。用正则表达式只需取出XXX数字
        count_list = response.xpath('//div[@class="star"]/span[4]/text()').extract()
        item['rating_count'] = [re.findall('\d+', count)[0] for count in count_list]
        item['image_urls'] = response.xpath('//div[@class="pic"]/a/img/@src').extract()
        item['topid'] = response.xpath('//div[@class="pic"]/em/text()').extract()

        yield item

