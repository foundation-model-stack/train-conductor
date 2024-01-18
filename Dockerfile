FROM registry.access.redhat.com/ubi9/ubi-minimal:latest

RUN cd ~ && \
    curl -L -O https://repo.anaconda.com/miniconda/Miniconda3-py311_23.10.0-1-Linux-x86_64.sh && \
    chmod +x Miniconda3-*-Linux-x86_64.sh && \
    bash ./Miniconda3-*-Linux-x86_64.sh -bf -p /opt/miniconda

ENV PATH=/opt/miniconda/bin:$PATH

RUN mkdir /app
WORKDIR /app
COPY pyproject.toml /tmp/train-conductor/pyproject.toml
COPY README.md /tmp/train-conductor/README.md
COPY train_conductor /tmp/train-conductor/train_conductor

RUN python -m pip install /tmp/train-conductor
COPY runtime_config.yml /app

RUN true \
    && microdnf update \
    && microdnf clean all \
    && true

RUN chown -R 1000:1000 /app
RUN chown -R 1000:1000 /tmp/train-conductor

USER 1000

CMD [ "python", "-m", "train_conductor.grpc_server"]
