import csv

def save_to_file(jobs):
  # mode="w"는 file을 open할 때마다 이전 파일 내용이 날라간다
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["title", "company", "location", "link"])
  for job in jobs:
    # dictionary의 값만 추출하는 함수 values()
    # list로 만들어주어야한다.
    writer.writerow(list(job.values()))
  return