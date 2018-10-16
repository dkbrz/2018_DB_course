from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

from patterns import *

import sqlite3

class Work(object):
    def __init__(self, args):
        self.args = args

    def result(self):
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        string = '1=1'
        for i in ['id_test', 't_name', 'discipline','c_date']:
            if self.args[i] != '':
                string = string + ' AND ' + WORK[self.args['TYPE']][1][i].format(self.args[i])
        cur.execute(WORK[self.args['TYPE']][0].format(string))
        results = ['</td><td>'.join(str(j) for j in i) for i in [WORK[self.args['TYPE']][2]]+cur.fetchall()]

        html_part='<table>'
        for t in results:
            html_part=html_part + '<tr><td>' + t + '</td></tr>'
        html_part=html_part + '</table>'
        return html_part

class Student(object):
    def __init__(self, args):
        self.args = args

    def result(self):
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        string = '1=1'
        for i in ['id_student', 's_name', 's_course', 's_degree', 's_program']:
            if self.args[i] != '':
                string = string + ' AND ' + STUDENT[self.args['TYPE']][1][i].format(self.args[i])
        cur.execute(STUDENT[self.args['TYPE']][0].format(string))
        results = ['</td><td>'.join(str(j) for j in i) for i in [STUDENT[self.args['TYPE']][2]]+cur.fetchall()]

        html_part='<table>'
        for t in results:
            html_part=html_part + '<tr><td>' + t + '</td></tr>'
        html_part=html_part + '</table>'
        return html_part

        return results
        return [STUDENT[self.args['TYPE']][0].format(string)]


@app.route('/',  methods=['GET'])
def index():
    if request.args:
        if request.args['what']=='TEST':
            query = Work(request.args)
        else:
            query = Student(request.args)
        result = query.result()
        return render_template('index.html', result=result)
    return render_template('index.html',result='')

@app.route('/add',  methods=['GET'])
def add():
    con = sqlite3.connect('test.db')
    cur = con.cursor()
    if request.args:
        if request.args['what'] == 'TEST':
            cur.execute(ADD['TEST'].format(request.args['discipline'],
                                           request.args['task_text'],
                                           request.args['t_name'],
                                           request.args['c_date']))
            con.commit()
        elif request.args['what'] == 'STUDENT':
            cur.execute(ADD['STUDENT'].format(request.args['s_name'],
                                           str(request.args['s_course']),
                                           request.args['s_degree'],
                                           request.args['s_program']))
            con.commit()
        elif request.args['what'] == 'RESULTS':
            cur.execute(ADD['RESULTS'].format(str(request.args['id_student']),
                                           str(request.args['id_test']),
                                           str(request.args['mark'])))
            con.commit()
        return render_template('add.html', result=['Результат успешно добавлен'])
    return render_template('add.html',result='')

@app.route('/edit',  methods=['GET'])
def edit():
    if request.args:

        return render_template('edit.html', result=result)
    return render_template('edit.html',result='')

if __name__ == '__main__':
    app.run(host='localhost', port=5005, debug=True)
