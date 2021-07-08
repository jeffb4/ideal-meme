# ideal-meme

Gaggle coding exercise repository

## Usage

### Prerequisites

- Docker

- AWS access

### Running

    docker run -v ${HOME}/.aws:/root/.aws \
      -e AWS_ACCESS_KEY_ID \
      -e AWS_SECRET_ACCESS_KEY \
      -e AWS_SESSION_TOKEN jeffb4/ideal-meme

## Development

### Structure

- `cdkrunner` - command-line utility to launch a pre-defined AWS CDK stack. Used

### Building

make docker

### Testing

A CodePipeline is automatically created
