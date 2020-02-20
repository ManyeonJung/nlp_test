import json
import logging
from pprint import pprint
import requests

'''
    윈도우에서 MeCab사용할 수 있도록 서버에서 처리하고 결과를 받을 수 있게함
    하위 메소드 tagger, morph, pos 
    tagger : 모든 형태소와 태그를 반환
    morph : 분리된 형태소만 반환
    pos : 형태소와 태그 튜플 리스트를 반환
    
    데이터는 단일 str또는 list str을 사용할 수 있음
    
    MeCabAPI를 초기화할 때 URL을 넣거나 default URL을 사용할 수 있음
    
'''
URL = "http://*.*.*.*:5001"

class MeCabAPI:
    def __init__(self,url=URL):
        self.url=url

    def tagger(self,string):
        try:
            if type(string)==str:
                data= {"string" : string}
                response = requests.post(url="{0}/tagger".format(self.url),data=data)
                result = json.loads(response.content)["result"]
                return result
            elif type(string)==list:
                data = {"string": string}
                response = requests.post(url="{0}/taggerlist".format(self.url), data=data)
                result = json.loads(response.content)["result"]
                return result
        except Exception as err:
            logging.warning(err)
            return None

    def morph(self,string):
        try:
            response = self.pos(string)
            if len(response) == 1:
                return [s for s,t in response]
            else:
                result = []
                for each in response:
                    result.append([s for s,t in each])
                return result
        except Exception as err:
            logging.warning(err)

    def pos(self,string):
        def text_refine(text):
            z1 = text[:-5].split()[::2]
            z2 = []
            for each in text[:-5].split()[1::2]:
                z2.append(each.split()[0].split(",")[0])
            output = list(zip(z1,z2))
            return output
        try:
            response = self.tagger(string)
            if type(string) == str:
                result = text_refine(response)
            elif type(string) == list:
                result=[]
                for each in response:
                    result.append(text_refine(each))
            return result
        except Exception as err:
            logging.warning(err)

if __name__ == "__main__":
    m = MeCabAPI()
    print(m.tagger("아버지가방에들어가신다"))
    pprint(m.morph(["테스트 문자열입니다.", "이것도 해석해보시지"]))
    pprint(m.pos("아버지가방에들어가신다"))