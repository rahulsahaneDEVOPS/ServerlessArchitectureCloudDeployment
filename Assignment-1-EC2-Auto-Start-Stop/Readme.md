Assignment 1: EC2 Auto Start/Stop using AWS Lambda

Objective:
The objective of this assignment is to automate the starting and stopping of EC2 instances based on tags using AWS Lambda and Boto3.

Services Used:
- Amazon EC2
- AWS Lambda
- IAM
- Python (Boto3)

Project Description:
In this project, EC2 instances are managed automatically using AWS Lambda.

If an instance has the tag "Action = Auto-Stop", it will be stopped.
If an instance has the tag "Action = Auto-Start", it will be started.

Implementation Steps:
1. Created two EC2 instances
2. Added tags (Auto-Stop and Auto-Start)
3. Created IAM role with EC2 permissions
4. Created Lambda function using Python
5. Wrote Boto3 script to control EC2 instances
6. Tested the function successfully

Lambda Code:
```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    response = ec2.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']

            tags = instance.get('Tags', [])
            for tag in tags:
                if tag['Key'] == 'Action':

                    if tag['Value'] == 'Auto-Stop':
                        print(f"Stopping instance: {instance_id}")
                        ec2.stop_instances(InstanceIds=[instance_id])

                    elif tag['Value'] == 'Auto-Start':
                        print(f"Starting instance: {instance_id}")
                        ec2.start_instances(InstanceIds=[instance_id])

    return {
        "statusCode": 200,
        "body": "Execution completed successfully"
    }
```

Output:
- Instance with Auto-Stop tag was stopped
- Instance with Auto-Start tag was running

Conclusion:
This assignment helped me understand how to automate AWS services using Lambda and Boto3.

Author:
Rahul Sahane