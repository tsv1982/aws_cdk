from aws_cdk import (
    Stack,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as actions,
    pipelines,
    aws_iam as iam

)

from constructs import Construct


class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        git_source = pipelines.CodePipelineSource.connection("tsv1982/myHtml", "myHtml",
                                                             connection_arn="arn:aws:codestar-connections:eu-central-1:447506749563:connection/e506d89c-9323-43d0-ad9d-de617349945d")

        sourceOutput = codepipeline.Artifact()

        invalidate_build_project = codebuild.PipelineProject(self, "InvalidateProject",
                                                             environment=codebuild.BuildEnvironment(privileged=True),
                                                             build_spec=codebuild.BuildSpec.from_object({

                                                                 "version": "0.2",
                                                                 "phases": {
                                                                     "build": {"commands": [
                                                                         "aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 447506749563.dkr.ecr.eu-central-1.amazonaws.com",
                                                                         "docker build -t ecs-tsv-my-html .",
                                                                         "docker tag ecs-tsv-my-html:latest 447506749563.dkr.ecr.eu-central-1.amazonaws.com/ecs-tsv-my-html:latest",
                                                                         "docker push 447506749563.dkr.ecr.eu-central-1.amazonaws.com/ecs-tsv-my-html:latest"]}}
                                                             }))



        invalidate_build_project.role.add_to_policy(iam.PolicyStatement(actions=[

            "ecr:BatchCheckLayerAvailability",
            "ecr:GetDownloadUrlForLayer",
            "ecr:BatchGetImage",
            "ecr:GetAuthorizationToken",
            "ecr:PutImage",
            "ecr:InitiateLayerUpload",
            "ecr:UploadLayerPart",
            "ecr:CompleteLayerUpload"

        ],

            effect=iam.Effect.ALLOW,

            resources=["*"]))

        pipeline = codepipeline.Pipeline(self, "Pipeline")

        source_action = actions.CodeStarConnectionsSourceAction(
            action_name="Source",
            owner="tsv1982",
            repo="myHtml",
            branch="main",
            connection_arn="arn:aws:codestar-connections:eu-central-1:447506749563:connection/e506d89c-9323-43d0-ad9d-de617349945d",
            output=sourceOutput,
            run_order=1)

        build_action = actions.CodeBuildAction(
            action_name="Build",
            project=invalidate_build_project,
            input=sourceOutput,
            run_order=2)

        souce_stage = pipeline.add_stage(
            stage_name="source",
            actions=[source_action]
        )

        build_stage = pipeline.add_stage(
            stage_name="deploy",
            actions=[build_action]
        )


