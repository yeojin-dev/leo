import os

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_from_directory,
)
from pymongo import MongoClient
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')
ALLOWED_EXTENSIONS = {'html'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = MongoClient('localhost', 27017)
db = client.leo


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/homework/<string:author>/<string:title>', methods=['POST'])
def upload_homework(author, title):
    homework_name = {'title': title, 'author': author}

    if file := request.files.get('file'):
        filename = secure_filename(f'{author}_{title}_{file.filename}')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
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
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
