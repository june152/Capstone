import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

#네이버 블로그 검색 + 변환
plusUrl = urllib.parse.quote_plus(input('검색어 입력 : '))
#몇 페이지를 불러올 것인가
pageNum = 1
count = 1

i = input('몇 페이지 크롤링합니까? : ')

lastPage = pageNum + (int(i) - 1)*10
while pageNum < lastPage + 1:
    url = f'https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query={plusUrl}&sm=tab_pge&srchby=all&st=sim&where=post&start={pageNum}'
    #url 열기
    html = urllib.request.urlopen(url).read()
    #분석
    soup = BeautifulSoup(html, 'html.parser')
    #특정 클래스 찾기
    title = soup.find_all(class_='sh_blog_title')
    print(f'-----{count}페이지 결과')
    for i in title :
        print(i.attrs['title'])
        print(i.attrs['href'])
    print()

    pageNum += 10
    count += 1