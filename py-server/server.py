from flask import Flask
from flask import send_file, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/isTheServiceOn')
def serviceOn():
    return jsonify({
        "serviceOn": True
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0') # this is for docker to work