import requests
from bs4 import BeautifulSoup



'''
1. 페이지 가져오기
2. request만들기
3. job 추출하기
'''

def get_last_page(url, header=None):
   result = requests.get(url, headers=header) #헤더가 없으면 페이지 값이 이상하게 나온다.
   soup = BeautifulSoup(result.text, "html.parser")
   pages = soup.find('div', class_='s-pagination')
   if pages is not None:
       pages = pages.find_all('a')
   last_page = pages[-2].get_text(strip=True)
   print('max_page :', last_page)
   return int(last_page)

def extract_job(html):
    # result['data-jobid']
    title =html.find('a', class_='s-link')['title']
    company, location =html.find('h3', class_='fc-black-700').find_all('span', recursive=False) 
    # print(company.string, location.string)
    company = company.get_text(strip=True) #공백삭제
    location = location.get_text(strip=True) #공백삭제  : 문자를 넣으면 해당 문자 삭제
    job_id = html['data-jobid']
    apply_url = "https://stackoverflow.com/jobs"
    return {'title':title,
            'company':company,
            'location':location,
            'link':f'{apply_url}/{job_id}'}

def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f'Scrapping SO page--- {page}')
        result = requests.get(f'{url}&pg={page}')
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all('div', class_='-job')
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs
        # print(result.status_code)  #서버 응답확인
        # print(page+1)
    
def get_jobs(word):
    url  = f"https://stackoverflow.com/jobs?q={word}&sort=p"
    # header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs