#!/usr/bin/env python3

import aws_cdk as cdk

from tsv_ecs.tsv_ecs_stack import TsvEcsStack

app = cdk.App()
TsvEcsStack(app, "TsvEcsStack", )

app.synth()
