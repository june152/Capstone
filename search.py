import simplejson, requests
import sys

url = "https://dapi.kakao.com/v2/local/search/keyword.json?"
apikey = "22cc33a079983f84affcd80fab62fb53"
query = "올리브영"
r = requests.get( url, params = {'query':query}, headers={'Authorization' : 'KakaoAK ' + apikey } )
js = simplejson.JSONEncoder().encode(r.json())
r.json()
