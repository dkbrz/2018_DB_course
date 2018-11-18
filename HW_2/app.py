from flask import Flask
from flask import request
from flask import render_template
import mysql.connector

app = Flask(__name__)
class DB:
    
    def __init__(self):
        self.db = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="mandarinka",
          database="techdata"
        )
        self.cur = self.db.cursor()
        
    def search(self, args):
        query = []
        check = []
        columns = []
        if 'use_htype' in args and args['use_htype'] == 'True':
            if args['htype'] != '': 
                query.append('type.htype LIKE \"%{}%\"'.format(args['htype']))
            check.append('type.htype')
            columns.append('<b>Тип устройства</b>')
        if 'use_producer' in args and args['use_producer'] == 'True':
            if args['htype'] != '': 
                query.append('type.producer LIKE \"%{}%\"'.format(args['producer']))
            check.append('type.producer')
            columns.append('<b>Производитель</b>')
        if 'use_model' in args and args['use_model'] == 'True':
            if args['model'] != '': 
                query.append('type.model LIKE \"%{}%\"'.format(args['model']))
            check.append('type.model')
            columns.append('<b>Модель</b>')
        if 'use_out_date' in args and args['use_out_date'] == 'True':
            if args['out_date'] != '':
                query.append('hardware.out_date = \"{}\"'.format(args['out_date']))
            check.append('hardware.out_date')
            columns.append('<b>Дата выдачи</b>')
        if 'use_name' in args and args['use_name'] == 'True':
            if args['name'] != '': 
                query.append('workers.name LIKE \"%{}%\"'.format(args['name']))
            check.append('workers.name')
            columns.append('<b>Имя</b>')
        if 'use_department' in args and args['use_department'] == 'True':
            if args['department'] != '': 
                query.append('workers.department LIKE \"%{}%\"'.format(args['department']))
            check.append('workers.department')
            columns.append('<b>Департамент</b>')
        if 'use_position' in args and args['use_position'] == 'True':
            if args['position'] != '': 
                query.append('workers.position LIKE \"%{}%\"'.format(args['position']))
            check.append('workers.position')
            columns.append('<b>Должность</b>')
        
        if 'use_office' in args and args['use_office'] == 'True':
            if args['office'] != '': 
                query.append('workers.office={}'.format(args['office']))
            check.append('workers.office')
            columns.append('<b>Кабинет</b>')

        st = 'SELECT DISTINCT {} FROM type \
        JOIN hardware ON type.id = hardware.id_char \
        JOIN workers ON workers.id = hardware.owner \
        WHERE {}'.format(', '.join(check), ' AND '.join(query))
        print (st)
        self.cur.execute(st)
        data = [tuple(columns)]+self.cur.fetchall()
        return data
        #return st
    
    def prettify_search(self, data):
        return '<table><tr><td>{} </td></tr></table>'.format(
            '</td></tr><tr><td>'.join(
                ['</td><td>'.join(str(x) for x in i) for i in data]
            ))

db = DB()

@app.route('/',  methods=['GET'])
def index():
    if request.args:
        #try:
            result = db.prettify_search(db.search(request.args))
            #result = db.search(request.args)
            return render_template('index.html', result=result)
        #except:
        #    return render_template('index.html',result='Что-то пошло не так или ваш запрос пуст.')
    return render_template('index.html',result='')

@app.route('/workers',  methods=['GET'])
def workers():
    if request.args:
        #try:
            result = db.prettify_search(db.search(request.args))
            #result = db.search(request.args)
            return render_template('success.html')
        #except:
        #    return render_template('index.html',result='Что-то пошло не так или ваш запрос пуст.')
    return render_template('workers.html',result='')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
