import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
from flask import *
from processor.AIDetector_pytorch import Detector
import boto3, botocore
import config
import MySQLdb
import core.main
import pymongo
from werkzeug.utils import secure_filename
from aws.upload_file_to_s3 import upload_file_to_s3
from utils.video2frame import get_first_frame
import pyspark as spark

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

@app.route("/upload_csv", methods=['GET', "POST"])
def upload_csv():

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
    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1] == 'json':
        file.filename = secure_filename(file.filename)

        # upload video to s3
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        file.save(src_path)

        # metadata
        file_name = file.filename
        json_s3_url = upload_file_to_s3(s3, src_path, file.filename, config.S3_BUCKET)
        file_size = str(round(os.path.getsize(src_path) / float(1024*1024), 2)) + ' mb'

        videos = mycol.find({}, ["id", "createTime", "diggCount", "shareCount", "playCount", "commentCount"])

        # spark version
        # videos = spark.read.json('./uploads/trending.json')
        # videos = video_info[["id", "createTime", "diggCount", "shareCount", "playCount", "commentCount"]]

        video_info = {}
        cnt = 0
        for video in videos:
            # print(video)
            # insert_video_info = (
            #     "insert into video_csv_detail_info (id, createTime, diggCount, shareCount, playCount, commentCount)"
            #     "values (%s, %s, %s, %s, %s, %s)"
            # )
            # # print(int(video["id"]), int(video["createTime"]), int(video["diggCount"]), int(video["shareCount"]), int(video["playCount"]), int(video["commentCount"]))
            # cursor.execute(insert_video_info, (int(video["id"]), int(video["createTime"]), int(video["diggCount"]), int(video["shareCount"]), int(video["playCount"]), int(video["commentCount"])))
            # db.commit()
            cnt += 1
            v = [int(video["id"]), int(video["createTime"]), int(video["diggCount"]), int(video["shareCount"]), int(video["playCount"]), int(video["commentCount"])]
            video_info[int(video["id"])] = v
            if cnt > 50:
                break

        # print(video_info)

        return jsonify({'file_name': file_name,
                        'json_s3_url': json_s3_url,
                        'file_size': file_size,
                        'video_info': video_info})

    return jsonify({'status': 0})

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

        video_s3_url = upload_file_to_s3(s3, src_path, file.filename, config.S3_BUCKET)

        # get first frame of video
        video_oath = src_path
        src_path = src_path[:-3] + 'jpg'
        get_first_frame(src_path, video_oath)

        img_name = file.filename[:-3] + 'jpg'
        shutil.copy(src_path, './tmp/ct')
        image_path = os.path.join('./tmp/ct', img_name)
        result_path = os.path.join('./tmp/draw', img_name)
        pid, image_info = core.main.c_main(
            image_path, current_app.model, img_name.rsplit('.', 1)[1])

        file_size = str(round(os.path.getsize(video_oath) / float(1024*1024), 2)) + ' mb'
        # insert record into rds
        insert_video_info = (
            "insert into video_info (video_name, video_s3_path, pic_s3_path, result_s3_path, content_type, content_length, mimetype)"
            "values (%s, %s, %s, %s, %s, %s, %s)"
        )
        cursor.execute(insert_video_info, (file.filename, video_s3_url, image_path, result_path, str(file.content_type), file_size, str(file.mimetype)))
        db.commit()

        for k, v in image_info.items():
            recommend_url = "www.amazon.com/s?k=" + k.split("-")[0]
            image_info[k].append(recommend_url)

        # print(image_info)

        return jsonify({'status': 1,
                        'image_url': 'http://127.0.0.1:5003/tmp/ct/' + pid,
                        'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
                        'image_info': image_info})

    return jsonify({'status': 0})

@app.route("/get_video_info", methods=['GET'])
def get_video_info():
    get_video_info = (
        "select video_name, video_s3_path, content_type, content_length from video_info"
    )
    cursor.execute(get_video_info)
    data = cursor.fetchall()

    return jsonify({'video_info': data})

@app.route("/get_video_result_detail", methods=['GET', 'POST'])
def get_video_result_detail():

    video_name = request.form.get('video_name')
    # print(video_name)
    img_name = video_name[:-3] + 'jpg'
    image_path = os.path.join('./tmp/ct', img_name)
    result_path = os.path.join('./tmp/draw', img_name)
    pid, image_info = core.main.c_main(
        image_path, current_app.model, img_name.rsplit('.', 1)[1])

    for k, v in image_info.items():
        recommend_url = "www.amazon.com/s?k=" + k.split("-")[0]
        image_info[k].append(recommend_url)

    # print(image_info)

    return jsonify({'status': 1,
                    'image_url': 'http://127.0.0.1:5003/tmp/ct/' + pid,
                    'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
                    'image_info': image_info})

@app.route("/get_json_detail", methods=['GET', 'POST'])
def get_json_detail():

    # metadata
    filename = 'trending.json'
    src_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    json_s3_url = "{}{}".format(config.S3_LOCATION, filename)
    file_size = str(round(os.path.getsize(src_path) / float(1024*1024), 2)) + ' mb'

    videos = mycol.find({}, ["id", "createTime", "diggCount", "shareCount", "playCount", "commentCount"])

    # spark version
    # videos = spark.read.json('./uploads/trending.json')
    # videos = video_info[["id", "createTime", "diggCount", "shareCount", "playCount", "commentCount"]]


    video_info = {}
    cnt = 0
    for video in videos:
        # print(video)
        # insert_video_info = (
        #     "insert into video_csv_detail_info (id, createTime, diggCount, shareCount, playCount, commentCount)"
        #     "values (%s, %s, %s, %s, %s, %s)"
        # )
        # # print(int(video["id"]), int(video["createTime"]), int(video["diggCount"]), int(video["shareCount"]), int(video["playCount"]), int(video["commentCount"]))
        # cursor.execute(insert_video_info, (int(video["id"]), int(video["createTime"]), int(video["diggCount"]), int(video["shareCount"]), int(video["playCount"]), int(video["commentCount"])))
        # db.commit()
        # cnt += 1
        v = [int(video["id"]), int(video["createTime"]), int(video["diggCount"]), int(video["shareCount"]), int(video["playCount"]), int(video["commentCount"])]
        video_info[int(video["id"])] = v
        if cnt > 50:
            break

    # print(video_info)

    return jsonify({'file_name': filename,
                    'json_s3_url': json_s3_url,
                    'file_size': file_size,
                    'video_info': video_info})

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

    # connect to s3
    s3 = boto3.client(
        "s3",
        aws_access_key_id=config.S3_KEY,
        aws_secret_access_key=config.S3_SECRET
    )

    # connect to MongoDB / AWS DocumentsDB
    myclient = pymongo.MongoClient(config.MONGO_HOST)
    mydb = myclient[config.MONGO_DB]
    mycol = mydb[config.MONGO_COL]

    # connect to rds
    db = MySQLdb.connect(host=config.HOST,
                            port=config.PORT,
                            user=config.USER,
                            passwd=config.PASSWD,
                            db=config.DB,
                            charset=config.CHARSET)

    cursor = db.cursor()

    # test
    # cursor.execute("SELECT * FROM video")
    # print(cursor.fetchone()[0])

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
