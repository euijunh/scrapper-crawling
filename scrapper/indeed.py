import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs/?q=python&limit={LIMIT}"


def extract_indeed_pages():
  result = requests.get(URL)
  # print(indeed_resul.text) # 전체 html 가져오기
  soup = BeautifulSoup(result.text, 'html.parser')
  pagination = soup.find("div", {"class": "pagination"})

  links = pagination.find_all('a')
  pages = []
  for link in links[:-1]:
      pages.append(int(link.string))  # string을 int로 타입 전환
  # 마지막에 next를 제외
  # 마지막 item을 제외하는 operation 사용 [:-1] -1은 마지막에서부터 시작해서 첫 item을 나타냄
  # spans[0:5] 은 0부터 시작해서 5개의 item을 가지고온다.

  max_page = pages[-1]
  return max_page


def extract_job(html):
  title = html.find("div", {"class": "title"}).find("a")["title"]
  company = html.find("span", {"class": "company"})
  # 회사네임이 존재할 때만
  if company:
    # 회사링크가 없는 경우
    company_anchor = company.find("a")
    if company_anchor is not None:
      company = str(company_anchor.string)
    else:
      company = str(company.string)
    # 빈칸을 지워준다.
    company = company.strip()
  location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"]
  return {
    'title': title,
    'company': company,
    "location": location,
    "link": f"https://www.indeed.com/viewjob?jk={job_id}"
  }


def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)

  return jobs
