from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time, os

#같은 폴더 아니면 드라이버 경로 지정
driver = webdriver.Chrome('./chromedriver\chromedriver.exe')
url = 'https://google.com'
#브라우저 켜기
driver.get(url)

#검색(클래스는 앞에 .을 붙이고 빈 칸도 없애도 .으로), send_keys 매개변수는 검색어
driver.find_element_by_css_selector('.gLFyf.gsfi').send_keys('파이썬')
#엔터키
driver.find_element_by_css_selector('.gLFyf.gsfi').send_keys(Keys.ENTER)
#어떤 클래스 엘리먼트 찾아서 클릭(복수의 경우, 이 경우 3번째 페이지)
driver.find_elements_by_css_selector('.LC20lb')[2].click()
#단수의 경우
# driver.find_element_by_css_selector('.LC20lb').click()