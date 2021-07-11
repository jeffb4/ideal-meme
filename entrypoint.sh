#!/bin/sh

if [ "${GH_TOKEN}" = "" ]; then
  echo "GH_TOKEN environment variable must be set to a GitHub Personal Access Token"
fi

cd /app/pipeline || exit 1

cdk deploy \
  --require-approval never \
  --parameters "PipelineStack:githubToken=${GH_TOKEN}" \
  PipelineStack
