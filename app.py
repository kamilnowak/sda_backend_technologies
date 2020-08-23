from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        "name": "Pizzeria",
        "items": [
            {"name": "pizza 1", "price": 19.90},
            {"name": "pizza 2", "price": 19.90},
            {"name": "pizza 3", "price": 19.90},
        ]
    },
    {
        "name": "Pizzeria 2",
        "items": [],
    },
]


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/template')
def home_page_template():
    return render_template('example.html', stores=stores)


@app.route('/store')
def get_stores():
    if request.headers.environ.get('CONTENT_TYPE') == 'application/json':
        return jsonify({"stores": stores})
    return render_template('example.html', stores=stores)


@app.route('/store', methods=['POST'])
def store():
    data = {
        'name': request.get_json()['name'],
        'items': []
    }
    stores.append(data)
    return jsonify({"stores": stores})


@app.route('/store/<string:name>')
def get_store(name):
    for item in stores:
        if item['name'] == name:
            return jsonify(item)
    return 'Cannot find store', 404


@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for item in stores:
        if item['name'] == name:
            return jsonify(item['items'])
    return 'Cannot find store', 404


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    data = request.get_json()
    for st in stores:
        if st['name'] == name:
            st['items'].append({
                'name': data['name'],
                'price': data['price']
            })
            return jsonify({"stores": stores})



if __name__ == '__main__':
    app.run()
