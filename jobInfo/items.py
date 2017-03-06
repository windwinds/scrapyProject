# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 专场宣讲会
class CampusTalkItem(scrapy.Item):
    # define the fields for your item here like:
    schoolNo = scrapy.Field()             # 学校编号

    name = scrapy.Field()            # 公司名称
    address = scrapy.Field()            # 宣讲地点
    date = scrapy.Field()               # 宣讲日期，3字节，日期，格式：2014-09-18

    url = scrapy.Field()                 # 详情页url

    # companyType = scrapy.Field()        # 公司性质
    # industry = scrapy.Field()           # 公司行业
    # size = scrapy.Field()               # 公司规模
    companyInfoDom = scrapy.Field()       # 存储公司信息的Dom，可能包括上面几个字段，mongodb存储结构

    # talkDateTime = scrapy.Field()       # 宣讲时间， 8字节，日期时间，格式：2017-03-03 10:00-12:00
    # school = scrapy.Field()             # 宣讲学校
    # city = scrapy.Field()               # 宣讲城市
    # writeDate = scrapy.Field()          # 笔试日期
    # writeAddress = scrapy.Field()       # 笔试地址
    # interviewTime = scrapy.Field()      # 面试日期
    # interviewAddress = scrapy.Field()   # 面试地址
    # email = scrapy.Field()              # 简历投递邮箱
    # tel = scrapy.Field()                # 招聘部门电话
    workInfoDom = scrapy.Field()          # 存储宣讲信息的Dom，可能包括上面几个字段，mongodb存储结构

    detail = scrapy.Field()             # 宣讲会详情,直接存html
    introduction = scrapy.Field()       # 公司简介,直接存html
    jobDomList = scrapy.Field()    # 存储包含职位信息的Dom的List


# 双选会
class ShuangXuanHui(scrapy.Item):
    schoolNo = scrapy.Field()  # 学校编号

    name = scrapy.Field()               # 双选会名称
    address = scrapy.Field()            # 双选会地点
    date = scrapy.Field()               # 双选会日期

    url = scrapy.Field()                # 详情页url

    # type = scrapy.Field()             # 招聘会类型
    # time = scrapy.Field()             # 举办时间 2017-03-11 09:00
    # city = scrapy.Field()             # 举办城市
    zphInfoDom = scrapy.Field()         # 招聘会信息Dom

    detail = scrapy.Field()             # 详情， 存html
    companyDomList = scrapy.Field()     # 存储参展企业的Dom的List


# 招聘公告
class ZhaoPinGonGao(scrapy.Item):
    schoolNo = scrapy.Field()  # 学校编号

    name = scrapy.Field()              # 招聘名称
    date = scrapy.Field()              # 招聘时间

    url = scrapy.Field()                # 详情页url

    # companyType = scrapy.Field()       # 公司性质
    # linkman = scrapy.Field()           # 联系人
    # industry = scrapy.Field()          # 公司行业
    # tel = scrapy.Field()               # 联系电话
    # size = scrapy.Field()              # 公司规模
    # email = scrapy.Field()             # 简历投递邮箱
    companyInfoDom = scrapy.Field()     # 存储公司信息的Dom，可能包括上面几个字段，mongodb存储结构

    # city = scrapy.Field()              # 工作城市
    # pubtime = scrapy.Field()           # 发布日期
    workInfoDom = scrapy.Field()        # 存储工作信息的Dom，可能包括上面几个字段，mongodb存储结构

    jobDomList = scrapy.Field()           # 存储包含职位信息的Dom的List
    detail = scrapy.Field()            # 详情， 存html


