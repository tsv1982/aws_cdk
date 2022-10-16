#!/usr/bin/env python3

import aws_cdk as cdk
import tsv_ecs.rds_stack
from tsv_ecs.tsv_ecs_stack import TsvEcsStack
from tsv_ecs.pipeline_stack import PipelineStack
from tsv_ecs.rds_stack import RdsStack
from tsv_ecs.networking_stack import NetworkingStack
from tsv_ecs.CdkPipilene import CdkPipeline

app = cdk.App()
#networking_stack = NetworkingStack(app, "Networking")
#rds_stack = RdsStack(app, "RdsStack", vpc=networking_stack.vpc, creds_arn=db_creds_arn)
#ecs_stack = TsvEcsStack(app, "TsvEcsStack", vpc=networking_stack.vpc, db_secret=rds_stack.db_credentials)
#pipeline_stack = PipelineStack(app, "PipelineStack", service=ecs_stack.service)
cdk_pipeline = CdkPipeline(app, "CdkPipeline")


app.synth()
