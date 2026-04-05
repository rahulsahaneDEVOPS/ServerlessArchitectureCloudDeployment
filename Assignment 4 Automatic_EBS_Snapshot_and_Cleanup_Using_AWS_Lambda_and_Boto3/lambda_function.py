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
        Filters=[{'Name': 'volume-id', 'Values': [VOLUME_ID]}],
        OwnerIds=['self']
    )

    now = datetime.now(timezone.utc)

    for snap in snapshots['Snapshots']:
        start_time = snap['StartTime']
        state = snap['State']   # 👈 IMPORTANT

        age = now - start_time

        print(f"Snapshot {snap['SnapshotId']} age: {age}, state: {state}")

        # ✅ Delete only if completed AND older than 1 min
        if state == 'completed' and age > timedelta(minutes=1):
            old_id = snap['SnapshotId']
            print(f"Deleting snapshot: {old_id}")
            
            ec2.delete_snapshot(SnapshotId=old_id)

    print("Process completed")