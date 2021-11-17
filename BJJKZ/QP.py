import os
import re
import time
import urllib
from urllib import request, parse
from lxml import html
from urllib.parse import quote
import _thread
from multiprocessing import Process

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 '
                  'Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63030532)',
    'Host': 'weixin.gycode.com',
    "Cookie": "PHPSESSID=5ain46aoi7q8rbpavv8k2uh240; oauth2_etyscl1632878633=%7B%22wap_token%22%3A%22etyscl1632878633"
              "%22%2C%22wecha_id%22%3A%22oi-MHwzdGuUq9tkWinhIOq2UaeDY%22%2C%22appid%22%3A%22wxbbdfb146fd90745a%22%7D; "
              "UM_distinctid=17d10095c3944-0b6243059f3caf-61263e23-144000-17d10095c3a16a; "
              "CNZZDATA1254401729=1081976128-1636644555-%7C1636656075",
}
#23524
def fuck():
    id = 23524
    dae = []
    for i in range(23524):
        tmp = id + i
        url = "http://weixin.gycode.com/index.php?g=Wap&m=Custom&a=index&token=etyscl1632878633&id=" + str(tmp) + "&v=2271"
        dae.append(url)
    print(dae)
    for url in dae:
        #print(url)
        try:
            #url = "http://weixin.gycode.com/index.php?g=Wap&m=Custom&a=index&token=etyscl1632878633&id=" + str(id) + "&v=2271"
            #print(url)
            req = request.Request(url=url, headers=headers, method='GET')
            response = request.urlopen(req)
            data = response.read().decode('utf-8')
            selector = html.etree.HTML(data)
            # 解析获得specCode和specName
            xpathstr = "//*[@id=\"form\"]/input/@value"
            #print(xpathstr)
            specCode = selector.xpath(xpathstr)[0]
            #print(specCode)
            # print(data)
            d = {'oz79a1_22722': 'xxx', #姓名
                 'a3gxt_22722': '女',   #性别
                 'godpns_22722': 'xx',  #年龄
                 'xfj8w_22722': "xxxxx", #身份证号
                 'kdp3k_22722': "xxxxx", #电话号码
                 'i27u5_22722': "九价人乳头瘤病毒疫苗（美国-默沙东）",
                 'sexpcf_22722': "无",
                 'ya1k5j_22722': "否",
                 'ktupp_22722': "否",
                 'xwqjrn_22722': '无',
                 'k1h00b_22722': '否',
                 'etkyqq_22722': '无',
                 'a8opc_22722': '无',
                 '47nwab_22722[]': '无',
                 'd5vlm9_22722': '第一针',
                 'zyql08_22805': '2021年11月18日上午8：00- 11:00',  #具体时间
                 'ch9nhi_22807': '本人已知',
                 '__hash__': specCode,
                 }
            #print(d)
            data = bytes(urllib.parse.urlencode(d), encoding='utf8')
            req = request.Request(url=url, headers=headers, data=data)
            response = request.urlopen(req)
            date = response.read().decode('utf-8')
            #print(date)
        except:
            return

if __name__ == '__main__':
    while True:
        time.sleep(0.1)
        fuck()
    #fuck()