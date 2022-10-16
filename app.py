#!/usr/bin/env python3

import aws_cdk as cdk
import tsv_ecs.rds_stack
from tsv_ecs.tsv_ecs_stack import TsvEcsStack
from tsv_ecs.pipeline_stack import PipelineStack
from tsv_ecs.rds_stack import RdsStack
from tsv_ecs.networking_stack import NetworkingStack
from tsv_ecs.CdkPipilene import CdkPipeline

app = cdk.App()
cdk_pipeline = CdkPipeline(app, "CdkPipeline")


app.synth()
