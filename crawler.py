from selenium import webdriver
from bs4 import BeautifulSoup
import time, os
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

# 지역 광범위
area = ['강원도', '경기도', '경상남도', '경상북도', '광주광역시', '대구광역시',
'대전광역시', '부산광역시', '서울특별시', '울산광역시', '인천광역시',
'전라남도', '전라북도', '제주특별자치도', '충청남도', '충청북도', '세종특별자치시']

# 지역 세부
# area = ['강원도', '경기도수원시', '경기도성남시', '경기도용인시',
# '경기도안양시', '경기도안산시', '경기도과천시', '경기도광명시', '경기도광주시',
# '경기도군포시', '경기도부천시', '경기도시흥시', '경기도김포시', '경기도안성시',
# '경기도오산시', '경기도의왕시', '경기도이천시', '경기도평택시', '경기도하남시',
# '경기도화성시', '경기도여주시', '경기도양평군', '경기도고양시', '경기도구리시',
# '경기도남양주시', '경기도동두천시', '경기도양주시', '경기도의정부시',
# '경기도파주시', '경기도포천시', '경기도연천군',
# '경기도가평군', '경상남도', '경상북도', '광주광역시', '대구광역시',
# '대전광역시', '부산광역시', '서울종로구', '서울중구', '서울용산구', '서울성동구',
# '서울광진구', '서울동대문구', '서울중랑구', '서울성북구', '서울강북구',
# '서울도봉구', '서울노원구', '서울은평구', '서울서대문구', '서울마포구',
# '서울양천구', '서울강서구', '서울구로구', '서울금천구', '서울영등포구',
# '서울동작구', '서울관악구', '서울서초구', '서울강남구', '서울송파구',
# '서울강동구', '울산광역시', '인천광역시',
# '전라남도', '전라북도', '제주특별자치도', '충청남도', '충청북도', '세종특별자치시']

# 패스트푸드
fastfood = ['맥도날드', '버거킹', '스테프핫도그', 'KFC', 
'파파이스', '맘스터치', '롯데리아', '종료']
# fastfood = ['파파이스', '종료']
# 햄버거
hamburger = ['모스버거', '쉐이크쉑', '자니로켓', '노브랜드버거', '종료']
# hamburger = ['모스버거', '쉐이크쉑', '종료']
# 샌드위치
sandwich = ['서브웨이', '종료']
# 도시락
dosirak = ['한솥', '토마토', '종료']
# 드럭스토어
drugstore = ['롭스', '랄라블라', '올리브영', '판도라', '종료']
# drugstore = ['롭스', '랄라블라', '종료']
# 화장품
cosmetics = ['네이처리퍼블릭', '닥터자르트', '아리따움', '이니스프리', '에뛰드하우스', '헤라', '설화수',
'아모레퍼시픽', '미샤', '토니모리', '스킨푸드', '종료']
# cosmetics = ['네이처리퍼블릭', '닥터자르트', '종료']
# 커피
cafe = ['더리터', '더벤티', '라떼떼', '메가', '빽다방', '엔제리너스', 
'이디야', '카페드롭탑', '카페베네', '커피베이', '탐앤탐스', '투썸플레이스',
'폴바셋', '할리스', '스타벅스', '파스쿠찌', '종료']
# cafe = ['더리터', '종료']
# 디저트카페
dessertcafe = ['요거프레소', '종료']
# 아이스크림
icecream = ['카페띠아모', '배스킨라빈스', '하겐다즈', '나뚜루', '종료']
# 치킨
chicken = ['굽네', 'BHC', 'BBQ', '교촌', '네네', '처갓집', '또래오래',
'호식이두마리', '페리카나', '치킨마루', '종료']
# 토스트
toast = ['이삭', '종료']

allCat = [fastfood, hamburger, sandwich, dosirak, drugstore, 
cosmetics, cafe, dessertcafe, icecream, chicken, toast]

location = 0
dataNum = 0
firstOpen = True
link = 'https://map.kakao.com/?from=total&nil_suggest=btn&tab=place&q='
driver = webdriver.Chrome('./chromedriver\chromedriver.exe')
keyward = ''
cate = ['패스트푸드', '햄버거', '샌드위치', '도시락', '드럭스토어', 
'화장품', '커피', '디저트카페', '아이스크림', '치킨', '토스트']
w_Dict = {}
areaDic = {}
categoryDic = {}
filterSwitch = True
fSwit = ''
cateLeng = 0
leng = 0
tstart = time.time()  # 시작 시간 저장
while cateLeng < len(allCat) :
    while keyward != '종료' :
        # keyward = input('검색어 입력 : ')
        # print('현재 : ',cateLeng)
        keyward = (allCat[cateLeng])[leng]
        leng += 1
        if keyward == '종료' :
            break
        # else :
        #     disc = input('설명 입력 : ')
        # fSwit = input('결과필터 On/Off(Off 이외에는 Onc으로 가정) : ')
        # if fSwit == 'On' :
        #     filterSwitch = True
        # elif fSwit == 'Off' :
        #     filterSwitch = False
        # else :
        #     filterSwitch = True
        term_Dic = {}
        if cate[cateLeng] == '커피' :
            area = ['강원도', '경기도수원시', '경기도성남시', '경기도용인시',
            '경기도안양시', '경기도안산시', '경기도과천시', '경기도광명시', '경기도광주시',
            '경기도군포시', '경기도부천시', '경기도시흥시', '경기도김포시', '경기도안성시',
            '경기도오산시', '경기도의왕시', '경기도이천시', '경기도평택시', '경기도하남시',
            '경기도화성시', '경기도여주시', '경기도양평군', '경기도고양시', '경기도구리시',
            '경기도남양주시', '경기도동두천시', '경기도양주시', '경기도의정부시',
            '경기도파주시', '경기도포천시', '경기도연천군',
            '경기도가평군', '경상남도', '경상북도', '광주광역시', '대구광역시',
            '대전광역시', '부산광역시', '서울종로구', '서울중구', '서울용산구', '서울성동구',
            '서울광진구', '서울동대문구', '서울중랑구', '서울성북구', '서울강북구',
            '서울도봉구', '서울노원구', '서울은평구', '서울서대문구', '서울마포구',
            '서울양천구', '서울강서구', '서울구로구', '서울금천구', '서울영등포구',
            '서울동작구', '서울관악구', '서울서초구', '서울강남구', '서울송파구',
            '서울강동구', '울산광역시', '인천광역시',
            '전라남도', '전라북도', '제주특별자치도', '충청남도', '충청북도', '세종특별자치시']
        else :
            area = ['강원도', '경기도', '경상남도', '경상북도', '광주광역시', '대구광역시',
            '대전광역시', '부산광역시', '서울특별시', '울산광역시', '인천광역시',
            '전라남도', '전라북도', '제주특별자치도', '충청남도', '충청북도', '세종특별자치시']
        while location < len(area) :
            search = link + urllib.parse.quote_plus(area[location]) + urllib.parse.quote_plus(keyward) + urllib.parse.quote_plus(cate[cateLeng])
            # search = link + urllib.parse.quote_plus(keyward)
            # print(area[location]+cate[cateLeng])
            driver.get(search)
            time.sleep(2)
            if firstOpen == True :
                allSite = driver.find_element_by_id('dimmedLayer')
                time.sleep(1)
                allSite.click()
                firstOpen = False
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

                #검색결과 없는 경우
            npInfo = driver.find_elements_by_id('info.noPlace')
            noSearch = str(npInfo[0].get_attribute('class'))
            if noSearch == 'noPlace' :  # 검색결과 없음
                location += 1
                continue

            #페이지 부분 클래스로 찾는다
            pages = driver.find_element_by_css_selector('.pages')
            page_2 = driver.find_element_by_id('info.search.page.no2')
            page_3 = driver.find_element_by_id('info.search.page.no3')
            page_4 = driver.find_element_by_id('info.search.page.no4')
            page_5 = driver.find_element_by_id('info.search.page.no5')
            p_next = driver.find_element_by_id('info.search.page.next')

            #페이지 개수
            pageNum = 0
            #반복 횟수 = 페이지에 있는 정보 갯수만큼
            count = 0
            current = 1

            p2_state = str(page_2.get_attribute('class'))
            p3_state = str(page_3.get_attribute('class'))
            p4_state = str(page_4.get_attribute('class'))
            p5_state = str(page_5.get_attribute('class'))
            # 페이지랩 상태
            pn_state = str(p_next.get_attribute('class'))
            # 첫 페이지랩 페이지 수
            pageNum = pState(p2_state, p3_state, p4_state, p5_state, pageNum)

            while current < pageNum + 1 :
                obj = driver.find_elements_by_css_selector('.PlaceItem.clickArea')
                title = driver.find_elements_by_css_selector('.link_name')
                category = driver.find_elements_by_css_selector('.subcategory.clickable')
                #필터링용
                # filter_sub = str(category[0].get_attribute('innerHTML'))
                # cate = str(category[0].get_attribute('innerHTML'))
                score = driver.find_elements_by_css_selector('span.score > em.num')
                addr1 = driver.find_elements_by_css_selector('div.addr > p:nth-child(1)')#div.addr > p:nth-child(1)
                addr2 = driver.find_elements_by_css_selector('div.addr > p.lot_number')#div.addr > p.lot_number
                tel = driver.find_elements_by_css_selector('.phone')
                while count < len(obj) :
                    d_title = str(title[count].get_attribute('innerText'))
                    #필터링용
                    # d_sub = str(category[count].get_attribute('innerHTML'))
                    d_score = str(score[count].get_attribute('innerText')) + ' / 5.0'
                    d_addr1 = str(addr1[count].get_attribute('innerText'))
                    d_addr2 = str(addr2[count].get_attribute('innerText'))
                    d_tel = str(tel[count].get_attribute('innerHTML'))

                    domainDic = {}

                    #지점
                    domainDic['지점'] = d_title
                    #지역
                    # domainDic['지역'] = area[location]
                    #서브
                    #domainDic['서브카테고리'] = d_sub
                    #도로명
                    domainDic['도로명 주소'] = d_addr1
                    #지번
                    domainDic['지번 주소'] = d_addr2
                    #번호
                    domainDic['번호'] = d_tel
                    #평점
                    domainDic['평점'] = d_score

                    # if filterSwitch == True :
                    #     if d_sub == filter_sub :
                    #         term_Dic[d_title] = domainDic
                    #         dataNum += 1
                    # else :
                    #     term_Dic[d_title] = domainDic
                    #     dataNum += 1
                    term_Dic[d_title] = domainDic
                    dataNum += 1
                    count += 1
                    ###
                current += 1
                if current == 2 :
                    if p2_state == inact :
                        page_2.click()
                        # print('페이지 2 이동')
                        time.sleep(1)
                elif current == 3 :
                    if p3_state == inact :
                        page_3.click()
                        # print('페이지 3 이동')
                        time.sleep(1)
                elif current == 4 :
                    if p4_state == inact :
                        page_4.click()
                        # print('페이지 4 이동')
                        time.sleep(1)
                elif current == 5 :
                    if p5_state == inact :
                        page_5.click()
                        # print('페이지 5 이동')
                        time.sleep(1)
                elif current == 6 :
                    # 다음 페이지랩 없는 상태
                    if pn_state == n_dis :
                        print('',end='')
                    else :  # 다음 페이지랩 있는 상태
                        p_next.click()
                        # print('다음 페이지랩으로 이동')
                        time.sleep(2)
                        #페이지 부분 클래스로 찾는다
                        pages = driver.find_element_by_css_selector('.pages')
                        page_2 = driver.find_element_by_id('info.search.page.no2')
                        page_3 = driver.find_element_by_id('info.search.page.no3')
                        page_4 = driver.find_element_by_id('info.search.page.no4')
                        page_5 = driver.find_element_by_id('info.search.page.no5')
                        p_next = driver.find_element_by_id('info.search.page.next')
                        p2_state = str(page_2.get_attribute('class'))
                        p3_state = str(page_3.get_attribute('class'))
                        p4_state = str(page_4.get_attribute('class'))
                        p5_state = str(page_5.get_attribute('class'))
                        # 페이지랩 상태
                        pn_state = str(p_next.get_attribute('class'))
                        # 첫 페이지랩 페이지 수
                        pageNum = pState(p2_state, p3_state, p4_state, p5_state, pageNum)
                        current = 1
                count = 0
                ###
            location += 1
        areaDic[keyward] = term_Dic
        print(keyward,'에 대해 크롤링한 데이터 갯수 : ', dataNum)
        dataNum = 0
        location = 0
    # print('증가전 : ',cateLeng)
    # print(cate[cateLeng])
    w_Dict[cate[cateLeng]] = areaDic
    areaDic = {}
    cateLeng += 1
    leng = 0
    # print('증가후 : ',cateLeng)
    keyward = ''

categoryDic['category'] = w_Dict
print("time :", time.time() - tstart)  # 현재시각 - 시작시간 = 실행 시간
os.makedirs('category', exist_ok=True)
#json 파일로 저장
with open('./category/category.json', 'w', encoding='utf-8') as f:
  json.dump(categoryDic, f, ensure_ascii=False, indent='\t')