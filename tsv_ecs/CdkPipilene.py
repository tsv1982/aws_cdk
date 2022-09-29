from aws_cdk import (
    Stack,
    pipelines,
    Stage,
)

from constructs import Construct

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

                                          )

        ordered_steps = pipelines.Step.sequence([
            pipelines.ManualApprovalStep("build"),

        ])

