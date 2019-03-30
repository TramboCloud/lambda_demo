#!/usr/bin/python
import json
import boto3

def lambda_handler(event, context):
    S3_OBJECT = event['Records'][0]['s3']

    S3_KEY = S3_OBJECT['object']['key']
    S3_BUCKET    = S3_OBJECT['bucket']['name']

    print S3_BUCKET
    print S3_KEY

    s3 = boto3.resource('s3')

    obj = s3.Object(S3_BUCKET, S3_KEY)
    FILE_CONTENT = obj.get()['Body'].read().decode('utf-8')

    attributes = eval(FILE_CONTENT)

    image_id        = attributes['image_id']
    count           = attributes['count']
    subnet_id       = attributes['subnet_id']
    instance_type   = attributes['instance_type']
    name            = attributes['name']

    ec2 = boto3.resource('ec2')

    instance = ec2.create_instances(
        ImageId=image_id,
        MaxCount=count,
        MinCount=1,
        InstanceType=instance_type,
        SubnetId=subnet_id,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': name
                    }
                ]
            }
        ]
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Instance launched successfully!')
    }
