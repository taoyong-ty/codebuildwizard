# Define the buildspec for the build-and-push-to-ecr template
BUILD_AND_PUSH_TO_ECR_BUILDSPEC = """
version: 0.2

phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $ECR_REPOSITORY_URI
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...
      - docker build -t $ECR_REPOSITORY_URI:$IMAGE_TAG .
      - docker tag $ECR_REPOSITORY_URI:$IMAGE_TAG $ECR_REPOSITORY_URI:$IMAGE_TAG
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker image...
      - docker push $ECR_REPOSITORY_URI:$IMAGE_TAG
artifacts:
  files:
    - '**/*'
"""

# Define the questions for the build-and-push-to-ecr template
BUILD_AND_PUSH_TO_ECR_QUESTIONS = [
    {
        "type": "input",
        "name": "project_name",
        "message": "Enter the name of the CodeBuild project:",
    },
    {
        "type": "input",
        "name": "source_repo",
        "message": "Enter the URL of the source code repository:",
    },
    {
        "type": "input",
        "name": "ecr_repo",
        "message": "Enter the name of the ECR repository to push the image to:",
    },
]

