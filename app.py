from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json()
    # обработка запроса
    res = {
        "version": req['version'],
        "session": req['session'],
        "response": {
            "text": "Hello, world!",
            "end_session": False
        }
    }
    return jsonify(res)

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
