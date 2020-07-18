import os

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_from_directory,
)
from flask.cli import load_dotenv
from pymongo import MongoClient
from werkzeug.utils import secure_filename

app = Flask(__name__)
load_dotenv()

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']
UPLOAD_PASSWORD = os.environ['UPLOAD_PASSWORD']
ALLOWED_EXTENSIONS = {'html'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_PASSWORD'] = UPLOAD_PASSWORD

if os.environ.get('FLASK_ENV') == 'test':
    client = MongoClient(os.environ['MONGO_TEST_CLIENT_URI'], 27017)
    db_name = os.environ['MONGO_TEST_DB_NAME']
else:
    client = MongoClient(os.environ['MONGO_CLIENT_URI'], 27017)
    db_name = os.environ['MONGO_DB_NAME']
db = getattr(client, db_name)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/homework/<string:author>/<string:title>', methods=['POST'])
def upload_homework(author, title):
    homework_name = {'title': title, 'author': author}

    if file := request.files.get('file'):
        filename = secure_filename(f'{author}_{title}_practice.html')
        filepath = os.path.join(BASE_FOLDER, app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        db.homework.update(homework_name, {'$set': {'filepath': filepath}})
        result = {'result': 'success', 'msg': '숙제가 성공적으로 등록되었습니다.'}

    else:
        result = {'result': 'fail', 'msg': '숙제 파일이 없습니다.'}

    return jsonify(result)


@app.route('/homework', methods=['POST'])
def submit_homework():
    title_receive = request.form['title_give']
    author_receive = request.form['author_give']
    password_receive = request.form['password_give']

    if password_receive != app.config['UPLOAD_PASSWORD']:
        return jsonify({'result': 'fail', 'msg': '비밀번호가 틀렸습니다.'})

    homework_name = {'title': title_receive, 'author': author_receive}

    db.homework.update_one(homework_name, {'$set': homework_name}, upsert=True)
    return jsonify({'result': 'success', 'msg': '숙제가 성공적으로 등록되었습니다.'})


@app.route('/homework', methods=['GET'])
def read_homework():
    homework = list(db.homework.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'homework': homework})


@app.route('/homework/<string:author>/<string:title>', methods=['GET'])
def get_homework(author, title):
    homework_name = {'title': title, 'author': author}
    homework = db.homework.find_one(homework_name)
    filename = homework.get('filepath').split('/')[-1]
    return send_from_directory(os.path.join(BASE_FOLDER, app.config['UPLOAD_FOLDER']), filename)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
