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

        class MyApplication(Stage):
            def __init__(self, scope, id, *, env=None, outdir=None):
                super().__init__(scope, id, env=env, outdir=outdir)
                db_creds_arn = "arn:aws:secretsmanager:eu-central-1:571847562388:secret:secretDB-k7uD0M"

                networking_stack = NetworkingStack(self, "Networking")
                rds_stack = RdsStack(self, "RdsStack", vpc=networking_stack.vpc, creds_arn=db_creds_arn)
                ecs_stack = TsvEcsStack(self, "TsvEcsStack", vpc=networking_stack.vpc, db_secret=rds_stack.db_credentials)
                pipeline_stack = PipelineStack(self, "PipelineStack", service=ecs_stack.service)

        network_stage = pipeline.add_stage(MyApplication(self, "MyPipeline"))
        # rds_stage = pipeline.add_stage(MyApplication(self, "RdsStack"))
        # esc_stage = pipeline.add_stage(MyApplication(self, "TsvEcsStack"))
        # pipeline_stage = pipeline.add_stage(MyApplication(self, "PipelineStack"))

