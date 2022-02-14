import json
import os

kind = {}
keyward1 = ''
keyward2 = ''
disc = ''
dump = {}
dump2 = {}
while keyward1 != '종료' :
    keyward1 = input('카테고리명 : ')   # 예 : 패스트푸드
    keyward2 = ''
    if keyward1 == '종료' :
        break
    while keyward2 != '상위' :
        keyward2 = input('프렌차이즈명 : ') # 예 : 맥도날드
        if keyward2 == '상위' :
            break
        disc = input('설명 : ') # 예 : 존맛탱
        dump[keyward2] = disc
    dump2[keyward1] = dump
    dump = {}
kind['kind'] = dump2

#json 파일로 저장
os.makedirs('범주정리', exist_ok=True)
with open('./범주정리/kind.json', 'w', encoding='utf-8') as f:
  json.dump(kind, f, ensure_ascii=False, indent='\t')