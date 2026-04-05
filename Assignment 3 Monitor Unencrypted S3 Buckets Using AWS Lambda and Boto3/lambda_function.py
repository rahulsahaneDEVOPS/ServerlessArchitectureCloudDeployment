import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    print("Checking S3 bucket encryption...")

    buckets = s3.list_buckets()

    for bucket in buckets['Buckets']:
        bucket_name = bucket['Name']
        print(f"Checking bucket: {bucket_name}")

        try:
            encryption = s3.get_bucket_encryption(Bucket=bucket_name)

            rules = encryption['ServerSideEncryptionConfiguration']['Rules']
            algo = rules[0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']

            if algo != 'aws:kms':
                print(f"Bucket NOT using KMS (less secure): {bucket_name}")
            else:
                print(f"Bucket using KMS (secure): {bucket_name}")

        except Exception as e:
            print(f"No encryption config found for bucket: {bucket_name}")