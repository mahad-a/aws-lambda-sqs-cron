from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as event_targets,
)
from constructs import Construct

class CronLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        cron_lambda = _lambda.Function( # create a lambda function
            self,
            "CronLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda"),
            handler="lambda_function.lambda_handler", # the location of the lambda function
            description="Sends a message to simulated_application_queue every 5 minutes by using CRON scheduling",
            environment={ # the queue to send messages to
                "QUEUE_NAME": "simulated_application_queue"
            }
        )
        
        lambda_statement = iam.PolicyStatement(
            actions= ['lambda:*', 'sqs:*', 'logs:*'],
            effect= iam.Effect.ALLOW,
            resources=['*']
        )
        
        # create a policy using the policy statement for all lambda functions
        policy = iam.Policy(self, "CronLambdaPolicy", statements=[lambda_statement])
        policy.attach_to_role(cron_lambda.role)
                
        lambda_schedule = events.Schedule.rate(Duration.minutes(5)) # schedule to trigger the lambda function every 5 minutes
        event_lambda_target = event_targets.LambdaFunction(handler=cron_lambda) # setting the target to be the lambda function

        # * define the CloudWatch Event Rule
        events.Rule( 
            self,
            "Lambda5MinsRule",
            description="Run Lambda Every 5 Minutes",
            enabled=True,
            schedule=lambda_schedule,
            targets=[event_lambda_target],
        )
