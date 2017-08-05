

#! -*- coding:utf-8 -*-
# 本模块用来离线下载资源到网盘
import urllib.request
import urllib.parse
import json
import execjs

class bdsaver:
    def __init__(self,cookie):
        self.cookie = cookie
        self.headers = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://pan.baidu.com/',
            'Cookie': self.cookie,
            'Connection': 'keep-alive'
        }

    # 登录需要POST一个包，其中包含帐号信息的Cookie
    def login(self):
        self.loginurl="http://pan.baidu.com/disk/home"
        try:
            req = urllib.request.Request(self.loginurl, headers=self.headers)
            sourcecode = urllib.request.urlopen(req)
        except Exception as e:
            print('Error ', str(e))
        else:
            #如果出现该字眼说明登录成功
            htmlcode=(sourcecode.read().decode())
            print(htmlcode)
            if(htmlcode.find('initPrefetch')!=-1):
                print('OK!')
    def query(self,magneturl):
        self.magneturl=magneturl
        self.headers = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://pan.baidu.com/disk/home?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0',
            'Cookie': self.cookie,
            'Connection': 'keep-alive',
            'Pragma': 'no - cache',
            'Cache - Control': 'no - cache',
        }

        self.queryurl = 'http://pan.baidu.com/rest/2.0/services/cloud_dl?channel=chunlei&web=1&app_id=250528&clienttype=0'
        self.data ={
            'method': 'query_magnetinfo',
            'app_id': '250528',
            'source_url':self.magneturl ,
            'save_path': '/',
            'type': '4'
        }
        req = urllib.request.Request(self.queryurl, headers=self.headers, data=urllib.parse.urlencode(self.data).encode(encoding='UTF8') )
        sourcecode = urllib.request.urlopen(req)
        result=(sourcecode.read().decode('unicode_escape'))
        print(result)
        result=json.loads(result)['magnet_info']
        download_list=''
        for i in range(len(result)):
            #文件大于50MB
            if (int(result[i]['size'])>1024*1024*50):
                download_list=download_list+str(i+1)+','
        if download_list!='':
            return download_list
        else:
            return '1'
    def save(self,selidx):
        # self.queryurl = 'http://pan.baidu.com/rest/2.0/services/cloud_dl?channel=chunlei&web=1&app_id=250528&bdstoken=efbd0c8c5eb658ea804bea857c9ad213&clienttype=0'
        self.queryurl = 'http://pan.baidu.com/rest/2.0/services/cloud_dl?channel=chunlei&web=1&app_id=250528&clienttype=0'
        self.data = {
            'method': 'add_task',
            'app_id': '250528',
            'save_path': '/',
            'selected_idx': selidx,
            'task_from': '1',
            'source_url':self.magneturl ,
            # 't':'1501251100480'
        }
        req = urllib.request.Request(self.queryurl, headers=self.headers,
                                     data=urllib.parse.urlencode(self.data).encode(encoding='UTF8'))
        sourcecode = urllib.request.urlopen(req)
        print(sourcecode.read().decode('unicode_escape'))



if __name__ == '__main__':
    #填入自己截获到的cookies
    bdtest = bdsaver(cookie='')
    bdtest.login()
    dllist=bdtest.query(magneturl='magnet:?xt=urn:btih:459E0DD6DCE56845BE3C72368797481F0B8C0216&xl=3391547763&dn=%E7%94%9F%E5%8C%96%E5%8D%B1%E6%9C%BA%E7%B3%BB%E5%88%97%E4%B8%89%E9%83%A8+%E7%94%9F%E5%8C%964%E9%A2%84%E5%91%8A%E7%89%87')
    bdtest.save(dllist)
