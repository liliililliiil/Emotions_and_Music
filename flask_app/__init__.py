from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
from datetime import timedelta
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'User_Info'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306

app.secret_key = '9de85b1db330eddaf2a3e861d23db198baafee41a968f8365f4f9acf60fb2e09'  
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5) # 5분후 자동 로그아웃
mysql.init_app(app)

@app.route('/')
@app.route('/index')
def index():
	if not session.get('userid'):  
		return render_template('index.html'), 200
	
	#로그인 세션정보가 없을 경우
	else:		
		userid = session.get('userid') 
		return render_template('index.html', userid=userid)

@app.route('/info')
def info():
    
    return render_template('info.html'), 200

@app.route('/result', methods=["GET","POST"])
def result():
    name = session.get('username')
    
    return render_template('result.html', name=name), 200



@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        userid = request.form.get('userid')
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re_password') 
        conn = mysql.connect()
        cursor = conn.cursor()
 
        sql = "INSERT IGNORE INTO user_info VALUES ('%s', '%s', '%s')" % (userid, password, username)
        cursor.execute(sql)
 
        data = cursor.fetchall()
        
        if not data and password == re_password:
            conn.commit()
            return redirect(url_for('index'))
        else:
            conn.rollback()
            return "Register Failed"
 
        cursor.close()
        conn.close()
    return render_template('register.html'), 200


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        userid = request.form.get('userid')
        password = request.form.get('password')
        
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT userid, user_name FROM user_info WHERE userid = %s AND password = %s"
        value = (userid, password)
        cursor.execute("set names utf8")
        cursor.execute(sql, value)

        data = cursor.fetchall()
        cursor.close()
        conn.close()
        if data != ():	# 쿼리 데이터가 존재하면
            session['userid'] = userid	# userid를 session에 저장한다.
            session['username'] = data[0][1]
            return redirect('/index')
        else:
            return 'Dont Login'	# 쿼리 데이터가 없으면 출력


@app.route('/logout', methods=['GET'])
def logout():
	session.pop('userid', None)
	return redirect('/index')

@app.route('/loading', methods=['GET', 'POST'])
def loading():
    return render_template('loading.html'),200

        

