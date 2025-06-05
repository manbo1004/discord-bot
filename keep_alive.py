
from flask import Flask, Response
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return Response("봇이 살아있습니다!", status=200, mimetype='text/plain')

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
