from flask import Flask
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

#client = MongoClient('localhost', 27017)
#client = MongoClient('mongodb://test:test@localhost', 27017)

db = client.soccer


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

# @app.route('/soccer-when', methods=['POST'])
# def get_soccer():  # put application's code here
#     when = request.form['when']
#     soccer_team = list(db.soccer.find({'when':when}, {'_id':False}))
#     #soccer_team = list(db.soccer.find({'status': 0}, {'_id': False}))
#     print(soccer_team)
#     return jsonify({'msg': '등록됨', 'when':soccer_team})
#
# #post
# @app.route('/soccer-board', methods=['POST'])
# def post_soccer():  # put application's code here
#     #user 이름을 unique, id 없음
#
#     title = request.form['title']
#     description = request.form['description']
#     when = request.form['when']
#     where = request.form['where']
#     user = request.form['user']
#     is_matched=request.form['is_matched']
#     match=request.form['match']
#
#     doc = {
#         'title': title,
#         'description': description,
#         'user':user,
#         'when': when,
#         'where': where,
#         'is_matched': is_matched,
#         'match': match,
#         'comment': None,
#         'status': 0
#     }
#
#     db.soccer.insert_one(doc)
#     print(doc)
#
#     return jsonify({'msg': '등록됨'})
#
#
#
#
# #Detail
#
# @app.route('/detail/', methods=['GET'])
# def homework(num=None):
#     orders = list(db.orders.find({}, {'_id': False}))
#     result = dict()
#
#     print(request.args.get('num'))
#     temp = request.args.get('num')
#     text = request.args.get('text')
#
#     #return jsonify({'result': 'success', 'orders': orders})
#     return render_template('index.html',orders = orders, result = result, num = temp, text=text)
#
# @app.route('/order', methods=['POST'])
# def save_order():
#     name_receive = request.form['name_give']
#     # count_receive = request.form['count_give']
#     # age_receive = request.form['age_give']
#     # address_receive = request.form['address_give']
#     # date_receive = request.form['date_give']
#     text_receive = request.form['text_give']
#
#     doc = {
#         'name': name_receive,
#         # 'count': count_receive,
#         # 'age': age_receive,
#         # 'address': address_receive,
#         # 'date': date_receive,
#         'text': text_receive
#     }
#     db.orders.insert_one(doc)
#     return jsonify({'result': 'success', 'msg':  f'{name_receive} 저장완료 !'})


# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5000, debug=True)
