from selenium import webdriver
from bs4 import BeautifulSoup
import time, os
import pandas as pd
import urllib.request
import urllib.parse
import json
n_dis = 'next disabled'
act = 'ACTIVE'
inact = 'INACTIVE'
inact_hide = 'INACTIVE HIDDEN'
def pState (s2, s3, s4, s5, pNum) :
    if s5 == inact_hide :
        if s4 == inact_hide :
            if s3 == inact_hide :
                if s2 == inact_hide :
                    pNum = 1
                else :
                    pNum = 2
            else :
                pNum = 3
        else :
            pNum = 4
    else :
        pNum = 5
    return pNum
area = ['강원도', '경기도', '경상남도', '경상북도', '광주광역시', '대구광역시',
'대전광역시', '부산광역시', '서울특별시', '울산광역시', '인천광역시',
'전라남도', '전라북도', '제주특별자치도', '충청남도', '충청북도', '세종특별자치시']
location = 0
dataNum = 0
firstOpen = True
link = 'https://map.kakao.com/?from=total&nil_suggest=btn&tab=place&q='
driver = webdriver.Chrome('./chromedriver\chromedriver.exe')
keyward = ''
cate = ''
w_Dict = {}
areaDic = {}
filterSwitch = True
fSwit = ''
while keyward != '종료' :
    keyward = input('검색어 입력 : ')
    if keyward == '종료' :
        break
    fSwit = input('결과필터 On/Off(Off 이외에는 On으로 가정) : ')
    if fSwit == 'On' :
        filterSwitch = True
    elif fSwit == 'Off' :
        filterSwitch = False
    else :
        filterSwitch = True
    term_Dic = {}
    while location < len(area) :
        search = link + urllib.parse.quote_plus(area[location]) + urllib.parse.quote_plus(keyward)
        # search = link + urllib.parse.quote_plus(keyward)
        driver.get(search)
        time.sleep(3)
        if firstOpen == True :
            allSite = driver.find_element_by_css_selector('.index.NOFLASH')
            time.sleep(1)
            allSite.click()
            firstOpen = False
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        npInfo = driver.find_elements_by_id('info.noPlace')
        page_2 = driver.find_element_by_id('info.search.page.no2')
        page_3 = driver.find_element_by_id('info.search.page.no3')
        page_4 = driver.find_element_by_id('info.search.page.no4')
        page_5 = driver.find_element_by_id('info.search.page.no5')
        p_next = driver.find_element_by_id('info.search.page.next')
        pageNum = 0
        count = 0
        current = 1
        p2_state = str(page_2.get_attribute('class'))
        p3_state = str(page_3.get_attribute('class'))
        p4_state = str(page_4.get_attribute('class'))
        p5_state = str(page_5.get_attribute('class'))
        pn_state = str(p_next.get_attribute('class'))
        pageNum = pState(p2_state, p3_state, p4_state, p5_state, pageNum)
        while current < pageNum + 1 :
            obj = driver.find_elements_by_css_selector('.PlaceItem.clickArea')
            title = driver.find_elements_by_css_selector('.link_name')
            category = driver.find_elements_by_css_selector('.subcategory.clickable')
            filter_sub = str(category[0].get_attribute('innerHTML'))
            cate = str(category[0].get_attribute('innerHTML'))
            score = driver.find_elements_by_css_selector('span.score > em.num')
            addr1 = driver.find_elements_by_css_selector('div.addr > p:nth-child(1)')#div.addr > p:nth-child(1)
            addr2 = driver.find_elements_by_css_selector('div.addr > p.lot_number')#div.addr > p.lot_number
            tel = driver.find_elements_by_css_selector('.phone')
            while count < len(obj) :
                d_title = str(title[count].get_attribute('innerText'))
                d_sub = str(category[count].get_attribute('innerHTML'))
                d_score = str(score[count].get_attribute('innerText')) + ' / 5.0'
                d_addr1 = str(addr1[count].get_attribute('innerText'))
                d_addr2 = str(addr2[count].get_attribute('innerText'))
                d_tel = str(tel[count].get_attribute('innerHTML'))
                domainDic = {}
                #지역
                domainDic['지역'] = area[location]
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
                if filterSwitch == True :
                    if d_sub == filter_sub :
                        term_Dic[d_title] = domainDic
                        dataNum += 1
                else :
                    term_Dic[d_title] = domainDic
                    dataNum += 1
                count += 1
            current += 1
            if current == 2 :
                if p2_state == inact :
                    page_2.click()
                    time.sleep(2)
            elif current == 3 :
                if p3_state == inact :
                    page_3.click()
                    time.sleep(2)
            elif current == 4 :
                if p4_state == inact :
                    page_4.click()
                    time.sleep(2)
            elif current == 5 :
                if p5_state == inact :
                    page_5.click()
                    time.sleep(2)
            elif current == 6 :
                if pn_state == n_dis :
                    print('')
                else :
                    p_next.click()
                    time.sleep(2)
                    page_2 = driver.find_element_by_id('info.search.page.no2')
                    page_3 = driver.find_element_by_id('info.search.page.no3')
                    page_4 = driver.find_element_by_id('info.search.page.no4')
                    page_5 = driver.find_element_by_id('info.search.page.no5')
                    p_next = driver.find_element_by_id('info.search.page.next')
                    p2_state = str(page_2.get_attribute('class'))
                    p3_state = str(page_3.get_attribute('class'))
                    p4_state = str(page_4.get_attribute('class'))
                    p5_state = str(page_5.get_attribute('class'))
                    pn_state = str(p_next.get_attribute('class'))
                    pageNum = pState(p2_state, p3_state, p4_state, p5_state, pageNum)
                    current = 1
            count = 0
        location += 1
    areaDic[keyward] = term_Dic
    print(keyward,'에 대해 크롤링한 데이터 갯수 : ', dataNum)
    dataNum = 0
    location = 0
w_Dict['드럭스토어'] = areaDic
os.makedirs('드럭스토어', exist_ok=True)
#json 파일로 저장
with open('./드럭스토어/드럭스토어.json', 'w', encoding='utf-8') as f:
  json.dump(w_Dict, f, ensure_ascii=False, indent='\t')