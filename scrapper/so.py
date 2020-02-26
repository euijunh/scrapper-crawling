import requests
from bs4 import BeautifulSoup

URL = f"https://www.stackoverflow.com/jobs?q=python&sort=i"

def get_last_page():
  result = requests.get(URL)
  # print(indeed_resul.text) # 전체 html 가져오기
  soup = BeautifulSoup(result.text, 'html.parser')
  pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
  last_page = pages[-2].get_text(strip=True) # -1은 마지막,  -2가 그 전 숫자
  return int(last_page)

def extract_job(html):
  title = html.find("a", {"class": "s-link"})["title"]
  # recursive은 전부 가져오지 않는 옵션
  # unpacking value라고하면 리스트안에 요소를 미리알고 있을때 사용가능 
  company, location = html.find("h3", {"class": "fs-body1"}).find_all("span", recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True).strip("-").strip(" \r").strip("\n")
  job_id = html["data-jobid"]
  return {'title': title, 'company': company, 'location': location, 'apply_link': f"https://www.stackoverflow.com/jobs/{job_id}"}
  
  
def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping SO: page: {page+1}")
    result = requests.get(f"{URL}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "-job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)

  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs