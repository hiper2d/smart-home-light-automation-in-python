import os.path

from flask import Flask, make_response, render_template
from flask_cors import CORS

template_dir = os.path.abspath('static')
app = Flask(__name__, template_folder=template_dir, static_url_path='', static_folder=template_dir)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/api/echo', methods=['GET'])
def get_devices():
    return make_response("echo", 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)