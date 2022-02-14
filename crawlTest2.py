from selenium import webdriver
from bs4 import BeautifulSoup
import time, os
from datetime import datetime
import pandas as pd
import urllib.request
import urllib.parse
import json

###########################################

#다음 페이지 없는 경우
n_dis = 'next disabled'
#현재 페이지
act = 'ACTIVE'
#현재 이외의 페이지
inact = 'INACTIVE'
#해당 페이지 없음
inact_hide = 'INACTIVE HIDDEN'

def pState (s2, s3, s4, s5, pNum) :
    # 페이지 5 없음
    if s5 == inact_hide :
        # 페이지 4 없음
        if s4 == inact_hide :
            # 3 없음
            if s3 == inact_hide :
                # 2 없음
                if s2 == inact_hide :
                    pNum = 1 # 단일 페이지
                else :
                    pNum = 2 # 페이지 2
            else :
                pNum = 3 # 페이지 3
        else :
            pNum = 4 # 페이지 4
    else :
        pNum = 5 # 페이지 5
    return pNum

###########################################

area = ['강원도', '경기도', '경상남도', '경상북도', '광주광역시', '대구광역시',
'대전광역시', '부산광역시', '서울특별시', '울산광역시', '인천광역시',
'전라남도', '전라북도', '제주특별자치도', '충청남도', '충청북도', '세종특별자치시']

firstOpen = True
link = 'https://map.kakao.com/?from=total&nil_suggest=btn&tab=place&q='
driver = webdriver.Chrome('./chromedriver\chromedriver.exe')
keyward = ''
w_Dict = {}
areaDic = {}
#areaDic = {keyward : {'설명' : '패스트푸드, 고오급 레스토랑'}}
# areaDic['설명'] = '패스트푸드, 고오급 레스토랑'
while keyward != '종료' :
    keyward = input('검색어 입력 : ')
    if keyward == '종료' :
        break
    search = link + urllib.parse.quote_plus(area[0]) + urllib.parse.quote_plus(keyward)

    driver.get(search)
    time.sleep(2)
    if firstOpen == True :
        allSite = driver.find_element_by_css_selector('.index.NOFLASH')
        time.sleep(1)
        allSite.click()
        firstOpen = False

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #페이지 부분 클래스로 찾는다
    pages = driver.find_element_by_css_selector('.pages')
    #page_1 = pages.find_all(attrs={'id':'info.search.page.no1'})
    page_2 = driver.find_element_by_id('info.search.page.no2')
    page_3 = driver.find_element_by_id('info.search.page.no3')
    page_4 = driver.find_element_by_id('info.search.page.no4')
    page_5 = driver.find_element_by_id('info.search.page.no5')
    p_next = driver.find_element_by_id('info.search.page.next')

    #페이지 개수
    pageNum = 0
    #반복 횟수 = 페이지에 있는 정보 갯수만큼
    count = 0
    term_Dic = {}
    current = 1

    p2_state = str(page_2.get_attribute('class'))
    p3_state = str(page_3.get_attribute('class'))
    p4_state = str(page_4.get_attribute('class'))
    p5_state = str(page_5.get_attribute('class'))
    # 첫 페이지랩 페이지 수
    pageNum = pState(p2_state, p3_state, p4_state, p5_state, pageNum)

    # page_2.click()
    # time.sleep(2)
    obj = driver.find_elements_by_css_selector('.PlaceItem.clickArea')
    # title = soup.find_all(class_='link_name')
    title = driver.find_elements_by_css_selector('.link_name')
    category = driver.find_elements_by_css_selector('.subcategory.clickable')
    # score = soup.find_all(class_='score')
    score = driver.find_elements_by_css_selector('span.score > em.num')
    # addr = soup.find_all(class_='addr')
    addr1 = driver.find_elements_by_css_selector('div.addr > p:nth-child(1)')#div.addr > p:nth-child(1)
    addr2 = driver.find_elements_by_css_selector('div.addr > p.lot_number')#div.addr > p.lot_number
    tel = driver.find_elements_by_css_selector('.phone')
    while count < len(obj) :
        d_title = str(title[count].get_attribute('innerText'))
        #d_sub = str(category[count].get_attribute('innerHTML'))
        d_score = str(score[count].get_attribute('innerText')) + ' / 5.0'
        d_addr1 = str(addr1[count].get_attribute('innerText'))
        d_addr2 = str(addr2[count].get_attribute('innerText'))
        d_tel = str(tel[count].get_attribute('innerText'))

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
            
        term_Dic[d_title] = domainDic
        count += 1
        current += 1
    areaDic[keyward] = term_Dic

w_Dict['대형마트'] = areaDic

#json 파일로 저장
with open('대형마트.json', 'w', encoding='utf-8') as f:
  json.dump(w_Dict, f, ensure_ascii=False, indent='\t')
