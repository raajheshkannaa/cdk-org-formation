#!/usr/bin/env python3

import aws_cdk as cdk

from cdkorgformation.pipeline_stack import CDKOrgFormationPipelineStack


app = cdk.App()
CDKOrgFormationPipelineStack(app, "pipeline-org-formation")

app.synth()
