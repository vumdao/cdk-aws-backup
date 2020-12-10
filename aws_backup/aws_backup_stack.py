from aws_cdk import (
    core,
    aws_backup as bk,
    aws_events as event
)


class AwsBackupStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, env, **kwargs) -> None:
        super().__init__(scope, id, env=env, **kwargs)

        core_tag = core.Tags.of(self)

        # The code that defines your stack goes here
        backup_plan = bk.BackupPlan(
            scope=self,
            id="UsStorageBackupPlanEBS",
            backup_plan_name=f"us-storage-ebs-volume"
        )

        backup_vault_name = f'us-storage-backup-vault'
        bk_vault = bk.BackupVault(
            scope=self,
            id=f'UsStorageBackupVault',
            backup_vault_name=backup_vault_name,
        )

        backup_plan.add_rule(
            rule=bk.BackupPlanRule(
                backup_vault=bk_vault,
                rule_name='backup-ebs-volume-daily',
                delete_after=core.Duration.days(1),
                schedule_expression=event.Schedule.cron(
                    minute="0",
                    hour="0",
                    month="*",
                    week_day="*",
                    year="*"
                )
            )
        )

        backup_plan.add_selection(
            id=f'us-storage-selection',
            backup_selection_name=f"us-storage-ebs-volume",
            resources=[
                bk.BackupResource.from_tag(
                    key='us:aws-volume:kind',
                    value='ebs-storage'
                )
            ]
        )

        core_tag.add(
            key='cfn.aws-backup.stack',
            value='ebs-storage'
        )
