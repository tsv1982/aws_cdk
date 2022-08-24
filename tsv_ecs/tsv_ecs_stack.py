from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ecs_patterns as ecs_patterns,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as actions,
    pipelines,

)
from aws_cdk.pipelines import ShellStep

from constructs import Construct

class TsvEcsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ecr_repository = ecr.Repository(self, "tsv-petclinic-repository", repository_name="ecs-petclinic-repository")



        # vpc = ec2.Vpc(self, "tsv-vpc", cidr="10.0.0.0/22", max_azs=3)
        #
        # cluster = ecs.Cluster(self, "tsv_cluster", cluster_name="tsv_cluster", vpc=vpc)
        #
        # execution_role = iam.Role(self, "tsv_execution_role",
        #                             assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        #                             role_name="tsv_execution_role")
        # execution_role.add_to_policy(iam.PolicyStatement(effect=iam.Effect.ALLOW, resources=["*"],
        #                                                    actions=["ecr:GetAuthorizationToken",
        #                                                             "ecr:BatchCheckLayerAvailability",
        #                                                             "ecr:GetDownloadUrlForLayer", "ecr:BatchGetImage",
        #                                                             "logs:CreateLogStream", "logs:PutLogEvents"]))
        #
        # task_definition = ecs.FargateTaskDefinition(self, "tsv_task_definition", cpu=512, memory_limit_mib=2048,
        #                                             execution_role=execution_role, family="tsv_task_definition")
        #
        # image = ecs.ContainerImage.from_registry("tsv1982/petclinic_01")
        # container = task_definition.add_container("petclinic", image=image)
        #
        # container.add_port_mappings(ecs.PortMapping(container_port=8080, host_port=8080))
        #
        # ecs_patterns.ApplicationLoadBalancedFargateService(self, "tsv-LB",
        #                                                cluster=cluster,
        #                                                task_definition=task_definition,
        #                                                desired_count=2,
        #                                                cpu=512,
        #                                                memory_limit_mib=2048,
        #                                                public_load_balancer=True)

        git_source = pipelines.CodePipelineSource.connection("tsv1982/petclinic-docker-jenkins", "ci-cd-cdk",
                     connection_arn="arn:aws:codestar-connections:eu-central-1:779113714568:connection/93b86f37-0210-4c36-b297-5ed5a32b7e72")

        synth = pipelines.ShellStep("Synth",
                                    input=git_source,
                                  # commands=["mvn -B -Dspring-boot.run.profiles=mysql -DskipTests clean package", ]))
                                    commands=["ls -la", ])

        sourceOutput = codepipeline.Artifact()
        source_output = codepipeline.Artifact()

        invalidate_build_project = codebuild.PipelineProject(self, "InvalidateProject",
                                                             build_spec=codebuild.BuildSpec.from_object({
                                                                 "version": "0.2",
                                                                 "phases": {
                                                                     "build": {
                                                                         "commands": [
                                                                             "mvn -B -Dspring-boot.run.profiles=mysql -DskipTests clean package"
                                                                             ]
                                                                     }
                                                                 }
                                                             }))


        stages = [codepipeline.StageProps(
                  stage_name="Deploy",
                  actions=[actions.CodeStarConnectionsSourceAction(
                        action_name="tsvGit",
                        owner="tsv1982",
                        repo="petclinic-docker-jenkins",
                        branch="ci-cd-cdk",
                        connection_arn="arn:aws:codestar-connections:us-east-1:123456789012:connection/12345678-abcd-12ab-34cdef5678gh",
                        output=sourceOutput,
                        run_order=1),

                    actions.CodeBuildAction(
                    action_name="Build",
                    project=invalidate_build_project,
                    input=sourceOutput,
                    run_order=2)]
                  ),


        ]

        pipeline = codepipeline.Pipeline(self, "Pipeline", stages=stages)



        # source_stage = pipeline.add_stage(stage_name="Source")
        #
        # source_stage.add_action(source_action)








       # pipeline = pipelines.CodePipeline(self, "Pipeline", synth=[synth, dep])









