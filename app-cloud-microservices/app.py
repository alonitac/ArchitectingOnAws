import os
from flask import Flask, request, render_template
from yt_dlp import YoutubeDL
from flask import jsonify
import mysql.connector
import boto3

con = mysql.connector.connect(
    host=os.environ['SQL_HOST'],
    # host='database-3.c34a2z7p5ba9.eu-north-1.rds.amazonaws.com',
    user="root",
    password="secret1234",
    database="videos"
)

cur = con.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS videos(
        client_ip varchar(255),
        title varchar(255),
        videoId varchar(255),
        CONSTRAINT UC_video UNIQUE (client_ip, title, videoId))
    """)

app = Flask(__name__, static_url_path='')


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/youtube", methods=['POST'])
def get_youtube():
    client_ip = request.remote_addr
    video_name = request.json['text']

    if video_name == 'my videos':
        cur.execute(f"SELECT * FROM videos WHERE client_ip='{client_ip}'")
        data = cur.fetchall()
        return jsonify({
            'items': [{'text': t, 'videoId': i} for _, t, i in data]
        }), 200

    with YoutubeDL() as ydl:
        videos = ydl.extract_info(f"ytsearch{1}:{video_name}", download=False)['entries']

        if videos:
            response = workers_queue.send_message(MessageBody=videos[0]['webpage_url'])
            print(response)

            cur.execute(f"""INSERT IGNORE INTO videos VALUES ('{client_ip}', '{videos[0]['title']}', '{videos[0]['id']}')""")
            con.commit()

        return jsonify({
            'items': [{
                'text': videos[0]['title'] if videos else 'Video not found',
                'videoId': videos[0]['id'] if videos else ''
            }]
        }), 200


if __name__ == '__main__':
    sqs = boto3.resource('sqs', region_name=os.environ['AWS_REGION'])
    workers_queue = sqs.get_queue_by_name(QueueName=os.environ['QUEUE_NAME'])
    app.run(host='0.0.0.0', port=8080)
