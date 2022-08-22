import os
from yt_dlp import YoutubeDL
import boto3

s3 = boto3.resource('s3')
bucket_name = os.environ['BUCKET_NAME']


def main():
    print('worker is up!')
    while True:
        messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )
        for msg in messages:
            with YoutubeDL() as ydl:
                video = ydl.extract_info(msg.body, download=True)
                filename = ydl.prepare_filename(video)
                s3.meta.client.upload_file(filename, bucket_name, filename)

            # delete message from the queue after is was handled
            queue.delete_messages(Entries=[{
                'Id': msg.message_id,
                'ReceiptHandle': msg.receipt_handle
            }])


if __name__ == '__main__':
    sqs = boto3.resource('sqs', region_name=os.environ['AWS_REGION'])
    queue = sqs.get_queue_by_name(QueueName=os.environ['QUEUE_NAME'])
    main()

