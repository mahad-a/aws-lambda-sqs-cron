#!/usr/bin/env python3
import aws_cdk as cdk

from cron_lambda.cron_lambda_stack import CronLambdaStack

app = cdk.App()
CronLambdaStack(app, "CronLambdaStack")

app.synth()
