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

# client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
client = MongoClient('52.79.249.185', 27017, username="test", password="test")
db = client.dbsparta_plus_week4


# 로그인 화면
@app.route('/')
def home():
    # 쿠키에서 토큰 받기
    token_receive = request.cookies.get('mytoken')
    # 받아서 jwt인증
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('soccer.html')
    # 시간이 지났거나 인증이 안  주소창에 로그인 시간만료 띄어주기
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    # 토큰이 없으면
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# 로그인 페이지
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


# 매치 삭제하기
@app.route('/api/delete_match', methods=['POST'])
def delete_match():
    # 클라이언트에게 이름 받아오기
    name_receive = request.form["name_give"]
    # 받아온 이름을 db에서 찾아 삭제하기
    db.orders.delete_one({"name": name_receive})
    # 성공하면 매치삭제 알럿 띄어주기
    return jsonify({'result': 'success', 'msg': f'매치{name_receive}삭제'})


# 로그인
@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 아이디 비밀번호 받기
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    # 암호화된 비밀번호 확인
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # db에서 찾기
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})
    # 디비에서 찾았을때 id와 로그인 시간을 담은 jwt 토큰 전송
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


# 회원가입
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    # 아이디, 비밀번호 받기
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    # 비밀번호 암호화 해서 db에 저장
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "profile_name": username_receive,  # 프로필 이름 기본값은 아이디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# 회원가입 시 아이디 중복확인
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    # 아이디 받아오기
    username_receive = request.form['username_give']
    # 받아온 아이디로 db에서 검색 -> 못찾을 시 성공
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# @app.route('/main')
# def login():
#     msg = request.args.get("msg")
#     return render_template('index.html', msg=msg)

# 보여주기
@app.route('/main')
def hello_world():
    # DB에서 축구팀 내용 전체 불러오기
    soccer_team = list(db.orders.find({'status': 0}, {'_id': False}))
    # 달력 만들어서 날짜별로 매칭팀 보여주기 -> 삭제
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
    # jinja2 template으로 내용보내기
    return render_template('soccer.html', soccer=soccer_team, first=first, second=second, third=third, fourth=fourth,
                           fifth=fifth)


@app.route('/detailtest/<name>', methods=['GET'])
def detail_test(name=None):
    # 주소에서 값 받아와서 매칭팀 보여주기
    soccer_team = db.orders.find_one({'name': name}, {'_id': False})
    print(soccer_team)
    # 각 팀마다 디테일정보 보내기
    return render_template('detail_test.html', soccer_team=soccer_team)


# 등록된 데이터들을 db에서 불러오기
@app.route('/detail')
def homework():
    # db에서 등록받은 정보 모두 가져오기
    orders = list(db.orders.find({}, {"_id": False}))
    # soc 라는 변수에 정보 저장 후 보냄
    return render_template('detail.html', soc=orders)


# 등록페이지에서 값들을 받아서 db에 저장
@app.route('/order', methods=['POST'])
def save_order():
    name_receive = request.form['name_give']
    count_receive = request.form['count_give']
    age_receive = request.form['age_give']
    address_receive = request.form['address_give']
    date_receive = request.form['date_give']
    phone_receive = request.form['phone_give']
    text_receive = request.form['text_give']

    # 입력받은 값들을 doc에 저장
    doc = {
        'name': name_receive,
        'count': count_receive,
        'age': age_receive,
        'address': address_receive,
        'date': date_receive,
        'phone': phone_receive,
        'text': text_receive,
        'status': 0,  # 하림 추가
        'is_matched': 0,
        'match': None
    }
    # db orders에 doc 데이터 저장
    db.orders.insert_one(doc)
    # 등록을 눌렀을 때 메세지 전달
    return jsonify({'result': 'success', 'msg': '매칭 등록 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
