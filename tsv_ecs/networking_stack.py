from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)

from constructs import Construct


class NetworkingStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, ".venv-vpc", cidr="10.0.0.0/22", max_azs=3)



