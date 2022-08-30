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

     #   ecr_repository = ecr.Repository(self, "tsv-my-html", repository_name="ecs-tsv-my-html")



        vpc = ec2.Vpc(self, "tsv-vpc", cidr="10.0.0.0/22", max_azs=3)

        cluster = ecs.Cluster(self, "tsv_cluster", cluster_name="tsv_cluster", vpc=vpc)

        execution_role = iam.Role(self, "tsv_execution_role",
                                    assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
                                    role_name="tsv_execution_role")
        execution_role.add_to_policy(iam.PolicyStatement(effect=iam.Effect.ALLOW, resources=["*"],
                                                           actions=["ecr:GetAuthorizationToken",
                                                                    "ecr:BatchCheckLayerAvailability",
                                                                    "ecr:GetDownloadUrlForLayer", "ecr:BatchGetImage",
                                                                    "logs:CreateLogStream", "logs:PutLogEvents"]))

        task_definition = ecs.FargateTaskDefinition(self, "tsv_task_definition", cpu=512, memory_limit_mib=2048,
                                                    execution_role=execution_role, family="tsv_task_definition")

        image = ecs.ContainerImage.from_registry("447506749563.dkr.ecr.eu-central-1.amazonaws.com/ecs-tsv-my-html:latest")
        container = task_definition.add_container("myHtml", image=image)

        container.add_port_mappings(ecs.PortMapping(container_port=80, host_port=80))

        ecs_patterns.ApplicationLoadBalancedFargateService(self, "tsv-LB",
                                                       cluster=cluster,
                                                       task_definition=task_definition,
                                                       desired_count=2,
                                                       cpu=512,
                                                       memory_limit_mib=2048,
                                                       public_load_balancer=True)












