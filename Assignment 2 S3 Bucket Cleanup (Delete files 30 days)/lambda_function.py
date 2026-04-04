import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 'cleanup-s3bucket-rahul'  # your correct bucket name

def lambda_handler(event, context):
    
    print("Lambda execution started")

    objects = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' not in objects:
        print("No files found in bucket")
        return

    for obj in objects['Contents']:
        key = obj['Key']
        last_modified = obj['LastModified']

        print(f"Checking file: {key}")

        # Used minutes for testing
        if last_modified < datetime.now(timezone.utc) - timedelta(minutes=1):
            print(f"Deleting file: {key}")
            s3.delete_object(Bucket=BUCKET_NAME, Key=key)

    print("Cleanup completed successfully")