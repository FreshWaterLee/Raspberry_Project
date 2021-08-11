## FireBase Example Get, Set, Update

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
##FireBase 접근 및 비공개를 다운받아서 
##경로등을 설정해주어야 Python으로 FireBase에 접근이 가능하다.
cred = credentials.Certificate("./raspython-fire-firebase-adminsdk-zhvmd-5ab5a3d2dd.json")
## 비공개 키 파일 불러오기
firebase_admin.initialize_app(cred)
#FireBase 연결 
db = firestore.client()
#FireBase 데이터 객체화
doc_ref = db.collection(u'RasPy').document(u'RaspberryPi')
## collecition 내부에는 컬렉션 이름, Document 내부에는 문서 이름
## 입력해서 FireBase 내부에 있는 문서에 데이터 접근을 가능케 하는 객체생성
doc_ref.set({
## set 이란 함수를 사용해 문서에 존재하는 필드의 데이터 접근
    u'CPUTemp' : 200
})
#FireBase 데이터 불러오기
try:
    doc = doc_ref.get()
    ## 설정한 Collection의 문서에 존재하는 필드값을 모두 가져옴
    print(u'Document data: {}'.format(doc.to_dict()))
except google.cloud.exceptions.NotFound:
    print(u'No such document!')

## 데이터 업데이트 방법
#doc_ref.update({
#        txt : txt,
#        updateDate : new Date().getTime()
#    });
