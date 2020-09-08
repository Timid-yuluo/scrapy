# -*- coding: utf-8 -*-
import scrapy
from urllib import request
from PIL import Image

class PoetrySpider(scrapy.Spider):
    name = 'poetry'
    # 限制网页范围
    # allowed_domains = ['gushiwen.org']
    start_urls = ['https://so.gushiwen.org/user/login.aspx']
    # 登录页网址
    login_url = 'https://so.gushiwen.org/user/login.aspx'

    def parse(self, response):
        formdata = {
        '__VIEWSTATE': 'ygGjY8wotCrjfJdqYogosmC + k1ahJE1y5syK43wZhlqF9pt1atHba8smIRmgDC1S9xGhpuN + sSWqdp3tXa/kTsS3e2gVuaItugPlGkQ4W4DkaHqSaHwBYV7l3a0 =',
        '__VIEWSTATEGENERATOR': 'C93BE1AE',
        # 登陆后跳转的网页
        'from': 'http://so.gushiwen.org/user/collect.aspx',
        'email': '2744255833@qq.com',
        'pwd': '2744255833aa',
        'denglu': '登录',
        # 识别后手动输入
        # 'code': c4m6
        }
        # 获取验证码的url（只能获得域名）
        captcha_img = response.xpath('//*[@id="imgCode"]/@src').get()
        # 拼接获得完整的验证码url
        captcha_img = 'https://so.gushiwen.org/' + captcha_img
        print(captcha_img)
        # 调用regonize_captcha函数，把captcha_img传入
        captcha = self.regonize_captcha(captcha_img)
        print(captcha, '='*30)
        # 把验证码传入formdata
        formdata['code'] = captcha
        print(formdata, '='*30)
        # 携带参数请求网址，回调给函数parse_after_login
        yield scrapy.FormRequest(url=self.login_url, formdata=formdata, callback=self.parse_after_login)

    def parse_after_login(self, response):
        # 判断是否登陆成功
        if response.url == 'https://so.gushiwen.org/user/collect.aspx':
            print('登录成功')
        else:
            print('登陆失败')

    def regonize_captcha(self, image_url):
        request.urlretrieve(image_url, 'captcha.png')
        image = Image.open('captcha.png')
        image.show()
        captcha = input("请输入验证码>>>: ")
        return  captcha