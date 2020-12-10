#!/bin/bash
regions="us-east-1 us-east-2"

for reg in $regions; do
    echo $reg
    instance_id=$(aws ec2 describe-instances --region ${reg} --filters "Name=tag:Name,Values=*-ddb-instance" | jq -r '.[] [0] | [.Instances][0][0] | [.InstanceId][0]')
    volume_id=$(aws ec2 describe-volumes --region ${reg} --filter "Name=attachment.instance-id, Values=${instance_id}" --query "Volumes[].VolumeId" --out text)
    aws ec2 create-tags --region ${reg} --resources ${volume_id} --tags Key=$reg:aws-volume:kind,Value=ebs-storage
done
