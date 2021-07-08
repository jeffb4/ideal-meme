#!/bin/sh

cd /app/pipeline || exit 1

cdk deploy
