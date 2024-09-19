import boto3
from datetime import datetime, timedelta, timezone

# Initialize EC2 client
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Get all EBS Snapshots
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Define the age limit for snapshots (e.g., 1 days) with UTC timezone
   # age_limit = datetime.now(timezone.utc) - timedelta(days=1)

    deleted_snapshots = []

    # Loop through all snapshots
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')
        start_time = snapshot['StartTime']  # When the snapshot was created (timezone-aware)

        # Only process snapshots older than the defined age limit
       # if start_time < age_limit:
        if not volume_id:
                # If no volume ID is found, delete the snapshot
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                deleted_snapshots.append(snapshot_id)
                print(f"Deleted EBS snapshot {snapshot_id} as it was not attached to any volume and is older than 30 days.")
        else:
                try:
                    # Try to describe the volume
                    volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
                    # If the volume is not attached to any instance, delete the snapshot
                    if not volume_response['Volumes'][0]['Attachments']:
                        ec2.delete_snapshot(SnapshotId=snapshot_id)
                        deleted_snapshots.append(snapshot_id)
                        print(f"Deleted EBS snapshot {snapshot_id} as it was taken from a volume not attached to any instance and is older than 30 days.")
                except ec2.exceptions.ClientError as e:
                    # If volume does not exist (InvalidVolume.NotFound), delete the snapshot
                    if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                        ec2.delete_snapshot(SnapshotId=snapshot_id)
                        deleted_snapshots.append(snapshot_id)
                        print(f"Deleted EBS snapshot {snapshot_id} as its associated volume was deleted and it is older than 30 days.")
    
    # Return the response
    return {
        "statusCode": 200,
        "body": f"Deleted Snapshots: {deleted_snapshots}" if deleted_snapshots else "No snapshots deleted."
    }
