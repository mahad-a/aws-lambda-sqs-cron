import json
import boto3
from datetime import datetime

# sqs queue
sqs = boto3.resource('sqs', region_name='ca-central-1')

def lambda_handler(event, context):
    queue = sqs.get_queue_by_name(QueueName="simulated_application_queue") # set the sqs queue to be the one we want to send messages to 
    
    # use the current date and time to create a unique message
    the_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"Message from Lambda sent on: {the_date}"

    # send the message to the SQS queue
    response = queue.send_message(MessageBody=message)

    return {
        'statusCode': 200, # attach a json body to confirm if successful (200 indicates success)
        'body': json.dumps(f'Message has been sent from lambda to sqs queue: {response}')
    }
