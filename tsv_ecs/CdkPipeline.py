from aws_cdk import (
    Stack,
    pipelines,
    Stage,
)

from constructs import Construct

from tsv_ecs.networking_stack import NetworkingStack
from tsv_ecs.rds_stack import RdsStack
from tsv_ecs.tsv_ecs_stack import TsvEcsStack
from tsv_ecs.pipeline_stack import PipelineStack

DB_CREDS_ARN = "arn:aws:secretsmanager:eu-central-1:571847562388:secret:secretDB-k7uD0M"


class CdkPipeline(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_output = pipelines.CodePipelineSource.connection("tsv1982/aws_cdk", "pipeline",
                                                                connection_arn="arn:aws:codestar-connections:ap-northeast-1:571847562388:connection/200c13ec-a117-4efb-b81c-0b93cba32197"
                                                                )

        pipeline = pipelines.CodePipeline(self, "Pipeline",
                                          synth=pipelines.ShellStep("Synth",
                                                                    # Use a connection created using the AWS console to authenticate to GitHub
                                                                    # Other sources are available.
                                                                    input=source_output,
                                                                    commands=["pip install -r requirements.txt",
                                                                              "npm install -g aws-cdk", "cdk synth"]
                                                                    ),
                                          self_mutation=True,
                                          )

        network_stage = pipeline.add_stage(InfrastructureStage(self, "MyPipeline"))


class InfrastructureStage(Stage):
    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)

        networking_stack = NetworkingStack(self, "Networking")
        rds_stack = RdsStack(self, "RdsStack", vpc=networking_stack.vpc, creds_arn=DB_CREDS_ARN)
        ecs_stack = TsvEcsStack(self, "TsvEcsStack", vpc=networking_stack.vpc, db_secret=rds_stack.db_credentials)
        ecs_stack.add_dependency(rds_stack)
        PipelineStack(self, "PipelineStack", service=ecs_stack.service)