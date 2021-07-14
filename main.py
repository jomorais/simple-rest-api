from flask import Flask, request, jsonify, render_template

from api.api import Api

app = Flask(__name__)


api = Api()


@app.route('/')
def home():
    return render_template('index.html', name='simple-rest-api')


@app.route('/register_device', methods=["POST"])
def register_device():
    return api.register_device(request.json)


@app.route('/unregister_device', methods=["DELETE"])
def unregister_device():
    return api.unregister_device(request.json)


@app.route('/query_device', methods=["GET"])
def query_device():
    return api.query_device(request.json)


@app.route('/install_device', methods=["POST"])
def install_device():
    return api.install_device(request.json)


app.run(host='localhost', port=8989)

