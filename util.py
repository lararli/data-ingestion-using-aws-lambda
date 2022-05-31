import boto3
from credentials import aws_access_key_id, aws_secret_access_key
import os 

def get_client():
    return boto3.client('s3',aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def upload_s3(body, bucket, file):
    s3_client = get_client()
    res = s3_client.put_object(
        Bucket=bucket,
        Key=file,
        Body=body
    )
    return res