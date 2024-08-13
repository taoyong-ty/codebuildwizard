# Define the questions for the deploy-to-ecs template
DEPLOY_TO_ECS_QUESTIONS = [
    {
        "type": "input",
        "name": "project_name",
        "message": "Enter the name of the CodeBuild project:",
    },
    {
        "type": "input",
        "name": "ecr_repo",
        "message": "Enter the name of the ECR repository with the Docker image:",
    },
    {
        "type": "input",
        "name": "ecs_service",
        "message": "Enter the name of the ECS service to deploy to:",
    },
    {
        "type": "input",
        "name": "ecs_cluster",
        "message": "Enter the name of the ECS cluster:",
    },
    {
        "type": "input",
        "name": "ecs_task_definition",
        "message": "Enter the name of the ECS task definition:",
    },
    {
        "type": "input",
        "name": "container_name",
        "message": "Enter the name of the container in the task definition:",
    },
]

DEPLOY_TO_ECS_BUILDSPEC = """
version: 0.2

phases:
  build:
    commands:
      - TASK_DEFINITION=$(aws ecs describe-task-definition --task-definition "$TASK_FAMILY" --region "$AWS_DEFAULT_REGION")
      - NEW_TASK_DEFINITION=$(echo $TASK_DEFINITION | jq --arg IMAGE "$FULL_IMAGE" '.taskDefinition | .containerDefinitions[0].image = $IMAGE | del(.taskDefinitionArn) | del(.revision) | del(.status) | del(.requiresAttributes) | del(.compatibilities) |  del(.registeredAt)  | del(.registeredBy)')
      - NEW_TASK_INFO=$(aws ecs register-task-definition --region "$AWS_DEFAULT_REGION" --cli-input-json "$NEW_TASK_DEFINITION")
      - NEW_REVISION=$(echo $NEW_TASK_INFO | jq '.taskDefinition.revision')
      - aws ecs update-service --cluster ${ECS_CLUSTER} --service ${SERVICE_NAME} --task-definition ${TASK_FAMILY}:${NEW_REVISION}
"""
