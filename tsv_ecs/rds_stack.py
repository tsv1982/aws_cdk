from aws_cdk import (
    Stack,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as actions,
    aws_iam as iam, Duration

)

from constructs import Construct
from werkzeug.debug import console


class RdsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # vpc = ec2.Vpc(self, "tsv-bd", cidr="10.0.0.0/22", max_azs=3)
        # credentials = rds.Credentials.from_generated_secret("clusteradmin")
        #
        # cluster = rds.DatabaseCluster(self, "Database", engine=rds.DatabaseClusterEngine.aurora_mysql(
        #                               version=rds.AuroraMysqlEngineVersion.of(aurora_mysql_full_version="5.7.mysql_aurora.2.08.1")),
        #                               credentials=credentials,
        #                               # Optional - will default to 'admin' username and generated password
        #                               instance_props=rds.InstanceProps(
        #                               # optional , defaults to t3.medium
        #                               # instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
        #                               vpc=vpc,
        #                               #vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
        #                               publicly_accessible=True
        #                               )
        #                               )



