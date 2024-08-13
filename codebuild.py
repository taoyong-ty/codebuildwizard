import click
import boto3
import time
from PyInquirer import prompt
from templates.build_to_ecr import BUILD_AND_PUSH_TO_ECR_QUESTIONS, BUILD_AND_PUSH_TO_ECR_BUILDSPEC
from templates.deploy_to_ecs import DEPLOY_TO_ECS_QUESTIONS, DEPLOY_TO_ECS_BUILDSPEC

AVAILABLE_TEMPLATES = {
    "build-and-push-to-ecr": {
        "description": "Build and push a Docker image to Amazon ECR",
        "questions": BUILD_AND_PUSH_TO_ECR_QUESTIONS,
        "buildspec": BUILD_AND_PUSH_TO_ECR_BUILDSPEC,
    },
    "deploy-to-ecs": {
        "description": "Deploy a ECR image to an Amazon ECS service",
        "questions": DEPLOY_TO_ECS_QUESTIONS,
        "buildspec": DEPLOY_TO_ECS_BUILDSPEC,
    },
}
@click.command()
def create_project():
    """Create a new AWS CodeBuild project using a template."""
    template_choices = [
        {
            "name": f"**{name}** ({data['description']})",
            "value": data,
        }
        for name, data in AVAILABLE_TEMPLATES.items()
    ]
    template = prompt([
        {
            "type": "list",
            "name": "template",
            "message": "Select a template:",
            "choices": template_choices,
        }
    ])["template"]

    answers = prompt(template["questions"])
    print_friendly_string(template, answers)

def print_friendly_string(template, answers):
    """Print a friendly version of the create_project API input based on the selected template and user inputs."""
    time.sleep(1)
    print("")
    print("")
    print("Creating CodeBuild project with the following input:")
    print(f"Project Name: {answers['project_name']}")
    time.sleep(0.5)

    if "source_repo" in answers:
        print(f"Source Repository: {answers['source_repo']}")

    environment = {
        "type": "LINUX_CONTAINER",
        "image": "aws/codebuild/standard:5.0",
        "computeType": "BUILD_GENERAL1_SMALL",
        "environmentVariables": [],
    }

    if "ecr_repo" in answers:
        environment["environmentVariables"].append({
            "name": "ECR_REPOSITORY_URI",
            "value": answers["ecr_repo"],
        })

    if "ecs_service" in answers:
        environment["environmentVariables"].append({
            "name": "ECS_SERVICE",
            "value": answers["ecs_service"],
        })

    if "ecs_cluster" in answers:
        environment["environmentVariables"].append({
            "name": "ECS_CLUSTER",
            "value": answers["ecs_cluster"],
        })

    if "ecs_task_definition" in answers:
        environment["environmentVariables"].append({
            "name": "ECS_TASK_DEFINITION",
            "value": answers["ecs_task_definition"],
        })

    if "container_name" in answers:
        environment["environmentVariables"].append({
            "name": "CONTAINER_NAME",
            "value": answers["container_name"],
        })

    time.sleep(0.3)

    print("Environment:")
    print(f"\tType: {environment['type']}")
    print(f"\tImage: {environment['image']}")
    print(f"\tComputeType: {environment['computeType']}")
    print("\tEnvironmentVariables:")
    for env_var in environment["environmentVariables"]:
        time.sleep(0.2)
        print(f"\t\t{env_var['name']}: {env_var['value']}")

    print("")
    print("ServiceRole: arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/service-role/codebuild-service-role")
    print("Buildspec:")
    time.sleep(0.5)
    print(template["buildspec"])

if __name__ == "__main__":
    create_project()