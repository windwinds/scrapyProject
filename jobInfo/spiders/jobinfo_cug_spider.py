# -*- coding:utf-8 -*-
import scrapy
import json
from scrapy import Selector
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ..items import CampusTalkItem, ShuangXuanHui, ZhaoPinGonGao


class JobInfoSpider(scrapy.spiders.Spider):

    name = "jobinfo_cug"
    allowed_domains = ["cug.91wllm.com"]
    start_urls = [
        "http://cug.91wllm.com"
    ]
    # 爬取时间：当前时间和下一个月的时间
    dates = [datetime.now(), datetime.now()+relativedelta(months=1)]

    def parse(self, response):
        # print(response, type(response))
        # print(response.body_as_unicode())
        # 招聘公告信息
        zpggs = response.xpath('//div[@class="tabs tab2"]/ul[@id="tabs-23"]/li').extract()
        for zpgg in zpggs:
            url = self.start_urls[0] + Selector(text=zpgg).xpath('//li/a/@href').extract_first()
            name = Selector(text=zpgg).xpath('//li/a/text()').extract_first()
            date = Selector(text=zpgg).xpath('//li/span/text()').extract_first()
            zhaoPinGonGao = ZhaoPinGonGao()
            zhaoPinGonGao['schoolNo'] = 1
            zhaoPinGonGao['name'] = name
            zhaoPinGonGao['date'] = date
            zhaoPinGonGao['url'] = url
            yield scrapy.Request(url, meta={'item': zhaoPinGonGao}, callback=self.get_detail_zpgg)

        for date in self.dates:
            year = date.year
            month = date.month
            yield scrapy.FormRequest(
                url="http://cug.91wllm.com/default/date",
                formdata={'year': str(year), 'month': str(month)},
                callback=self.after_post
            )

    # 招聘公告详情页
    def get_detail_zpgg(self, response):
        item = response.meta['item']
        # 提取公司信息的Dom
        keys1 = response.xpath('//div/ul[@class="xInfo"]/li/text()').extract()
        values1 = response.xpath('//div/ul[@class="xInfo"]/li/span/text()').extract()
        dom1 = {}
        if len(keys1)>0:
            for i in range(0, len(keys1)):
                dom1[keys1[i]] = values1[i]
        item["companyInfoDom"] = dom1
        # 工作信息的Dom
        keys2 = response.xpath('//div/ul[@class="xInfo xInfo-2 cl"]/li/text()').extract()
        values2 = response.xpath('//div/ul[@class="xInfo xInfo-2 cl"]/li/span/text()').extract()
        dom2 = {}
        if len(keys2)>0:
            for i in range(0, len(keys2)):
                dom2[keys2[i]] = values2[i]
        item["workInfoDom"] = dom2
        # print response.xpath('//div/h1/text()').extract_first(), item["companyInfoDom"], item["workInfoDom"]
        # 存储包含职位信息的Dom的List，解析table
        tableinfos = response.xpath('//table/tr').extract()
        list = []
        if len(tableinfos)>0:
            columns = Selector(text=tableinfos[0]).xpath("//tr/td/text()").extract()
            for i in range(1, len(tableinfos)):
                dom = {}
                tdvalues = Selector(text=tableinfos[i]).xpath("//tr/td/text()").extract()
                avalues = Selector(text=tableinfos[i]).xpath("//tr/td/a/text()").extract()
                dom[columns[0]] = tdvalues[0]
                dom[columns[1]] = avalues[0]
                dom[columns[2]] = tdvalues[1]
                dom[columns[3]] = tdvalues[2]
                dom[columns[4]] = tdvalues[3]
                dom[columns[5]] = tdvalues[4]
                list.append(dom)
        item["jobDomList"] = list
        # print item["jobDomList"]
        html = response.xpath('//div[@id="vTab2"]').extract_first()
        item["detail"] = html

        yield item

    # 处理post请求后返回的数据
    def after_post(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        for date in self.dates:
            year = date.year
            month = date.month
            for dd in range(1, 32):
                ymd = str(year) + '-' + str(month) + '-' + str(dd)
                if jsonresponse.has_key(ymd):
                    urlselector = Selector(text=jsonresponse[ymd]).xpath('//li/a/@href').extract()
                    li_text = Selector(text=jsonresponse[ymd]).xpath('//li/text()').extract()
                    a_text = Selector(text=jsonresponse[ymd]).xpath('//li/a/text()').extract()
                    for url in urlselector:
                        i = 0
                        if li_text[i] == u"宣讲会：" :
                            campusTalkItem = CampusTalkItem()
                            campusTalkItem['date'] = ymd
                            campusTalkItem['name'] = a_text[i]
                            campusTalkItem['schoolNo'] = 1
                            href = self.start_urls[0] + url
                            campusTalkItem["url"] = href
                            i += 1
                            # print jsonresponse['2017-3-25']
                            # print href + ' month:' + str(month)
                            yield scrapy.Request(href, meta={'item': campusTalkItem}, callback=self.get_detail_xjh)
                        else:
                            shuangXuanHui = ShuangXuanHui()
                            shuangXuanHui['date'] = ymd
                            shuangXuanHui['name'] = a_text[i]
                            shuangXuanHui['schoolNo'] = 1
                            href = self.start_urls[0] + url
                            shuangXuanHui["url"] = href
                            i += 1
                            yield scrapy.Request(href, meta={'item': shuangXuanHui}, callback=self.get_detail_sx)

    # 继续解析post请求时得到的公司具体信息的地址,处理宣讲会详细信息
    def get_detail_xjh(self, response):
        item = response.meta['item']
        # 提取公司信息的Dom
        keys1 = response.xpath('//div/ul[@class="xInfo xInfo-2"]/li/text()').extract()
        values1 = response.xpath('//div/ul[@class="xInfo xInfo-2"]/li/span/text()').extract()
        dom1 = {}
        if len(keys1) > 0:
            for i in range(0, len(keys1)):
                dom1[keys1[i]] = values1[i]
        item["companyInfoDom"] = dom1
        # 工作信息的Dom
        keys2 = response.xpath('//div/ul[@class="xInfo xInfo-2 cl tInfo-2"]/li/text()').extract()
        values2 = response.xpath('//div/ul[@class="xInfo xInfo-2 cl tInfo-2"]/li/span/text()').extract()
        dom2 = {}
        # if len(keys2) == 14:
        #     for i in range(0,14):
        #         print i, keys2[i]
        #     # for i in range(0,12):
        #     #     print i, values2[i]
        #     print "-------------------------"
        if len(keys2) > 0:
            # print len(keys2), len(values2), item["url"]
            if len(keys2) == len(values2):
                for i in range(0, len(keys2)):
                    dom2[keys2[i]] = values2[i]
            # 当key，value的个数不等时，表结构发生特殊变化，需要特殊处理
            elif len(keys2) == 14:
                for i in range(0,4):
                    dom2[keys2[i]] = values2[i]
                dom2[keys2[4]] = values2[4]+" "+values2[5]
                dom2[keys2[7]] = values2[6]
                dom2[keys2[8]] = values2[7]+" "+values2[8]
                for i in range(11,14):
                    dom2[keys2[i]] = values2[i-2]
            elif len(keys2) == 12:
                for i in range(0,4):
                    dom2[keys2[i]] = values2[i]
                dom2[keys2[4]] = values2[4] + " " + values2[5]
                for i in range(7,10):
                    dom2[keys2[i]] = values2[i-1]
        item["workInfoDom"] = dom2
        # 宣讲会详情,直接存html
        html1 = response.xpath('//div[@id="vTab1"]').extract_first()
        item["detail"] = html1
        # 公司简介, 直接存html
        html2 = response.xpath('//div[@class="vContent cl"]').extract_first()
        item["introduction"] = html2
        # 存储包含职位信息的Dom的List，解析table
        tableinfos = response.xpath('//table/tr').extract()
        list = []
        if len(tableinfos) > 0:
            columns = Selector(text=tableinfos[0]).xpath("//tr/td/text()").extract()
            for i in range(1, len(tableinfos)):
                dom = {}
                tdvalues = Selector(text=tableinfos[i]).xpath("//tr/td/text()").extract()
                avalues = Selector(text=tableinfos[i]).xpath("//tr/td/a/text()").extract()
                dom[columns[0]] = tdvalues[0]
                dom[columns[1]] = avalues[0]
                dom[columns[2]] = tdvalues[1]
                dom[columns[3]] = tdvalues[2]
                list.append(dom)
        item["jobDomList"] = list
        # print response.xpath('//title/text()').extract_first(), item['date']
        yield item

    # 继续解析post请求时得到的公司具体信息的地址,处理双选会详细信息
    def get_detail_sx(self, response):
        item = response.meta['item']
        # 提取公司信息的Dom
        keys1 = response.xpath('//div/ul[@class="xInfo xInfo-2 cl tInfo-2"]/li/text()').extract()
        values1 = response.xpath('//div/ul[@class="xInfo xInfo-2 cl tInfo-2"]/li/span/text()').extract()
        dom1 = {}
        if len(keys1) > 0:
            for i in range(0, len(keys1)):
                dom1[keys1[i]] = values1[i]
        item["zphInfoDom"] = dom1
        # 双选会详情,直接存html
        html1 = response.xpath('//div[@id="vTab1"]').extract_first()
        item["detail"] = html1
        # 存储包含职位信息的Dom的List，解析table
        tableinfos = response.xpath('//table/tr').extract()
        list = []
        if len(tableinfos) > 0:
            columns = Selector(text=tableinfos[0]).xpath("//tr/td/b/text()").extract()
            for i in range(1, len(tableinfos)):
                dom = {}
                tdvalues = Selector(text=tableinfos[i]).xpath("//tr/td/text()").extract()
                avalues = Selector(text=tableinfos[i]).xpath("//tr/td/a/text()").extract()
                dom[columns[0]] = tdvalues[0]
                dom[columns[1]] = avalues[0]
                dom[columns[2]] = tdvalues[1]
                dom[columns[3]] = tdvalues[2]
                list.append(dom)
        item["companyDomList"] = list
        yield item
        # print response.xpath('//title/text()').extract_first(), item['date']
        # pass