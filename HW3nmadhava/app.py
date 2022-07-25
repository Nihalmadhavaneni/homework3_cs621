from flask import Flask, request, render_template, redirect
import sqlite3
import uuid

app = Flask(__name__)


@app.route('/stds', methods=['GET'])
def ppl():

    ppl = sqlite3.connect('ppl.db')
    d_cur = ppl.cursor()
    d_cur.execute('select * from ppl')
    vals = d_cur.fetchall()

    return render_template('results.html', content=vals)


@app.route('/greater', methods=['GET'])
def ppl_gt():
    ppl = sqlite3.connect('ppl.db')
    d_cur = ppl.cursor()
    d_cur.execute('select * from ppl st where st.st_grade >= 85')
    vals = d_cur.fetchall()

    return render_template('results.html', content=vals)


@app.route('/update', methods=['POST'])
def ppl_update():
    ppl = sqlite3.connect('ppl.db')
    d_cur = ppl.cursor()
    if(request.method == 'POST'):
        sid = request.form['st_id']
        name = request.form['name']
        grade = request.form['grade']
        d_cur.execute("update ppl set st_name = '{0}', st_grade = {1} where stu_id = '{2}'".format(
            name, grade, sid))
        ppl.commit()
        ppl.close()
        return redirect('/', code=302)


@app.route('/delete', methods=['POST'])
def ppl_del():
    ppl = sqlite3.connect('ppl.db')
    d_cur = ppl.cursor()
    if(request.method == 'POST'):
        del_id = request.form['del']
        d_cur.execute('delete from ppl where stu_id = ?', [del_id])
        ppl.commit()
        ppl.close()
        return redirect('/',  code=302)


@app.route('/', methods=['GET', 'POST'])
def start():
    if(request.method == 'POST'):
        ppl = sqlite3.connect('ppl.db')
        d_cur = ppl.cursor()
        d_cur.execute(
            'create table if not exists ppl (stu_id varchar(255), st_name varchar(255), st_grade integer(2));')
        ppl.commit()
        del_id = uuid.uuid4()
        name = request.form['name']
        grade = request.form['grade']
        d_cur.execute("insert into ppl (stu_id, st_name, st_grade) values (?,?,?)", [str(del_id), str(name), int(grade)])
        ppl.commit()
        ppl.close()

    return render_template('Home.html')


app.run(host='localhost', port=5002, debug=True)
