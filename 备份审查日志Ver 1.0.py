import requests
import os

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)  # 消除证书警告
url = 'https://10.220.2.250'
login = '/login.html'
do = '/webui'
g = ['log_uac_export', 'log_uac_export_file', 'main']
log_type = ['webaccess', 'im', 'bbs', 'search_engine', 'mail', 'file_transfer', 'relax_stock', 'other']
date = {
    'year': '',
    'month': '',
    'day': ''
}
ymd = input('请输入需要备份的年月日（格式xxxxxxxx，例如19990208）')
date['year'] = ymd[0:4]
date['month'] = ymd[4:6]
date['day'] = ymd[6:8]

stime = date['year'] + date['month'] + date['day']
etime = date['year'] + date['month'] + date['day']
stime_hour = date['year'] + '-' + date['month'] + '-' + date['day'] + ' 00:00:00'
etime_hour = date['year'] + '-' + date['month'] + '-' + date['day'] + ' 23:59:59'
ttime_hour = date['year'] + '-' + date['month'] + '-' + date['day'] + ' 00:00:00'

dir = ['访问网站日志', 'IM聊天日志', '社区日志', '搜索引擎日志', '邮件日志', '文件传输日志', '娱乐股票日志', '其他日志']
data1 = {
    'g': g[0],
    'log_type': '',
    'stime': stime,
    'etime': etime,
    'stime_hour': stime_hour,
    'etime_hour': etime_hour
}
data2 = {
    'g': g[1],
    'log_type': ''
}

cookie = input('登录网页后，复制cookie值到此处')
cookies = {
    'Name': 'USGSESSID',
    'Value': cookie
}

session = requests.session()
session.cookies.set(cookies['Name'], cookies['Value'])
session.cookies.set('off', '')
headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
    'Referer': '',
    'Host': '10.220.2.250',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
    'Referer': '',
    'Host': '10.220.2.250',
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}
print('开始备份' + date['year'] + '年' + date['month'] + '月' + date['day'] + '日ACG审计日志')
for log, d in zip(log_type, dir):
    print('开始备份' + d)
    data1['log_type'] = log
    data2['log_type'] = log
    headers1['Referer'] = headers2['Referer'] = url + do + '/?g=' + 'log_uac_nbc_' + log + '_show'
    filedir = './' + date['year'] + '年/' + date['month'] + '月/' + date['day'] + '日/' + d
    if os.path.exists(filedir) is False:
        os.makedirs(filedir)
    stime_hour = date['year'] + '-' + date['month'] + '-' + date['day'] + ' 00:00:00'
    c = 0  # 表示没传完
    while c == 0:
        data1['stime_hour'] = stime_hour
        res1 = session.get(url + do, headers=headers1, verify=False, params=data1)
        res2 = session.get(url + do, headers=headers2, verify=False, params=data2)

        if res1.content == b'1':
            c = 1
            ttime_hour = date['year'] + '-' + date['month'] + '-' + date['day'] + ' 23:59:59'
            filenames = stime_hour[11:13] + '：' + stime_hour[14:16]
            filenamee = ttime_hour[11:13] + '：' + ttime_hour[14:16]
            filename = filenames + '-' + filenamee + '.zip'
            with open(filedir + '/' + filename, 'wb') as f:
                f.write(res2.content)
        else:
            c = 0
            ttime_hour = res1.content.decode()[0:19]
            print(ttime_hour)
            filenames = stime_hour[11:13] + '：' + stime_hour[14:16]
            filenamee = ttime_hour[11:13] + '：' + ttime_hour[14:16]
            filename = filenames + '-' + filenamee + '.zip'
            with open(filedir + '/' + filename, 'wb') as f:
                f.write(res2.content)
            stime_hour = ttime_hour
    print('已备份完成' + d)
print('已完成' + date['year'] + '年' + date['month'] + '月' + date['day'] + '日ACG审计日志备份')
