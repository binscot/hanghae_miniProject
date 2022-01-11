from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

#client = MongoClient('mongodb://test:test@localhost', 27017)

client = MongoClient('localhost', 27017)

db = client.dbhomework

@app.route('/')
def homework():

    orders = list(db.orders.find({}, {"_id": False}))
    return render_template('index.html', soc=orders)

@app.route('/order', methods=['POST'])
def save_order():
    name_receive = request.form['name_give']
    count_receive = request.form['count_give']
    age_receive = request.form['age_give']
    address_receive = request.form['address_give']
    date_receive = request.form['date_give']
    text_receive = request.form['text_give']

    doc = {
        'name': name_receive,
        'count': count_receive,
        'age': age_receive,
        'address': address_receive,
        'date': date_receive,
        'text': text_receive
    }
    db.orders.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '주문 완료!'})

# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    orders = list(db.orders.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'orders': orders})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5006, debug=True)