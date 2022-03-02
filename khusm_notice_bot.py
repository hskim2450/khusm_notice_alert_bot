import requests
from bs4 import BeautifulSoup
import time
from slack_notification import post_to_slack

def board_newest_post(url, selector):
    req = requests.get(url, verify=False) #경희의대 홈페이지가 verify=False해줘야지 url 접근 가능
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    posts = soup.select_one(selector)
    posts.select_one('span').decompose() #span태그에 '[학사]'이런 태그 붙어있어서 없애버리고 제목만 꺼냄.
    return posts

url_list = ['https://khusm.khu.ac.kr/bbs/board.php?bo_table=s6_1&sca=%ED%95%99%EC%82%AC',
            'https://khusm.khu.ac.kr/bbs/board.php?bo_table=s6_1&sca=%EC%9D%BC%EB%B0%98%EB%8C%80%ED%95%99%EC%9B%90',
            'https://khusm.khu.ac.kr/bbs/board.php?bo_table=s6_1&sca=%EC%9E%A5%ED%95%99',
            'https://khusm.khu.ac.kr/bbs/board.php?bo_table=s6_1&sca=%EC%9D%BC%EB%B0%98']
css_selector = '#fboardlist > div.tb_outline > div > div:nth-child(2) > div.div_td.col_subject > a'
#초기 게시판 최근 글 제목 분류별로 저장
title_latest_list = [board_newest_post(url_list[0], css_selector).text.strip(),
                board_newest_post(url_list[1], css_selector).text.strip(),
                board_newest_post(url_list[2], css_selector).text.strip(),
                board_newest_post(url_list[3], css_selector).text.strip()]

#10분마다 게시판 최근글 스크래핑 및 비교
while True:
    for i in range(len(url_list)):
        if i == 0:
            board_category = "학사"
        elif i == 1:
            board_category = "일반대학원"
        elif i == 2:
            board_category = "장학"
        elif i == 3:
            board_category = "일반"
        title = board_newest_post(url_list[i], css_selector).text.strip()
        link = board_newest_post(url_list[i], css_selector).attrs['href']
        if title != title_latest_list[i]:
            post_to_slack("의대게시판 새글: [" + board_category + "] " + title)
            post_to_slack("링크: " + link)
            title_latest_list[i] = title
    time.sleep(600)
