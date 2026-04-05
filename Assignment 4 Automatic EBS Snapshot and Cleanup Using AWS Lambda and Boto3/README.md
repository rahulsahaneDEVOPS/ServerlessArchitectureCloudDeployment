# Assignment 4: Automatic EBS Snapshot and Cleanup Using AWS Lambda and Boto3

## Objective
To automate the creation of EBS snapshots and delete old snapshots to optimize storage cost.

---

## 🛠️ Services Used
- AWS EC2 (EBS Volume)
- AWS Lambda
- AWS IAM
- Boto3 (Python SDK)

---

## Project Overview

This project automates:
- Creation of EBS snapshots
- Deletion of old snapshots based on retention period

A Lambda function is used to:
1. Create a snapshot of the specified EBS volume
2. Fetch all snapshots of the volume
3. Delete snapshots older than the defined retention period

---

## Implementation Steps

### Step 1: EBS Volume Setup
- Created an EBS volume (8GB) for testing

---

### Step 2: IAM Role
- Created IAM Role for Lambda  
- Attached policy: `AmazonEC2FullAccess`

---

### Step 3: Lambda Function
- Function Name: `ebs-snapshot-cleanup`  
- Runtime: Python 3.x  

---

### Step 4: Lambda Code

```python
import boto3
from datetime import datetime, timedelta, timezone

ec2 = boto3.client('ec2')

VOLUME_ID = 'vol-015470621a081c07e'

def lambda_handler(event, context):

    print("Starting snapshot process...")

    # Create snapshot
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description='Automated snapshot'
    )

    snapshot_id = snapshot['SnapshotId']
    print(f"Created snapshot: {snapshot_id}")

    # Get snapshots
    snapshots = ec2.describe_snapshots(
        Filters=[{'Name': 'volume-id', 'Values': [VOLUME_ID]}]
    )

    for snap in snapshots['Snapshots']:
        start_time = snap['StartTime']
        age = datetime.now(timezone.utc) - start_time

        print(f"Snapshot {snap['SnapshotId']} age: {age}, state: {snap['State']}")

        # 1 minute retention (for testing)
        if snap['State'] == 'completed' and age > timedelta(minutes=1):
            old_id = snap['SnapshotId']
            print(f"Deleting snapshot: {old_id}")
            ec2.delete_snapshot(SnapshotId=old_id)

   print("Process completed")
```

---

Execution
Lambda function was triggered manually using Test event
Execution logs confirmed:
Snapshot creation
Old snapshot deletion

---

Screenshots
01-ebs-volume-created.png
02-iam-role.png
03-lambda-function.png
04-lambda-code.png
05-ebs-snapshot-created.png
06-lambda-execution-logs.png

---

Note

For testing purposes, a shorter retention period (1 minute) was used instead of 30 days to quickly validate the snapshot cleanup functionality and avoid additional storage costs.

During each execution:

A new snapshot is created
Newly created snapshot is not deleted (because it is recent and pending)
Only older completed snapshots are deleted

---

Conclusion:

This assignment demonstrates how AWS Lambda and Boto3 can be used to automate EBS snapshot creation and cleanup.

It helps in:

Efficient backup management
Cost optimization by removing outdated snapshots

Additionally, this solution can be extended using Amazon EventBridge (CloudWatch Events) to schedule automated backups.

Future Enhancement
Schedule Lambda using EventBridge (weekly/daily backup)
Add tagging for snapshots
Implement more secure IAM policies instead of full access