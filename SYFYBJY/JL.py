import os
import re
import time
import urllib
from datetime import datetime
from urllib import request, parse
from lxml import html
from urllib.parse import quote
import _thread
from multiprocessing import Process
import smtplib
import urllib
from email.header import Header
from datetime import datetime
from email.mime.text import MIMEText

# 公共请求头需要自行抓包重新填写Cookie
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 '
                  'Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63030532)',
    'Host': 'sych.xiaoerfang.cn',
    "Cookie": "_csrf=9133752109ef502c887da9c6ced273f981a89aeee34932eb33f7156eed9389fda%3A2%3A%7Bi%3A0%3Bs%3A5%3A"
              "%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22MsQiC1t36K_kE5oRksbquHFUmZapKS00%22%3B%7D; "
              "PHPSESSID=fesorlm206odi5qbg6nhuki0sm; "
              "_identity=7d042ddbddc61566b1a8bfc98321906b4af3d0a8da2737e9ce55cfa90c0b9cf4a%3A2%3A%7Bi%3A0%3Bs%3A9%3A"
              "%22_identity%22%3Bi%3A1%3Bs%3A53%3A%22%5B%22433796%22%2C%22sBETxTqvITVgM7jcZJCL9_BBjfK76_eh%22"
              "%2C2592000%5D%22%3B%7D",
}
# 九价疫苗余量日期查询URL
dataurl = "https://sych.xiaoerfang.cn/sychwx/index.php?r=source%2Flist&specCode=442&specName=%E7%96%AB%E8%8B%97%E6%8E%A5%E7%A7%8D%E9%97%A8%E8%AF%8A&deptType=0&oneDeptId=285&twoDeptId=442&visitDate="
# 构造POST请求的默认接口
posturl = "https://sych.xiaoerfang.cn/sychwx/index.php?r=source%2Finfo"
# 九价疫苗默认CSRF获取URL
csrfurl = "https://sych.xiaoerfang.cn/sychwx/index.php?r=source%2Findex&deptId=442&twoDeptName=%E7%96%AB%E8%8B%97%E6" \
          "%8E%A5%E7%A7%8D%E9%97%A8%E8%AF%8A&deptType=0&oneDeptId=285&oneDeptName=%E5%A6%87%E5%A5%B3%E5%81%A5%E5%BA" \
          "%B7%E4%BF%9D%E5%81%A5%E4%B8%AD%E5%BF%83"
# 九价疫苗预约日期对应的specCode
global_specCode = []
# 九价疫苗预约日期对应的specName
global_specName = []
# 九价疫苗预约日期对应的regToken
# 0:上午 1：下午 2：晚上
global_regToken = []
# 九价疫苗预约日期对应的medFee
global_medFee = []
# 九价疫苗预约日期对应的csrf
csrf = ""
# 日期格式1
data1 = "2021-11-24"
# 日期格式2
data2 = "20211124"
# 时间格式1
time1 = "09:30"
# 时间格式2
time2 = "10:00"
# 选择上午（0）或者下午（1）
ap = 0
# 收件提醒邮箱
inbox = "xxxxxx@163.com"

# 日志记录
def wrLog(str2):
    dt = datetime.now()
    str1 = dt.strftime('%Y-%m-%d %H:%M:%S %f')
    str1 = str1 + "  " + str2 + "\n"
    with open('log.txt', 'a') as f:
        f.writelines(str1)


# 获取csrf_token为预定做准备
def getcsrf():
    global csrf, csrfurl
    data = ""
    try:
        if os.path.exists("csrf.html"):
            print("File csrf.html already exist!")
            with open('csrf.html', 'r') as f:
                data = f.read()
            searchObj = re.search(r'var _csrf = "(.*)"', data, re.M | re.I)
            csrf = searchObj.group(1)
            wrLog("成功获取csrf_token")
            print("成功获取csrf_token")
            print(csrf)
            return
        else:
            req = request.Request(url=csrfurl, headers=headers, method='GET')
            response = request.urlopen(req)
            data = response.read().decode('utf-8')
            searchObj = re.search(r'var _csrf = "(.*)"', data, re.M | re.I)
            csrf = searchObj.group(1)
            if csrf != "":
                with open('csrf.html', 'w') as f:
                    f.writelines(data)
            wrLog("成功获取csrf_token")
            print("成功获取csrf_token")
            print(csrf)
            return
    except:
        wrLog("获取失败csrf_token")
        print("获取失败csrf_token")


def regTokenHTML(specname="宫颈癌九价疫苗门诊", url=dataurl):
    try:
        getcsrf()
    except:
        return
    try:
        url = url + data1
        req = request.Request(url=url, headers=headers, method='GET')
        response = request.urlopen(req)
        data = response.read().decode('utf-8')
        selector = html.etree.HTML(data)
        # 解析获得specCode和specName
        xpathstr = "//div[@specname=\"" + specname + "\"]/@"
        specCode = selector.xpath(xpathstr + "speccode")
        if specCode != []:
            with open('regToken.html', 'w') as f:
                f.writelines(data)
        else:
            return
    except:
        return


# 获取展开内容的URL提取时间等参数
def expand(specname="宫颈癌九价疫苗门诊", url=dataurl):
    global global_regToken, global_medFee, global_specCode, global_specName, data1, data2
    data = ""
    try:
        try:
            if os.path.exists("csrf.html"):
                print("File csrf.html already exist!")
                with open('csrf.html', 'r') as f:
                    data = f.read()
                searchObj = re.search(r'var _csrf = "(.*)"', data, re.M | re.I)
                csrf = searchObj.group(1)
                wrLog("成功获取csrf_token")
                print("成功获取csrf_token")
                print(csrf)
            else:
                return 0
        except:
            return 0
        # 若已经获得regToken.html直接读取本地文件掠过一步
        if os.path.exists("regToken.html"):
            print("File regToken.html already exist!")
            with open('regToken.html', 'r') as f:
                data = f.read()
        else:
            return 0
        selector = html.etree.HTML(data)
        # 解析获得specCode和specName
        xpathstr = "//div[@specname=\"" + specname + "\"]/@"
        specCode = selector.xpath(xpathstr + "speccode")
        if specCode != []:
            specName = selector.xpath(xpathstr + "specname")
            index = 0
            for i in specName:
                specName[index] = quote(i, 'utf-8')
                index = index + 1
            medFee = selector.xpath(xpathstr + "medfee")
            regToken = selector.xpath(xpathstr + "regtoken")
            visitTimeName = selector.xpath(xpathstr + "visittimename")
            # 全局变量赋值
            global_regToken = regToken
            global_medFee = medFee
            global_specCode = specCode
            global_specName = specName
            # specCode = 1236
            # medFee = 50
            print("specCode", specCode)
            print("specName", specName)
            print("medFee", medFee)
            print("regToken", regToken)
            print("visitTimeName", visitTimeName)
            wrLog("成功获取regToken")
            print("成功获取regToken")
            return 1
        else:
            wrLog("获取regToken失败")
            print("获取regToken失败")
            return 0
    except:
        wrLog("获取regToken失败")
        print("获取regToken失败")
        return 0


# 获取预约的POST信息反馈
def postpack(posturl=posturl):
    global global_regToken, global_medFee, csrf, global_specCode, data2, time1, time2
    global ap
    try:
        # 需要两次request
        getcsrf()
        data = ""
        if csrf == "":
            return data
        # 这里的speccode与时间有关，标明时间
        # deptId填的是大部门名号
        # deptName就诊科室
        # specName就诊专家
        # 1236 442
        d = {'deptId': '442',
             'deptName': '疫苗接种门诊',
             'specName': '宫颈癌九价疫苗门诊',
             'specCode': global_specCode[ap],
             'medFee': global_medFee[ap],
             'visitDate': data2,
             'regToken': global_regToken[ap],
             'startTime': time1,
             'endTime': time2,
             'doctorCode': '',
             'doctorName': '',
             'doctorFlag': '',
             '_csrf': csrf
             }
        data = bytes(urllib.parse.urlencode(d), encoding='utf8')
        # 需要三次request
        req = request.Request(url=posturl, headers=headers, data=data)
        response = request.urlopen(req)
        date = response.read().decode('utf-8')
        if date == "":
            return 0
        else:
            with open('post.html', 'w') as f:
                f.writelines(date)
            return date
    except:
        return 0


def FuckYou(date):
    global csrf, global_regToken, global_specCode, data2, time1, time2
    global ap
    try:
        #
        url = "https://sych.xiaoerfang.cn/sychwx/index.php?"
        r = "pool/reg2"
        _csrf = csrf
        searchObj = re.search(r'PutRegForm\[ptId\]\\" value=\\"(.*?)\\">', date, re.M | re.I)
        PutRegForm_ptId = searchObj.group(1)
        PutRegForm_visitingDate = data2
        PutRegForm_doctorName = ""
        PutRegForm_deptId = "442"
        # 指明是九价苗
        PutRegForm_deptName = "%E7%96%AB%E8%8B%97%E6%8E%A5%E7%A7%8D%E9%97%A8%E8%AF%8A"
        PutRegForm_specCode = global_specCode[ap]
        PutRegForm_specName = ""
        searchObj = re.search(r'PutRegForm\[orderChannel\]\\" value=\\"(.*?)\\">', date, re.M | re.I)
        PutRegForm_orderChannel = searchObj.group(1)
        PutRegForm_regToken = global_regToken[ap]
        PutRegForm_doctorCode = ""
        PutRegForm_startTime = time1
        PutRegForm_endTime = time2
        PutRegForm_doctorFlag = ""
        PutRegForm_doctorName = ""
        PutRegForm_doctorCode = ""

        url = url + "r=" + r
        url = url + "&_csrf=" + _csrf
        url = url + "&PutRegForm[ptId]=" + PutRegForm_ptId
        url = url + "&PutRegForm[visitingDate]=" + PutRegForm_visitingDate
        url = url + "&PutRegForm[doctorName]=" + quote(PutRegForm_doctorName, 'utf-8')
        url = url + "&PutRegForm[deptId]=" + PutRegForm_deptId
        url = url + "&PutRegForm[deptName]=" + PutRegForm_deptName
        url = url + "&PutRegForm[specCode]=" + PutRegForm_specCode
        url = url + "&PutRegForm[specName]=" + PutRegForm_specName
        url = url + "&PutRegForm[orderChannel]=" + PutRegForm_orderChannel
        url = url + "&PutRegForm[regToken]=" + PutRegForm_regToken
        url = url + "&PutRegForm[doctorCode]=" + PutRegForm_doctorCode
        url = url + "&PutRegForm[startTime]=" + PutRegForm_startTime
        url = url + "&PutRegForm[endTime]=" + PutRegForm_endTime
        url = url + "&PutRegForm[doctorFlag]=" + "&PutRegForm[doctorName]=" + "&PutRegForm[doctorCode]="
        # 需要四次request
        req = request.Request(url=url, headers=headers, method='GET')
        response = request.urlopen(req)
        data = response.read().decode('utf-8')
        print(data)
        if data == "":
            with open('fuck.html', 'w') as f:
                f.writelines(data)
            return 0
        else:
            with open('fuck.html', 'w') as f:
                f.writelines(data)
            return data
    except:
        return 0


def multiT():
    res = ""
    while True:
        dt = datetime.now()
        str1 = dt.strftime('%Y-%m-%d %H:%M:%S %f')
        res = expand(specname="宫颈癌九价疫苗门诊", url=dataurl)
        if res != 0:
            str1 = str1 + "  " + "获取展开连接成功"
            print(str1)
            wrLog("获取展开连接成功")
            print(res)
            break
        else:
            str1 = str1 + "  " + "获取展开连接失败"
            print(str1)
            wrLog("获取展开连接成功")
            continue

    while True:
        dt = datetime.now()
        str1 = dt.strftime('%Y-%m-%d %H:%M:%S %f')
        res = postpack(posturl)
        if res != 0:
            str1 = str1 + "  " + "POST成功"
            print(str1)
            wrLog("POST成功")
            print(res)
            break
        else:
            str1 = str1 + "  " + "POST失败"
            print(str1)
            wrLog("POST失败")
            continue

    while True:
        dt = datetime.now()
        str1 = dt.strftime('%Y-%m-%d %H:%M:%S %f')
        res = FuckYou(res)
        if res != 0:
            str1 = str1 + "  " + "FUCK成功"
            print(str1)
            wrLog("FUCK成功")
            print(res)
            break
        else:
            str1 = str1 + "  " + "FUCK失败"
            print(str1)
            wrLog("FUCK失败")
            continue


def multiP(t1, t2, app):
    # 初始化时间参数
    global time1, time2, ap
    time1 = t1
    time2 = t2
    ap = app
    print("time1: ", time1, "time2: ", time2, "ap: ", ap)
    try:
        # 创建四个线程
        _thread.start_new_thread(multiT, ())
        _thread.start_new_thread(multiT, ())
        _thread.start_new_thread(multiT, ())
        _thread.start_new_thread(multiT, ())
    except:
        print("Error: 无法启动线程")
    while 1:
        pass


def regTokenHTMLP():
    while True:
        regTokenHTML(specname="宫颈癌九价疫苗门诊", url=dataurl)


def init():
    global headers
    data = ""
    if os.path.exists("cookie"):
        print("File cookie already exist!")
        with open('cookie', 'r') as f:
            data = f.read()
        headers['Cookie'] = data
    print(headers)

# 生成当天日期后七天的格式化日期
def getDay():
    ToDay = time.strftime("%Y-%m-%d", time.localtime())
    arg1 = ToDay[:8]
    arg2 = ToDay[8:10]
    index = 0
    list = []
    while index < 8:
        num = int(arg2)
        num = num + index
        num = str(num).zfill(2)
        arg = arg1 + num
        list.append(arg)
        # print(arg)
        index = index + 1
    return list


# 邮件发送提醒服务
def mail(inbox, data):
    dt = datetime.now()
    str1 = dt.strftime('%Y-%m-%d %H:%M:%S %f')
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = 'xxxxx@qq.com'
    password = 'xxxxxxx'
    # 收信方邮箱
    to_addr = inbox
    # 发信服务器
    smtp_server = 'smtp.qq.com'
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(str1 + " send by HPV-Hijack ", 'plain', 'utf-8')
    # 邮件头信息
    msg['From'] = Header('HPV-Hijack')
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header(data)
    try:
        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server, 465)
        # 登录发信邮箱
        server.login(from_addr, password)
        # 发送邮件
        server.sendmail(from_addr, to_addr, msg.as_string())
        # 关闭服务器
        server.quit()
        str1 = "邮件发送成功 发送地址邮箱地址为： " + to_addr
        wrLog(str1)
    except smtplib.SMTPException:
        str1 = "Error: 无法发送邮件 " + to_addr
        wrLog(str1)


# 检查票务状态
def checkNumber(url=dataurl, headers=headers):
    list = getDay()
    for i in list:
        dayurl = url + i
        try:
            req = request.Request(url=dayurl, headers=headers, method='GET')
            # req = proxiesrequest(dayurl, headers, 'GET')
            wrLog("抓取URL：" + dayurl + "成功")
        except:
            wrLog("抓取URL：" + dayurl + "失败")
            continue
        response = request.urlopen(req)
        # time.sleep(0.1)
        data = response.read().decode('utf-8')
        selector = html.etree.HTML(data)
        # 抓取时间分布
        title = selector.xpath(
            '//*[@id="collapse3"]/div[@class="weui-media-box__bd item-detail"]/div[@class="weui-cell"]/div['
            '@class="weui-cell__bd"]/table[@class="cell__bd_td"]/tr/td/p/text()')
        dt = datetime.now()
        str1 = dt.strftime('%Y-%m-%d %H:%M:%S %f')
        time.sleep(0.1)
        if title == []:
            print(str1 + i + "当天无号")
            wrLog(i + "当天无号")
            continue
        # print(title)
        # 抓取号码状态
        state = selector.xpath(
            '//*[@id="collapse3"]/div[@class="weui-media-box__bd item-detail"]/div[@class="weui-cell"]/div['
            '@class="weui-cell__bd"]/table[@class="cell__bd_td"]/tr/td/p/span/text()')
        # print(state)
        index = 0
        for j in title:
            title[index] = j[:2]
            index = index + 1
        # print(title)
        index = 0
        for k in state:
            str = i + " " + title[index] + " " + state[index]
            #print(title[index])
            #print(state[index])
            if state[index] != "约满" and state[index] != "无号":
                print(str1 + "当天有号")
                print(str)
                mail(inbox, str)
                return i
            else:
                print(str1 + i + "当天无号")
            index = index + 1
    return 0

def main1():
    init()
    # 创建获取regToken
    p1 = Process(target=regTokenHTMLP, args=(), kwargs={})
    # 创建上午约号进程
    t1 = "09:30"
    t2 = "10:00"
    app = 0
    am930 = Process(target=multiP, args=(t1, t2, app,), kwargs={})
    t1 = "10:00"
    t2 = "10:30"
    am10 = Process(target=multiP, args=(t1, t2, app,), kwargs={})
    t1 = "10:30"
    t2 = "11:00"
    am1030 = Process(target=multiP, args=(t1, t2, app,), kwargs={})
    t1 = "11:00"
    t2 = "11:30"
    am110 = Process(target=multiP, args=(t1, t2, app,), kwargs={})
    t1 = "11:30"
    t2 = "12:00"
    am1130 = Process(target=multiP, args=(t1, t2, app,), kwargs={})
    # 创建下午约号进程
    t1 = "13:00"
    t2 = "13:30"
    app = 1
    pm130 = Process(target=multiP, args=(t1, t2, app,), kwargs={})
    t1 = "13:30"
    t2 = "14:00"
    pm1330 = Process(target=multiP, args=(t1, t2, app,), kwargs={})
    t1 = "14:00"
    t2 = "14:30"
    pm140 = Process(target=multiP, args=(t1, t2, app,), kwargs={})

    p1.start()  # 开启第一个进程
    #time.sleep(0.5)
    am930.start()  # 开启第二个进程
    #time.sleep(0.5)
    am10.start()
    #time.sleep(0.5)
    am1030.start()
    #time.sleep(0.5)
    am110.start()
    #time.sleep(0.5)
    am1130.start()
    #time.sleep(0.5)
    pm130.start()
    #time.sleep(0.5)
    pm1330.start()
    #time.sleep(0.5)
    pm140.start()

def main2():
    global data1, data2
    while True:
        time.sleep(1)
        try:
            res = checkNumber(url=dataurl, headers=headers)
            if res != 0:
                data1 = res
                tmp = ""
                for i in range(0, len(res)):
                    if i != 4 and i != 7:
                        tmp = tmp + res[i]
                data2 = tmp
                break
        except:
            continue
    return
if __name__ == '__main__':
    main2()
    main1()

