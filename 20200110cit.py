#-*-coding:utf-8-*-
import requests
import re
import json
import os
from requests.exceptions import RequestException
from  multiprocessing import Pool

headers = {
  'Content-Type': 'text/plain; charset=UTF-8',
  'Origin':'https://maoyan.com',
  'Referer':'https://maoyan.com/board/4',
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
  'Cookie': '__mta=55516948.1610191431899.1610285198545.1610287005007.25; uuid_n_v=v1; uuid=25F1AB40526D11EBBF98AF0FCF9C8DCA707CCB5167C74FC3AEFACED3A88A2C99; _csrf=a4b715dc1631643c9752ef98571cc5e655be6d193a8682dc565399f1923434fe; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1610191432; _lxsdk_cuid=176e6e3687ec8-0fddf9dae33fde-9691c21-1fa400-176e6e3687fc8; _lxsdk=25F1AB40526D11EBBF98AF0FCF9C8DCA707CCB5167C74FC3AEFACED3A88A2C99; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1610287005; _lxsdk_s=176ec95badf-9db-15a-a91%7C%7C3'
}
 

def get_one_page(url,headers):
  try:
    response =requests.get(url,headers =headers)
    if response.status_code == 200:
      return response.text
    return None
  except RequestException:
    return None
 
def parse_one_page(html):
  pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
  items = re.findall(pattern,html)
  for item in items:
    yield{
    'index':item[0],
    'image':item[1],
    'title':item[2],
    'actor':item[3].strip()[3:],
    'time':item[4].strip()[5:],
    'score':item[5]+item[6]
    }

def write_to_file(content):
  #encoding ='utf-8',ensure_ascii =False,使写入文件的代码显示为中文
  with open('result.txt','a',encoding ='utf-8') as f:
    f.write(json.dumps(content,ensure_ascii =False)+'\n')
    f.close()
    
def save_image_file(url,path): 
  jd = requests.get(url)
  if jd.status_code == 200:
    with open(path,'wb') as f:
      f.write(jd.content)
      f.close()
 
def main(offset):
  url = "https://maoyan.com/board/4?offset="+str(offset)
  html = get_one_page(url,headers)
  if not os.path.exists('covers'):
    os.mkdir('covers')
  for item in parse_one_page(html):
    print(item)
    write_to_file(item)
    save_image_file(item['image'],'covers/'+item['title']+'.jpg')
 
if __name__ == '__main__':
#     for i in range(10):
#         main(i*10)
  pool = Pool()
  pool.map(main,[i*10 for i in range(10)])
  pool.close()
  pool.join()