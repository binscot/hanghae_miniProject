from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
db = client.dbsparta_plus_week4


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        msg = request.args.get("msg")
        return render_template('login.html', msg=msg)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/main')
def login():
    msg = request.args.get("msg")
    return render_template('index.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "profile_name": username_receive,  # 프로필 이름 기본값은 아이디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

#보여주기
@app.route('/main')
def hello_world():

    soccer_team = list(db.soccer.find({'status': 0}, {'_id': False}))

    dict_f = dict()
    first = list()
    for i in range(1, 8):
        dict_f = dict()
        dict_f['day'] = str(i)
        first.append(dict_f)
    second = list()
    for i in range(8, 15):
        dict_f = dict()
        dict_f['day'] = str(i)
        second.append(dict_f)
    third = list()
    for i in range(15, 22):
        dict_f = dict()
        dict_f['day'] = str(i)
        third.append(dict_f)
    fourth = list()
    for i in range(22, 29):
        dict_f = dict()
        dict_f['day'] = str(i)
        fourth.append(dict_f)
    fifth = list()
    for i in range(29, 32):
        dict_f = dict()
        dict_f['day'] = str(i)
        fifth.append(dict_f)
    #first = [{'day':1}, {'day':2}]
    return render_template('soccer2.html', soccer= soccer_team , first = first, second=second, third = third , fourth = fourth , fifth=fifth)






if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
