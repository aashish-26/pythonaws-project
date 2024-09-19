import boto3
ec2 = boto3.client('ec2')

# Get all EBS Snapshots
response = ec2.describe_snapshots(OwnerIds=['self'])

# Get all running EC2 instances
instances = ec2.describe_instances(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
active_instance_ids = set()

# Collect active instance IDs
for reservation in instances['Reservations']:
    for instance in reservation['Instances']:
        active_instance_ids.add(instance['InstanceId'])

# Loop through all snapshots
for snapshot in response['Snapshots']:
    snapshot_id = snapshot['SnapshotId']
    volume_id = snapshot.get('VolumeId')

    # If the snapshot is not attached to any volume, delete it
    if not volume_id:
        ec2.delete_snapshot(SnapshotId=snapshot_id)
        print(f"Deleted EBS snapshot {snapshot_id} as it was not attached to any volume.")
    else:
        try:
            # Get details of the volume
            volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
            # If the volume is not attached to any instance, delete the snapshot
            if not volume_response['Volumes'][0]['Attachments']:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"Deleted EBS snapshot {snapshot_id} as it was taken from volume not attached to any instance.")
        except ec2.exceptions.ClientError as e:
            # Handle the case where the volume doesn't exist
            if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"Deleted EBS Snapshot {snapshot_id} as its associated volume was not found.")
