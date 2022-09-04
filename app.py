#!/usr/bin/env python3

import aws_cdk as cdk

from tsv_ecs.tsv_ecs_stack import TsvEcsStack
from tsv_ecs.pipeline_stack import PipelineStack

app = cdk.App()
ecs_stack = TsvEcsStack(app, "TsvEcsStack", )
pipeline_stack = PipelineStack(app, "PipelineStack", service=ecs_stack.service)

app.synth()
