from flask import Flask, redirect, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("SuperScrapper", template_folder='templates')

db = {} 


@app.route('/') #'/'주소로 접속하면 아래의 함수를 실행
def home():
    # returyou want?' required/> <button>Search</button>"
    cur_list = db
    return render_template('main.html',
                         cur_list=cur_list)

@app.route('/report')
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existJobs = db.get(word)  #db에 해당 검색어가 있는지 확인
        if existJobs:
            jobs = existJobs
        else:
            jobs = get_jobs(word) #db에 검색어 없을시, 스크래핑 실행
            db[word] = jobs
    else:
        return redirect("/")
    # print("jobs",jobs)
    return render_template('report.html', 
                           searchingBy=word,
                           resultsNumber=len(jobs),
                           jobs = jobs
                           ) #데이터 넘겨주기
@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:    #검색어 없을시 예외처리
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:  #검색한 job이 존재 X시 예외처리
            raise Exception()
        save_to_file(jobs)
        return send_file('jobs_export.csv')
    except Exception as err:
        print(err)
        return redirect("/")   
        # return  err
        
app.run(host="0.0.0.0", debug=True)  #debug=True : 코드 변경시 플라스크 자동 리로드
