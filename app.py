#!/usr/bin/env python3

import aws_cdk as cdk

from infra.lib.CdkPipeline import CdkPipeline

app = cdk.App()
cdk_pipeline = CdkPipeline(app, "CdkPipeline")

app.synth()
