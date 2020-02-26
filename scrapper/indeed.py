import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs/?q=python&limit={LIMIT}"

def extract_indeed_pages():
  result = requests.get(URL)
  # print(indeed_resul.text) # 전체 html 가져오기
  soup = BeautifulSoup(result.text, 'html.parser')
  pagination = soup.find("div", {"class":"pagination"})

  links = pagination.find_all('a')
  pages = []
  for link in links[:-1]:
    pages.append(int(link.string)) # string을 int로 타입 전환
  # 마지막에 next를 제외 
  # 마지막 item을 제외하는 operation 사용 [:-1] -1은 마지막에서부터 시작해서 첫 item을 나타냄
  # spans[0:5] 은 0부터 시작해서 5개의 item을 가지고온다.

  max_page = pages[-1]
  return max_page

def extract_indeed_jobs(last_page):
  for page in range(last_page):
    request = requests.get(f"{URL}&start={page*LIMIT}")
    print(request.status_code)
