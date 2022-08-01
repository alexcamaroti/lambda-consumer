import json
import boto3
import requests
import urllib3

QUEUE_URL = 'http://host.docker.internal:4566/000000000000/open_diff_queue'
SQS_MAX_NUMBER_OF_MESSAGES: int = 3
URL_API = "http://192.168.1.190:8080/diff"



sqs = boto3.client('sqs',
                   endpoint_url='http://host.docker.internal:4566',
                   aws_access_key_id="secret-id",
                   aws_secret_access_key="secret-key",
                   region_name='sa-east-1')


def lambda_handler(event, context):
    # mock_messages_in_sqs()
    messages = receive_messages()
    print(messages)
    response = requests.post(url=URL_API, json=json.loads('{"primeiroRegistro" : "hai","segundoRegistro" : "hey", "terceiroRegistro" : "hoi"}'))
    print(response)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello universe 2",
            # "location": ip.text.replace("\n", "")
        }),
    }


def mock_messages_in_sqs() -> None:
    first_response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody='"Diffs": { "abertos": { "nome": "nome novo" }}')

    print(first_response)

    second_response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody='"Diffs": { "abertos": { }}')

    print(second_response)
    return


def receive_messages() -> []:
    # Receive message from SQS queue
    messages = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        AttributeNames=['All'],
        MaxNumberOfMessages=SQS_MAX_NUMBER_OF_MESSAGES,
        MessageAttributeNames=['All'],
        VisibilityTimeout=45,  # The duration (in seconds) that the received messages are hidden from subsequent
        # retrieve requests after being retrieved by a ReceiveMessage request.

        WaitTimeSeconds=5  # The duration (in seconds) for which the call waits for a message to arrive in the
        # queue before returning. If a message is available, the call returns sooner than
        # WaitTimeSeconds. If no messages are available and the wait time expires, the call
        # returns successfully with an empty list of messages.
    )

    return messages
