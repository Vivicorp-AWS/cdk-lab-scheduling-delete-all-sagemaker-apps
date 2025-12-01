
# Scheduling Deleting All SageMaker Apps

This project uses AWS CDK to automatically shutdown all running SageMaker Apps on a scheduled basis. It helps reduce costs by ensuring that SageMaker Studio apps (KernelGateway, JupyterServer, etc.) are not left running when not in use.

## Architecture

The solution provisions the following AWS resources:

- **Lambda Function**: Scans all SageMaker domains and user profiles, then deletes all apps with "InService" status
- **EventBridge Rule**: Triggers the Lambda function on a cron schedule (default: daily at 12:00 UTC)
- **IAM Role & Policy**: Grants the Lambda function necessary permissions to list and delete SageMaker apps

## Features

- Automatically discovers all SageMaker domains in the account
- Iterates through all user profiles in each domain
- Deletes only apps with "InService" status
- Comprehensive logging for monitoring and troubleshooting
- Error handling to continue processing even if individual app deletion fails

## Configuration

You can customize the shutdown schedule by modifying the `SHUTDOWN_PATTERN_UTC` variable in `app.py`. The default schedule is:

```python
SHUTDOWN_PATTERN_UTC = "cron(0 12 ? * * *)"  # Daily at 12:00 UTC
```

## Usage

 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk destroy`     remove the stack from your AWS account

## Prerequisites

- AWS CDK installed and configured
- Python 3.13 or compatible version
- AWS credentials configured with appropriate permissions

## Outputs

After deployment, the stack outputs:
- Lambda function name and ARN
- EventBridge rule name and ARN

## Cost Considerations

This solution helps reduce costs by automatically shutting down SageMaker apps that may be left running. The cost of running this solution (Lambda + EventBridge) is minimal compared to the potential savings from unused SageMaker apps.

