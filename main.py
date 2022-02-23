import requests
from bs4 import BeautifulSoup
import time
import json

def post_to_slack(text):
    slack_webhook_url = "user-slack-webhook-url"
    headers = { "Content-type": "application/json" }
    data = { "text" : text }
    res = requests.post(slack_webhook_url, headers=headers, data=json.dumps(data))

def new_post_alert(url, selector, category, title_latest):
    req = requests.get(url, verify=False) #경희의대 홈페이지가 verify=False해줘야지 url 접근 가능
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    posts = soup.select_one(selector)
    posts.select_one('span').decompose() #span태그에 '[학사]'이런 태그 붙어있어서 없애버리고 제목만 꺼냄.
    title = posts.text.strip()
    if title != title_latest:
        link = posts.attrs['href'].strip()
        post_to_slack("의대게시판 새글: [" + category + "] " + title)
        post_to_slack("링크: " + link)
    return title

url1 = 'https://khusm.khu.ac.kr/bbs/board.php?bo_table=s6_1&sca=%ED%95%99%EC%82%AC'
url2 = 'https://khusm.khu.ac.kr/bbs/board.php?bo_table=s6_1&sca=%EC%9D%BC%EB%B0%98%EB%8C%80%ED%95%99%EC%9B%90'
url3 = 'https://khusm.khu.ac.kr/bbs/board.php?bo_table=s6_1&sca=%EC%9E%A5%ED%95%99'
url4 = 'https://khusm.khu.ac.kr/bbs/board.php?bo_table=s6_1&sca=%EC%9D%BC%EB%B0%98'
css_selector = '#fboardlist > div.tb_outline > div > div:nth-child(2) > div.div_td.col_subject > a'
title_latest_hs = ''
title_latest_grd = ''
title_latest_sch = ''
title_latest_gen = ''

while True:
    title_latest_hs = new_post_alert(url1, css_selector, "학사", title_latest_hs)
    title_latest_grd = new_post_alert(url2, css_selector, "일반대학원", title_latest_grd)
    title_latest_sch = new_post_alert(url3, css_selector, "장학", title_latest_sch)
    title_latest_gen = new_post_alert(url4, css_selector, "일반", title_latest_gen)
    time.sleep(30)
