from aws_cdk import (
    Stack,
    pipelines,
    Stage,
)

from constructs import Construct

import tsv_ecs.rds_stack
from tsv_ecs.rds_stack import RdsStack


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

        shell_step3 = pipelines.ShellStep("printing", commands=["ls -la"])

        class MyApplication(Stage):
            def __init__(self, scope, id, *, env=None, outdir=None):
                super().__init__(scope, id, env=env, outdir=outdir)

                db_stack = RdsStack(self, "RdsStack")

        ordered_steps = pipelines.Step.sequence([shell_step3])
        app_stage = pipeline.add_stage(MyApplication(self, "RdsStack"),
                                       pre=ordered_steps,
                                       )
