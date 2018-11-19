from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/',  methods=['GET'])
def index():
    if request.args:
        args = dict(request.args)
        print (args)
        for i in args: args[i] = '"'+args[i][0].upper()+'"'
        return render_template('index.html',result='Нормас', args = args)
    return render_template('index.html',result='', args = {})


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
