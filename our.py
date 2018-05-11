import logging
import urllib

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from time import sleep
import pymongo

brower = webdriver.Chrome()
wait = ui.WebDriverWait(brower,10)
URL = 'https://movie.douban.com/'
username = '豆瓣账号'
password = '豆瓣密码'
movie = '后来的我们‎'

# 创建数据库
client = pymongo.MongoClient('localhost',27017)
next_our = client['next_our']
comments = next_our['comments']



# 登录
def login(url,username,password):
    brower.get(url)
    brower.find_element_by_css_selector('[class="nav-login"]').click()
    name = brower.find_element_by_id('email')
    name.clear()
    name.send_keys(username)
    pwd = brower.find_element_by_id('password')
    pwd.clear()
    pwd.send_keys(password)
    pic_src = brower.find_element_by_id('captcha_image').get_attribute('src')
    cap_value = get_yzm(pic_src)
    yan_zheng_ma = brower.find_element_by_id('captcha_field')
    yan_zheng_ma.clear()
    yan_zheng_ma.send_keys(cap_value)
    brower.find_element_by_css_selector('[class="btn-submit"]').click()
    print('登陆成功')


# 获取验证码
def get_yzm(src):
    print("正在保存验证码图片")
    captchapicfile = "D:/pycharm/PycharmProjects/next_our/captcha.png"
    urllib.request.urlretrieve(src, filename=captchapicfile)
    print("打开图片文件，查看验证码，输入单词......")
    captcha_value = input()
    print(captcha_value)
    return captcha_value

# 搜索电影
def seach(movie_name):
    inp_query = brower.find_element_by_id('inp-query')
    inp_query.clear()
    inp_query.send_keys(movie_name)
    submit = brower.find_element_by_css_selector('[type="submit"]')
    submit.click()
    sleep(1)
    brower.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[1]/a').click()
    logging.info("进入详情页")

# 进入短评列表
def into_comment():
    brower.find_element_by_xpath('//*[@id="comments-section"]/div[1]/h2/span/a').click()
    logging.info("进入短评列表")

# 获取短评
def get_comment():
    wait.until(lambda brower : brower.find_element_by_css_selector('[class="next"]'))
    sleep(1)
    for i in range(1,21):
        comment = brower.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/p'.format(str(i))).text
        comment_name = brower.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/a'.format(str(i))).text
        votes = brower.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[1]/span'.format(str(i))).text
        data = {
            'comment': comment,
            'comment_name': comment_name,
            'votes': int(votes)
        }
        comments.insert_one(data)
        print('*'*100)
        print(data)
        logging.info('成功存入数据库')

# 进入下一页
def next_page():
    next = brower.find_element_by_css_selector('[class="next"]')
    try:
        next.click()
    except:
        logging.info("全部完成了")

if __name__=="__main__":
    login(URL,username,password)
    seach(movie)
    into_comment()
    for page in range(24):
        get_comment()
        next_page()


