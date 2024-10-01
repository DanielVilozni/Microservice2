import boto3
import time
import os

# Initialize AWS clients for SQS and S3
sqs = boto3.client('sqs')
s3 = boto3.client('s3')

# SQS queue URL and S3 bucket name from environment variables
QUEUE_URL = os.getenv('QUEUE_URL')
BUCKET_NAME = os.getenv('BUCKET_NAME')

# Poll messages from SQS and upload to S3
def process_messages():
    while True:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )
        
        messages = response.get('Messages', [])
        
        for message in messages:
            # Extract message body
            email_data = message['Body']

            # Create a unique key for S3 upload (e.g., using timestamp)
            s3_key = f"email_{time.time()}.json"
            
            # Upload the message to S3
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=s3_key,
                Body=email_data
            )
            
            # Delete the message from the queue after processing
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )

        time.sleep(30)  # Poll every 30 seconds

if __name__ == '__main__':
    process_messages()
