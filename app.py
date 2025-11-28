#!/usr/bin/env python3
import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    aws_lambda as lambda_,
    Duration,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as events_targets,
    CfnOutput,
)

REGION = "us-east-1"
SHUTDOWN_PATTERN_DAILY_8PM_UTC = "cron(0 12 ? * * *)"  # [NOTE] Better set multiple timestamp to prevent unexpected exceptions

class ScheduledSageMakerAppsShutdown(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
    
        function = lambda_.Function(
            self, "lambda_function",
            runtime=lambda_.Runtime.PYTHON_3_13,
            code=lambda_.Code.from_asset("lambda_code"),
            handler="index.handler",
            timeout=Duration.seconds(300),
            )
        function.role.attach_inline_policy(
            iam.Policy(self, "policy", statements=[
                iam.PolicyStatement(
                    actions=[
                        "sagemaker:ListApps",
                        "sagemaker:DeleteApp",
                        "sagemaker:DescribeDomain",
                        "sagemaker:DescribeApp",
                        "sagemaker:ListDomains",
                        "sagemaker:ListUserProfiles",
                        "sagemaker:DescribeUserProfile"
                        ],
                    resources=["*"],
                ),
            ])
        )

        schedule_rule = events.Rule(
            self, "CanvasShutdownSchedule",
            schedule=events.Schedule.expression(SHUTDOWN_PATTERN_DAILY_8PM_UTC),
            targets=[events_targets.LambdaFunction(function)],
        )

        CfnOutput(self, "LambdaFunctionName", value=function.function_name)
        CfnOutput(self, "LambdaFunctionARN", value=function.function_arn)
        CfnOutput(self, "EventBridgeRuleName", value=schedule_rule.rule_name)
        CfnOutput(self, "EventBridgeRuleARN", value=schedule_rule.rule_arn)

app = cdk.App()
ScheduledSageMakerAppsShutdown(app, "ScheduledSageMakerAppsShutdown",)
app.synth()
