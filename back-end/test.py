import MySQLdb
import config

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