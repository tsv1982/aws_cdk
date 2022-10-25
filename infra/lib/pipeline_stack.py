from aws_cdk import (
    Stack,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as actions,
    aws_iam as iam, Duration
)

from constructs import Construct

CONNECTION_ARN = "arn:aws:codestar-connections:ap-northeast-1:571847562388:connection/200c13ec-a117-4efb-b81c-0b93cba32197"


class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, service, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_output = codepipeline.Artifact()

        build_project = codebuild.PipelineProject(self, "Build",
                                                  environment=codebuild.BuildEnvironment(privileged=True),
                                                  build_spec=codebuild.BuildSpec.from_object({
                                                      "version": "0.2",
                                                      "phases": {
                                                          "pre_build": {
                                                              "commands": [
                                                                  'REPOSITORY_URI=571847562388.dkr.ecr.eu-central-1.amazonaws.com/.venv-hello',
                                                                  'COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)',
                                                                  'IMAGE_TAG=${COMMIT_HASH:=latest}',
                                                                  "aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 571847562388.dkr.ecr.eu-central-1.amazonaws.com"
                                                              ]
                                                          },
                                                          "build": {"commands": [
                                                              "docker build -t $REPOSITORY_URI:latest .",
                                                              "docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG",
                                                              "docker push $REPOSITORY_URI:$IMAGE_TAG",
                                                              "docker push $REPOSITORY_URI:latest",
                                                              'printf \'[{"name":".venv-hello","imageUri":"%s"}]\' "$REPOSITORY_URI:$IMAGE_TAG" > imagedefinitions.json'
                                                          ]}},
                                                      'artifacts': {
                                                          'files': [
                                                              'imagedefinitions.json'
                                                          ]
                                                      }
                                                  }))

        build_project.role.add_to_policy(iam.PolicyStatement(actions=[
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

        pipeline = codepipeline.Pipeline(self, "Pipeline_hellow")

        source_action = actions.CodeStarConnectionsSourceAction(
            action_name="Source",
            owner="tsv1982",
            repo="cdkPyHelloWorld",
            branch="main",
            connection_arn=CONNECTION_ARN,
            output=source_output,
            run_order=1)

        build_output = codepipeline.Artifact()

        build_action = actions.CodeBuildAction(
            action_name="Build",
            project=build_project,
            input=source_output,
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
            deployment_timeout=Duration.minutes(60),
            run_order=3
        )

        deploy_stage = pipeline.add_stage(
            stage_name="deploy",
            actions=[deploy_action],
        )
