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

        git_source = pipelines.CodePipelineSource.connection("tsv1982/petclinic-docker-jenkins", "ci-cd-cdk",
                                                             connection_arn="arn:aws:codestar-connections:eu-central-1:779113714568:connection/93b86f37-0210-4c36-b297-5ed5a32b7e72")

        sourceOutput = codepipeline.Artifact()

        invalidate_build_project = codebuild.PipelineProject(self, "InvalidateProject",
                                                             environment=codebuild.BuildEnvironment(privileged=True),
                                                             build_spec=codebuild.BuildSpec.from_object({

                                                                 "version": "0.2",
                                                                 "phases": {
                                                                     "install": {
                                                                         "runtime-version": {
                                                                             "java": "latest"
                                                                         }
                                                                     },
                                                                     "build": {"commands": [
                                                                         "mvn -B -Dspring-boot.run.profiles=mysql -DskipTests clean package",
                                                                         "aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 779113714568.dkr.ecr.eu-central-1.amazonaws.com",
                                                                         "docker build -t ecs-petclinic-repository .",
                                                                         "docker tag ecs-petclinic-repository:latest 779113714568.dkr.ecr.eu-central-1.amazonaws.com/ecs-petclinic-repository:latest",
                                                                         "docker push 779113714568.dkr.ecr.eu-central-1.amazonaws.com/ecs-petclinic-repository:latest"]}}
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
            repo="petclinic-docker-jenkins",
            branch="ci-cd-cdk",
            connection_arn="arn:aws:codestar-connections:eu-central-1:779113714568:connection/93b86f37-0210-4c36-b297-5ed5a32b7e72",
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

        # source_stage = [codepipeline.StageProps(
        #           stage_name="stage1",
        #           actions=[actions.CodeStarConnectionsSourceAction(
        #                 action_name="Source",
        #                 owner="tsv1982",
        #                 repo="petclinic-docker-jenkins",
        #                 branch="ci-cd-cdk",
        #                 connection_arn="arn:aws:codestar-connections:us-east-1:123456789012:connection/12345678-abcd-12ab-34cdef5678gh",
        #                 output=sourceOutput,
        #                 run_order=1),
        #
        #             actions.CodeBuildAction(
        #             action_name="Build",
        #             project=invalidate_build_project,
        #             input=sourceOutput,
        #             run_order=2)],
        #           ),
        #
        # ]

    # pipeline = codepipeline.Pipeline(self, "Pipeline", stages=[source_stage])
