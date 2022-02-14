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

firstOpen = True
link = 'https://map.kakao.com/?from=total&nil_suggest=btn&tab=place&q='
keyward = input('검색어 입력 : ')
search = link + urllib.parse.quote_plus(area[0]) + urllib.parse.quote_plus(keyward)

driver = webdriver.Chrome('./chromedriver\chromedriver.exe')
driver.get(search)
time.sleep(2)
if firstOpen == True :
  allSite = driver.find_element_by_css_selector('.index.NOFLASH')
  time.sleep(1)
  allSite.click()
  time.sleep(1)
  firstOpen = False

driver.find_element_by_id('info.search.page.no2').click()
time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
w_Dict = {}
areaDic = {}
areaDic['설명'] = '패스트푸드, 고오급 레스토랑'

obj = driver.find_elements_by_css_selector('.PlaceItem.clickArea')
title = driver.find_elements_by_css_selector('.link_name')
category = driver.find_elements_by_css_selector('.subcategory.clickable')
score = driver.find_elements_by_css_selector('span.score > em.num')
addr1 = driver.find_elements_by_css_selector('div.addr > p:nth-child(1)')
addr2 = driver.find_elements_by_css_selector('div.addr > p.lot_number')
tel = driver.find_elements_by_css_selector('.phone')

term_Dic = {}
d_title = str(title[0].get_attribute('innerText'))
#d_sub = str(category[count].get_attribute('innerHTML'))
d_score = str(score[0].get_attribute('innerText')) + ' / 5.0'
d_addr1 = str(addr1[0].get_attribute('innerText'))
d_addr2 = str(addr2[0].get_attribute('innerText'))
d_tel = str(tel[0].get_attribute('innerText'))

domainDic = {}

domainDic['지역'] = area[0]
#domainDic['서브카테고리'] = d_sub
domainDic['평점'] = d_score
domainDic['도로명 주소'] = d_addr1
domainDic['지번 주소'] = d_addr2
domainDic['번호'] = d_tel
term_Dic[d_title] = domainDic
areaDic[keyward] = term_Dic
w_Dict['패스트푸드'] = areaDic

with open('test.json', 'w', encoding='utf-8') as f:
  json.dump(w_Dict, f, ensure_ascii=False, indent='\t')