import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time, os
from datetime import datetime
import pandas as pd
import urllib.request
import urllib.parse
import json


###########################################


area = ['강원도', '경기도', '경상남도', '경상북도', '광주광역시', '대구광역시',
'대전광역시', '부산광역시', '서울특별시', '울산광역시', '인천광역시',
'전라남도', '전라북도', '제주특별자치도', '충청남도', '충청북도', '세종특별자치시']

# 기본링크
link = 'https://map.kakao.com/?from=total&nil_suggest=btn&tab=place&q='
# 검색 키워드
keyward = input('검색어 입력 : ')
# 합쳐진 링크
search = link + urllib.parse.quote_plus(area[0]) + urllib.parse.quote_plus(keyward)

print(search)

driver = webdriver.Chrome('./chromedriver\chromedriver.exe')
driver.get(search)
time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

areaDic = {keyward : {'설명' : '패스트푸드, 고오급 레스토랑'}}

#해당 페이지 정보 분석
obj = driver.find_elements_by_css_selector('.PlaceItem.clickArea')
#상호명
title = soup.find_all(class_='link_name')
#서브카테고리
category = driver.find_elements_by_css_selector('.subcategory.clickable')
#평점
score = soup.find_all(class_='score')
#주소
addr = soup.find_all(class_='addr')
#번호
tel = driver.find_elements_by_css_selector('.phone')


print('상호명 :', title[0].attrs['title'])
d_title = str(title[0].attrs['title'])
#print('카테고리 : ', category[0].get_attribute('innerHTML'))
#d_sub = str(category[0].get_attribute('innerHTML'))
print('평점 :', score[0].find(attrs={'data-id':'scoreNum'}).string)
d_score = score[0].find(attrs={'data-id':'scoreNum'}).string + ' / 5.0'
print('도로명 주소 : ', addr[0].find(attrs={'data-id':'address'}).string)
d_addr1 = addr[0].find(attrs={'data-id':'address'}).string
print('지번 주소 : ', addr[0].find(attrs={'data-id':'otherAddr'}).string)
d_addr2 = addr[0].find(attrs={'data-id':'otherAddr'}).string
print('번호 : ', tel[0].get_attribute('innerHTML'))
d_tel = str(tel[0].get_attribute('innerHTML'))
#한 페이지당 15개씩 나온다.
print('페이지 당 표시 갯수 : ', len(obj))
print('페이지 당 상호 갯수 : ', len(title))
#print('페이지 당 카테고리 갯수 : ', len(category))
print('페이지 당 평점 갯수 : ', len(score))
print('페이지 당 주소 갯수 : ', len(addr))
print('페이지 당 번호 갯수 : ', len(tel))

domainDic = {}

#지역
domainDic['지역'] = area[0]
#서브
#domainDic['서브카테고리'] = d_sub
#평점
domainDic['평점'] = d_score
#도로명
domainDic['도로명 주소'] = d_addr1
#지번
domainDic['지번 주소'] = d_addr2
#번호
domainDic['번호'] = d_tel
#딕셔너리에 추가
areaDic[d_title] = domainDic

#json 파일로 저장
with open('test.json', 'w', encoding='utf-8') as f:
  json.dump(areaDic, f, ensure_ascii=False, indent='\t')




# # how many scrolls we need
# scroll_cnt = 3

# os.makedirs('result', exist_ok=True)

# for i in range(scroll_cnt):
#   # scroll to bottom
#   driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#   time.sleep(3)

#   # click 'Load more' button, if exists
#   try:
#     load_more = driver.find_element_by_xpath('//*[contains(@class,"U26fgb O0WRkf oG5Srb C0oVfc n9lfJ")]').click()
#   except:
#     print('Cannot find load more button...')

# # get review containers
# reviews = driver.find_elements_by_xpath('//*[@jsname="fk8dgd"]//div[@class="d15Mdf bAhLNe"]')

# print('There are %d reviews avaliable!' % len(reviews))
# print('Writing the data...')

# # create empty dataframe to store data
# df = pd.DataFrame(columns=['name', 'ratings', 'date', 'helpful', 'comment', 'developer_comment'])

# # get review data
# for review in reviews:
#   # parse string to html using bs4
#   soup = BeautifulSoup(review.get_attribute('innerHTML'), 'html.parser')

#   # reviewer
#   name = soup.find(class_='X43Kjb').text

#   # rating
#   ratings = int(soup.find('div', role='img').get('aria-label').replace('별표 5개 만점에', '').replace('개를 받았습니다.', '').strip())

#   # review date
#   date = soup.find(class_='p2TkOb').text
#   date = datetime.strptime(date, '%Y년 %m월 %d일')
#   date = date.strftime('%Y-%m-%d')

#   # helpful
#   helpful = soup.find(class_='jUL89d y92BAb').text
#   if not helpful:
#     helpful = 0
  
#   # review text
#   comment = soup.find('span', jsname='fbQN7e').text
#   if not comment:
#     comment = soup.find('span', jsname='bN97Pc').text
  
#   # developer comment
#   developer_comment = None
#   dc_div = soup.find('div', class_='LVQB0b')
#   if dc_div:
#     developer_comment = dc_div.text.replace('\n', ' ')
  
#   # append to dataframe
#   df = df.append({
#     'name': name,
#     'ratings': ratings,
#     'date': date,
#     'helpful': helpful,
#     'comment': comment,
#     'developer_comment': developer_comment
#   }, ignore_index=True)

# # finally save the dataframe into csv file
# filename = datetime.now().strftime('result/%Y-%m-%d_%H-%M-%S.csv')
# df.to_csv(filename, encoding='utf-8-sig', index=False)
# driver.stop_client()
# driver.close()

# print('Done!')