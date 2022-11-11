from aws_cdk import (
    Stack,
    pipelines,
    Stage,
)

from constructs import Construct

from infra.lib.networking_stack import NetworkingStack
from infra.lib.rds_stack import RdsStack
from infra.lib.tsv_ecs_stack import TsvEcsStack
from infra.lib.pipeline_stack import PipelineStack

DB_CREDS_ARN = "arn:aws:secretsmanager:eu-central-1:090146717911:secret:creds-gTGGRt"


class CdkPipeline(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_output = pipelines.CodePipelineSource.connection("tsv1982/aws_cdk", "infrastructure",
                                                                connection_arn="arn:aws:codestar-connections:eu-central-1:090146717911:connection/133453b9-a51d-4e8f-95dc-c3b4d39065d3"
                                                                )

        pipeline = pipelines.CodePipeline(self, "Pipeline",
                                          synth=pipelines.ShellStep("Synth",
                                                                    input=source_output,
                                                                    commands=["pip install -r ./infra/requirements.txt",
                                                                              "npm install -g aws-cdk", "cdk synth"]
                                                                    ),
                                          self_mutation=True,
                                          )

        pipeline.add_stage(InfrastructureStage(self, "infra"))


class InfrastructureStage(Stage):
    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)

        networking_stack = NetworkingStack(self, "Networking")
        rds_stack = RdsStack(self, "RdsStack", vpc=networking_stack.vpc, creds_arn=DB_CREDS_ARN)
        ecs_stack = TsvEcsStack(self, "TsvEcsStack", vpc=networking_stack.vpc, db_secret=rds_stack.db_credentials)
        ecs_stack.add_dependency(rds_stack)
#      PipelineStack(self, "PipelineStack", service=ecs_stack.service)
