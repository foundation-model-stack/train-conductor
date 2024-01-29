FROM registry.access.redhat.com/ubi9/ubi-minimal:latest

RUN mkdir /app
WORKDIR /app
COPY pyproject.toml /tmp/train-conductor/pyproject.toml
COPY README.md /tmp/train-conductor/README.md
COPY train_conductor /tmp/train-conductor/train_conductor

RUN microdnf install -y python3.11 python3.11-pip
RUN python3.11 -m pip install /tmp/train-conductor
COPY runtime_config.yml /app

RUN true \
    && microdnf update -y \
    && microdnf clean all \
    && true

RUN chown -R 1000:1000 /app
RUN chown -R 1000:1000 /tmp/train-conductor

USER 1000

CMD [ "python3.11", "-m", "train_conductor.grpc_server"]
