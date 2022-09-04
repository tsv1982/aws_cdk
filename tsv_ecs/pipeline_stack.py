from aws_cdk import (
    Stack,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as actions,
    pipelines,
    aws_iam as iam, Duration

)

from constructs import Construct


class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, service, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        sourceOutput = codepipeline.Artifact()

        invalidate_build_project = codebuild.PipelineProject(self, "InvalidateProject",
                                                             environment=codebuild.BuildEnvironment(privileged=True),
                                                             build_spec=codebuild.BuildSpec.from_object({

                                                                 "version": "0.2",
                                                                 "phases": {
                                                                     "pre_build": {
                                                                         "commands": [
                                                                             'REPOSITORY_URI=447506749563.dkr.ecr.eu-central-1.amazonaws.com/ecs-tsv-my-html',
                                                                             'COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)',
                                                                             'IMAGE_TAG=${COMMIT_HASH:=latest}',
                                                                             "aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 447506749563.dkr.ecr.eu-central-1.amazonaws.com"
                                                                         ]
                                                                     },
                                                                     "build": {"commands": [
                                                                         "docker build -t $REPOSITORY_URI:latest .",
                                                                         "docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG",
                                                                         "docker push $REPOSITORY_URI:$IMAGE_TAG",
                                                                         "docker push $REPOSITORY_URI:latest",
                                                                         'printf \'[{"name":"myHtml","imageUri":"%s"}]\' "$REPOSITORY_URI:$IMAGE_TAG" > imagedefinitions.json'
                                                                     ]}},
                                                                 'artifacts': {
                                                                     'files': [
                                                                         'imagedefinitions.json'
                                                                     ]
                                                                 }
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

        build_output = codepipeline.Artifact()
        build_action = actions.CodeBuildAction(
            action_name="Build",
            project=invalidate_build_project,
            input=sourceOutput,
            outputs=[build_output],
            run_order=2)

        source_stage = pipeline.add_stage(
            stage_name="source",
            actions=[source_action]
        )

        build_stage = pipeline.add_stage(
            stage_name="build",
            actions=[build_action]
        )

        deploy_action = actions.EcsDeployAction(
            action_name="DeployAction",
            service=service,
            input=build_output,
            deployment_timeout=Duration.minutes(60)
        )

        deploy_stage = pipeline.add_stage(
            stage_name="deploy",
            actions=[deploy_action]
        )
