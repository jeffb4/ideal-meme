# ideal-meme

Gaggle coding exercise repository

## Usage

### Prerequisites

- Docker (tested on a Mac with Docker Desktop)

- AWS API credentials (either in `~/.aws/` directory or environment variables)

- GitHub Personal Access Token

### Running

    docker run -v ${HOME}/.aws:/root/.aws \
      -e AWS_ACCESS_KEY_ID \
      -e AWS_SECRET_ACCESS_KEY \
      -e AWS_SESSION_TOKEN \
      -e AWS_PROFILE -e AWS_DEFAULT_PROFILE \
      -e GH_TOKEN=github_personal_access_token \
      jeffb4/ideal-meme

## Development

### Structure

- `.devcontainer/` - You can run this in a VSCode dev container

- `lambda/` - NodeJS API

- `pipeline/` - CDK pipeline stack and lambda stack

- `Dockerfile` - the way the `jeffb4/ideal-meme` wrapper container is built

- `Makefile` - build target for docker container

- `entrypoint.sh` - docker container entrypoint to make this mostly point-and-click

### Building

make docker

### Testing

A CodePipeline is automatically created that includes a functional test

## Reflections

So, this is my first AWS CDK project, and my first CodePipeline
deployment in a very long time.

Because CDK requires the `aws-cdk` npm project to do actual deployments,
I don't feel that using the Python variant was a good use of time; NodeJS
would have been an easier and faster path, probably.

Having to redeploy a CodePipeline stack to pick up stage/build changes is miserable,
it made me long for Jenkinsfile / .travis.yml / GitLabCI.

The functional tests I added ensure that the API generates the specified
text AND makes sure that it's returning an epoch time within a minute of what
it should be. It's done against an ephemeral CloudFormation deployment of the
Lambda, to prevent the actual deployment stack needing to roll back on a bad commit.

I don't love the way functional testing kinda has to go when you're deploying
with a CloudFormation stack. I'd love to do a staged deploy with live validation
that the API is performing within spec, and a rollback if not. That's not
something well-supported with CFN.
