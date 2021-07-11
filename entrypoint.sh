#!/bin/bash

if [ "${GH_TOKEN}" = "" ]; then
  echo "GH_TOKEN environment variable must be set to a GitHub Personal Access Token"
fi

export AWS_REGION=us-east-1
export AWS_DEFAULT_REGION=$AWS_REGION

cd /app/pipeline || exit 1

cdk deploy \
  --require-approval never \
  --parameters "PipelineStack:githubToken=${GH_TOKEN}" \
  PipelineStack

API_ENDPOINT=$(aws --region $AWS_REGION cloudformation describe-stacks --stack-name LambdaDeploymentStack | jq -r ".Stacks[0].Outputs[0].OutputValue")

while [ "$API_ENDPOINT" = "" ]; do
  sleep 1
  API_ENDPOINT=$(aws --region $AWS_REGION cloudformation describe-stacks --stack-name LambdaDeploymentStack | jq -r ".Stacks[0].Outputs[0].OutputValue")
done

echo "API should be available at $API_ENDPOINT"
