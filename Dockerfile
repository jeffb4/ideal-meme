ARG POETRY_ARGS="--no-dev"
ARG POETRY_VERSION="1.1.7"

FROM python:3-buster

ARG POETRY_ARGS
ARG POETRY_VERSION

WORKDIR /app

# Sets utf-8 encoding for Python et al
ENV LANG=C.UTF-8
# Turns off writing .pyc files; superfluous on an ephemeral container.
ENV PYTHONDONTWRITEBYTECODE=1
# Seems to speed things up
ENV PYTHONUNBUFFERED=1

# Ensures that the python and pip executables used
# in the image will be those from our virtualenv.
ENV PATH="/venv/bin:$PATH"

COPY . ./

# Setup the virtualenv
RUN python -m venv /venv \
    && /venv/bin/pip install poetry==${POETRY_VERSION} awscli \
    && poetry config virtualenvs.create false \
    && cd /app/pipeline \
    && poetry install --no-root ${POETRY_ARGS} \
    && /venv/bin/pip install colorama \
    && apt update \
    && apt install -y jq nodejs npm \
    && npm install -g aws-cdk

CMD [ "/app/entrypoint.sh" ]