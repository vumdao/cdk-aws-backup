#!/usr/bin/env python3

import sys
from aws_cdk import core
from aws_backup.aws_backup_stack import AwsBackupStack


app = core.App()
core_env = core.Environment(region='us-east-1')
AwsBackupStack(app, f"us-storage-aws-backup", env=core_env)
app.synth()
