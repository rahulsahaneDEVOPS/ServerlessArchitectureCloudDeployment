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