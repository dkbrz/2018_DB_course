from flask import Flask
from flask import request, redirect
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
        
    def create_worker(self, name, department, position, birth, office):
        self.cur.execute('INSERT INTO workers (name, department, position, birth, office) \
    VALUES (%s, %s, %s, %s, %s)', (name, department, position, birth, office))
        self.db.commit()
    def update_workers(self, args):
        self.cur.execute('UPDATE workers SET name = %s, department = %s, position = %s, birth = %s, office = %s WHERE id = %s', 
                         (args['name'], args['department'], args['position'], args['birth'], args['office'], args['id']))
        self.db.commit()
    def delete_workers(self, wid):
        print (wid)
        self.cur.execute('DELETE FROM workers WHERE id = {}'.format(wid))
        self.cur.execute('DELETE FROM hardware WHERE owner = {}'.format(wid))
        self.db.commit()
        
    def create_type(self, htype, producer, model, year):
        self.cur.execute('INSERT INTO type (htype, producer, model, year) \
    VALUES (%s, %s, %s, %s)', (htype, producer, model, year))
        self.db.commit()        
    def update_type(self, args):
        self.cur.execute('UPDATE type SET htype = %s, producer = %s, model = %s, year = %s WHERE id = %s', 
                         (args['htype'], args['producer'], args['model'], args['year'], args['id']))
        self.db.commit() 
    def delete_type(self, wid):
        print (wid)
        self.cur.execute('DELETE FROM type WHERE id = {}'.format(wid))
        self.cur.execute('DELETE FROM hardware WHERE id_char = {}'.format(wid))
        self.db.commit()
        
    def create_hardware(self, id_char, out_date, owner):
        self.cur.execute('INSERT INTO hardware (id_char, out_date, owner) \
    VALUES (%s, %s, %s)', (id_char, out_date, owner))
        self.db.commit()
    def update_hardware(self, args):
        self.cur.execute('UPDATE hardware SET id_char = %s, out_date = %s, owner = %s WHERE id = %s', 
                         (args['id_char'], args['out_date'], args['owner'], args['id']))
        self.db.commit()
    def delete_hardware(self, wid):
        print (wid)
        self.cur.execute('DELETE FROM hardware WHERE id = {}'.format(wid))
        self.db.commit()
        
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
        string = 'SELECT DISTINCT hardware.id, {} FROM type \
        JOIN hardware ON type.id = hardware.id_char \
        JOIN workers ON workers.id = hardware.owner \
        WHERE {}'.format(', '.join(check), ' AND '.join(query))
        print(string)
        if len(check) >= len(query) and len(query) > 0:   
            self.cur.execute(string)
            data = [tuple(columns)]+self.cur.fetchall()
            return data
        else: return []
    
    def search_workers(self, args):
        delete = '<a href="/delete?what=workers&id={}"> Удалить </a>'
        edit = '<a href="/edit_workers?id={}"> Рeдактировать </a>'
        query = []
        columns = ['<b>Имя</b>', '<b>Имя</b>','<b>Департамент</b>',
                   '<b>Должность</b>','<b>Дата рождения</b>','<b>Кабинет</b>',
                   '<b>Удалить</b>', '<b>Редактировать</b>']
        if args['id'] != '': 
            query.append('workers.id ={}'.format(args['id']))
        if args['name'] != '': 
            query.append('workers.name LIKE \"%{}%\"'.format(args['name']))
        if args['department'] != '': 
            query.append('workers.department LIKE \"%{}%\"'.format(args['department']))
        if args['position'] != '': 
            query.append('workers.position LIKE \"%{}%\"'.format(args['position']))
        if args['birth'] != '':
            query.append('birth.birth = \"{}\"'.format(args['birth']))
        if args['office'] != '': 
            query.append('workers.office={}'.format(args['office']))
            
        self.cur.execute('SELECT * FROM workers \
        WHERE {}'.format(' AND '.join(query)))
        result = [list(i)+[delete.format(i[0]), edit.format(i[0])] for i in self.cur.fetchall()]
        data = [tuple(columns)]+result
        return data

    def search_hardware(self, args):
        delete = '<a href="/delete?what=hardware&id={}"> Удалить </a>'
        edit = '<a href="/edit_hardware?id={}"> Рeдактировать </a>'
        query = []
        columns = ['<b>ID</b>', '<b>ID характеристики</b>','<b>Дата выдачи</b>',
                   '<b>Владелец</b>', '<b>Удалить</b>', '<b>Редактировать</b>']
        if args['id'] != '': 
            query.append('id={}'.format(args['id']))
        if args['id_char'] != '': 
            query.append('id_char={}'.format(args['id_char']))
        if args['out_date'] != '':
            query.append('out_date = \"{}\"'.format(args['out_date']))
        if args['owner'] != '': 
            query.append('owner={}'.format(args['owner']))
            
        self.cur.execute('SELECT * FROM hardware \
        WHERE {}'.format(' AND '.join(query)))
        result = [list(i)+[delete.format(i[0]), edit.format(i[0])] for i in self.cur.fetchall()]
        data = [tuple(columns)]+result
        return data
    
    def search_type(self, args):
        delete = '<a href="/delete?what=type&id={}"> Удалить </a>'
        edit = '<a href="/edit_type?id={}"> Рeдактировать </a>'
        query = []
        columns = ['<b>Имя</b>', '<b>Имя</b>','<b>Департамент</b>',
                   '<b>Должность</b>','<b>Дата рождения</b>','<b>Кабинет</b>',
                   '<b>Удалить</b>', '<b>Редактировать</b>']
        if args['id'] != '': 
            query.append('id ={}'.format(args['id']))
        if args['htype'] != '': 
            query.append('htype LIKE \"%{}%\"'.format(args['htype']))
        if args['producer'] != '': 
            query.append('producer LIKE \"%{}%\"'.format(args['producer']))
        if args['model'] != '': 
            query.append('model LIKE \"%{}%\"'.format(args['model']))
        if args['year'] != '': 
            query.append('year={}'.format(args['year']))
            
        self.cur.execute('SELECT * FROM type \
        WHERE {}'.format(' AND '.join(query)))
        result = [list(i)+[delete.format(i[0]), edit.format(i[0])] for i in self.cur.fetchall()]
        data = [tuple(columns)]+result
        return data
    
    def prettify_search(self, data):
        return '<table><tr><td>{} </td></tr></table>'.format(
            '</td></tr><tr><td>'.join(
                ['</td><td>'.join(str(x) for x in i) for i in data]
            ))

db = DB()

@app.route('/',  methods=['GET'])
def index():
    if request.args:
        try:
            result = db.prettify_search(db.search(request.args))
            return render_template('index.html', result=result)
        except:
            return render_template('index.html',result='Что-то пошло не так или ваш запрос пуст.')
    return render_template('index.html',result='')

@app.route('/add',  methods=['GET'])
def add():
    if request.args:
        if request.args['what'] == 'workers':
            db.create_worker(request.args['name'], request.args['department'], request.args['position'], 
                             request.args['birth'], request.args['office'])
        elif request.args['what'] == 'hardware':
            db.create_hardware(request.args['id_char'], request.args['out_date'], request.args['owner'])
        elif request.args['what'] == 'type':
            db.create_type(request.args['htype'], request.args['producer'], request.args['model'],
                       request.args['year'])
        return render_template('add.html', result=['Результат успешно добавлен'])
    return render_template('add.html',result='')

@app.route('/exact',  methods=['GET'])
def exact():
    if request.args:
        if request.args['what'] == 'workers':
            result = db.prettify_search(db.search_workers(request.args))
        elif request.args['what'] == 'hardware':
            result = db.prettify_search(db.search_hardware(request.args))
        elif request.args['what'] == 'type':
            result = db.prettify_search(db.search_type(request.args))
        return render_template('exact.html', result=result)
    return render_template('exact.html',result='')

@app.route('/delete',  methods=['GET'])
def delete():
    if request.args:
        print (request.args)
        if True: #try:
            if request.args['what'] == 'workers':
                db.delete_workers(request.args['id'])
            elif request.args['what'] == 'hardware':
                db.delete_hardware(request.args['id'])
            elif request.args['what'] == 'type':
                db.delete_type(request.args['id'])
        else: #except:
            return redirect('/exact')
        return redirect('/exact')
    return redirect('/exact')

@app.route('/edit_hardware',  methods=['GET'])
def edit_hardware():
    if request.args:
        if 'base' in request.args:
            db.update_hardware(request.args)
            return redirect('/exact') 
        else:
            args = {i:request.args[i] for i in request.args}
            db.cur.execute('SELECT id_char, owner, out_date  FROM hardware WHERE id={}'.format(args['id']))
            result = db.cur.fetchone()
            args['id_char'] = result[0]
            args['owner'] = result[1]
            args['out_date'] = str(result[2])
            print (args)
            return render_template('edit_hardware.html', args=args)
    return redirect('/exact')

@app.route('/edit_workers',  methods=['GET'])
def edit_workers():
    if request.args:
        if 'base' in request.args:
            db.update_workers(request.args)
            return redirect('/exact') 
        else:
            args = {i:request.args[i] for i in request.args}
            db.cur.execute('SELECT name, department, position, birth, office  FROM workers WHERE id={}'.format(args['id']))
            result = db.cur.fetchone()
            args['name'] = '"'+result[0] + '"'
            args['department'] = '"'+result[1]+'"'
            args['position'] = '"'+result[2]+'"'
            args['birth'] = str(result[3])
            args['office'] = result[4]
            print (args)
            return render_template('edit_workers.html', args=args)
    return redirect('/exact')

@app.route('/edit_type',  methods=['GET'])
def edit_type():
    if request.args:
        if 'base' in request.args:
            db.update_type(request.args)
            return redirect('/exact') 
        else:
            args = {i:request.args[i] for i in request.args}
            db.cur.execute('SELECT htype, producer, model, year  FROM type WHERE id={}'.format(args['id']))
            result = db.cur.fetchone()
            args['htype'] = '"'+result[0]+'"'
            args['producer'] = '"'+result[1]+'"'
            args['model'] = '"'+result[2]+'"'
            args['year'] = result[3]
            print (args)
            return render_template('edit_type.html', args=args)
    return redirect('/exact')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
