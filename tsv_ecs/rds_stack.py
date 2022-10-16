from aws_cdk import (
    Stack,
    Stage,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_secretsmanager as secrets,
    aws_connect as connect
)

from constructs import Construct


class RdsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, creds_arn: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.db_credentials = secrets.Secret.from_secret_complete_arn(self, "creds", secret_complete_arn=creds_arn)
        self.credentials = rds.Credentials.from_secret(self.db_credentials)

        cluster = rds.DatabaseCluster(self, "Database", engine=rds.DatabaseClusterEngine.aurora_postgres(
            version=rds.AuroraPostgresEngineVersion.VER_11_16),
                                      # AuroraMysqlEngineVersion.of(aurora_mysql_full_version="5.7.mysql_aurora.2.08.1")),
                                      credentials=self.credentials,
                                      # Optional - will default to 'admin' username and generated password
                                      instance_props=rds.InstanceProps(
                                          # optional , defaults to t3.medium

                                          instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3,
                                                                            ec2.InstanceSize.MEDIUM),
                                          vpc=vpc,
                                          vpc_subnets=ec2.SubnetSelection(
                                              subnet_type=ec2.SubnetType.PUBLIC),
                                          publicly_accessible=True

                                      )
                                      )
        cluster.connections.allow_from_any_ipv4(ec2.Port.all_traffic(), "Open to the world")
