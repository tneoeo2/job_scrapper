import csv

def save_to_file(jobs):
    file = open('jobs_export.csv', mode='w', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(['title', 'company', 'location', 'link'])
    for job in jobs:
        writer.writerow(list(job.values()))  #returnType:  dict_values : value값만 반환받아 리스트 형태로 변경 
    return