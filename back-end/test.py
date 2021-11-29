import MySQLdb
import config
import json
import pymongo

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
# print(cursor.fetchone())

get_video_info = (
    "select video_name, video_s3_path, content_type, content_length from video_info"
)
cursor.execute(get_video_info)
data = cursor.fetchall()
print(data)

myclient = pymongo.MongoClient(config.HOST)
mydb = myclient[config.DB]
mycol = mydb[config.Collection]

videos = mycol.find({}, ["id", "createTime", "diggCount", "shareCount", "playCount", "commentCount"])

cnt = 50

for video in videos:
    insert_video_info = (
        "insert into video_csv_detail_info (id, createTime, diggCount, shareCount, playCount, commentCount)"
        "values (%d, %d, %d, %d, %d, %d, %d)"
    )
    cursor.execute(insert_video_info, (video["id"], video["createTime"], video["diggCount"], video["shareCount"], video["playCount"], video["commentCount"]))
    db.commit()
    cnt += 1
    if cnt > 50:
        break

