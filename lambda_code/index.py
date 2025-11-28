import logging
from botocore.config import Config
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    sagemaker = boto3.client('sagemaker',)

    # config = Config(
    #     region_name = 'us-east-1',
    # )
    # sagemaker = boto3.client('sagemaker', config=config)

    domains = sagemaker.list_domains()['Domains']

    if domains:
        for domain in domains:
            domain_id = domain['DomainId']
            logger.info(f"Searching User Profiles in Domain: {domain_id}.")

            users = sagemaker.list_user_profiles(DomainIdEquals=domain_id)['UserProfiles']
            if users:
                for user in users:
                    user_profile_name = user['UserProfileName']
                    logger.info(f"Searching in-service Apps created by User Profile: {user_profile_name}.")

                    apps = sagemaker.list_apps(DomainIdEquals=domain_id, UserProfileNameEquals=user_profile_name)['Apps']
                    if apps:
                        for app in apps:
                            app_type, app_name, app_status = app['AppType'], app['AppName'], app['Status']
                            if app_status == 'InService':
                                logger.info(f"Deleting in-service App (App Name = {app_name}, App Type = ({app_type})")
                                try:
                                    sagemaker.delete_app(
                                        DomainId=domain_id,
                                        UserProfileName=user_profile_name,
                                        AppType=app_type,
                                        AppName=app_name,
                                    )
                                except Exception as e:
                                    logger.error(f"Failed to delete App (Domain ID = {domain_id}, User Profile Name = {user_profile_name}, App Name = {app_name}, App Type = ({app_type})")
                                    logger.error(e)

                            else: logger.info(f"Skipping non-in-service App (App Name = {app_name}, App Type = ({app_type}), Status = {app_status})")
                    else:
                        logger.info(f"No in-service App found in User Profile: {user_profile_name}.")
            else:
                logger.info(f"No User Profile found in Domain: {domain_id}.")
    else:
        logger.info("No domain found.")

    return {
            'statusCode': 200,
        }