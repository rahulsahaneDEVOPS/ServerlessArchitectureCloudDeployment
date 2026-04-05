# Assignment 3: Monitor S3 Bucket Encryption Using AWS Lambda

## Objective
The objective of this assignment is to monitor S3 bucket encryption and identify buckets that are not using stronger encryption methods like SSE-KMS.

---

## Services Used
- AWS S3  
- AWS Lambda  
- AWS IAM  
- Python (Boto3)

---

## Steps Performed

### Step 1: S3 Bucket Setup
Created multiple S3 buckets for testing:
- Some buckets using default encryption (SSE-S3)
- Some buckets using KMS encryption (SSE-KMS)

---

### Step 2: IAM Role
Created an IAM role named `lambda-s3-encryption-check-role` and attached the required permissions.

- Policy: AmazonS3ReadOnlyAccess

---

### Step 3: Lambda Function
Created a Lambda function with Python runtime and attached the IAM role.

- Function Name: s3-encryption-check  
- Runtime: Python 3.x  

---

### Step 4: Lambda Code
Wrote a Python script using Boto3 to:
- List all S3 buckets  
- Check encryption configuration  
- Identify buckets using SSE-S3 and SSE-KMS  
- Print results in logs  

---

## Code

```python
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

        except Exception:
            print(f"No encryption configuration found for bucket: {bucket_name}")

   print("Encryption check completed")
```

---

### Step 5: Execution Result

Ran the Lambda function using the Test option.

Logs showed:

Bucket names being checked
Identification of SSE-S3 buckets (less secure)
Identification of SSE-KMS buckets (more secure)

---

### Step 6: Result

After execution:

Buckets using weaker encryption (SSE-S3) were identified
Buckets using stronger encryption (SSE-KMS) were identified
Note

AWS now enables default encryption (SSE-S3) for all newly created S3 buckets. Because of this, it is not possible to create completely unencrypted buckets.

Therefore, instead of detecting unencrypted buckets, this assignment focuses on identifying buckets not using stronger encryption like SSE-KMS.

---

### Conclusion

This assignment demonstrates how AWS Lambda and Boto3 can be used to monitor S3 bucket encryption and improve overall security by identifying buckets that are not using stronger encryption methods.

---

### Author:
Rahul Sahane