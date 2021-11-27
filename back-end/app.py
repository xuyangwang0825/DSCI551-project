import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
from flask import *
from processor.AIDetector_pytorch import Detector
import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET
import core.main
from werkzeug.utils import secure_filename
from aws.upload_file_to_s3 import upload_file_to_s3
from utils.video2frame import get_first_frame

UPLOAD_FOLDER = r'./uploads'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'mp4'])
app = Flask(__name__)
app.secret_key = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

werkzeug_logger = rel_log.getLogger('werkzeug')
werkzeug_logger.setLevel(rel_log.ERROR)

# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='./index.html'))


# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     file = request.files['file']
#     print(datetime.datetime.now(), file.filename)
#     if file and allowed_file(file.filename):
#         src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(src_path)
#         shutil.copy(src_path, './tmp/ct')
#         image_path = os.path.join('./tmp/ct', file.filename)
#         pid, image_info = core.main.c_main(
#             image_path, current_app.model, file.filename.rsplit('.', 1)[1])
#         return jsonify({'status': 1,
#                         'image_url': 'http://127.0.0.1:5003/tmp/ct/' + pid,
#                         'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
#                         'image_info': image_info})

#     return jsonify({'status': 0})

@app.route("/upload", methods=['GET', "POST"])
def upload_file():

    # B
    file = request.files["file"]
    # print(file.filename)
    """
        These attributes are also available
        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype
    """
    # C.
    if file.filename == "":
        return "Please select a file"

    # D.
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)

        # upload video to s3
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        file.save(src_path)

        output = upload_file_to_s3(s3, src_path, file.filename, S3_BUCKET)
        print(output)
        # get first frame of video
        video_oath = src_path
        src_path = src_path[:-3] + 'jpg'
        get_first_frame(src_path, video_oath)

        img_name = file.filename[:-3] + 'jpg'
        shutil.copy(src_path, './tmp/ct')
        image_path = os.path.join('./tmp/ct', img_name)
        pid, image_info = core.main.c_main(
            image_path, current_app.model, img_name.rsplit('.', 1)[1])
        return jsonify({'status': 1,
                        'image_url': 'http://127.0.0.1:5003/tmp/ct/' + pid,
                        'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
                        'image_info': image_info})

    return jsonify({'status': 0})


@app.route("/download", methods=['GET'])
def download_file():
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    return send_from_directory('data', 'testfile.zip', as_attachment=True)


# show photo
@app.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    if request.method == 'GET':
        if not file is None:
            image_data = open(f'tmp/{file}', "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response


if __name__ == '__main__':

    #connect to s3
    s3 = boto3.client(
        "s3",
        aws_access_key_id=S3_KEY,
        aws_secret_access_key=S3_SECRET
    )

    files = [
        'uploads', 'tmp/ct', 'tmp/draw',
        'tmp/image', 'tmp/mask', 'tmp/uploads'
    ]
    for ff in files:
        if not os.path.exists(ff):
            os.makedirs(ff)
    with app.app_context():
        current_app.model = Detector()
    app.run(host='127.0.0.1', port=5003, debug=True)
