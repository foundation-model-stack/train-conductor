REPO_ROOT	    := $(shell pwd)
REPO_ROOT_BIN	:= ${REPO_ROOT}/bin
OS 				:= $(shell uname)
ARCH 			:= $(shell arch)
CONTAINER_ENGINE ?= podman

ifeq ($(OS),Darwin)
	OS_="osx"
endif

ifeq ($(ARCH), arm64)
	ARCH_ := "aarch_64"
endif
# Test Setup
KIND_CLUSTER_NAME ?= train-conductor-cluster
KIND ?= $(REPO_ROOT_BIN)/kind
PROTOC ?= $(REPO_ROOT_BIN)/bin/protoc
IMG ?= localhost/train-conductor
IMG_TAG ?= latest


$(REPO_ROOT_BIN):
	mkdir -p $(REPO_ROOT_BIN)

# Build
.PHONY: python-pb
python-pb: protoc-python-plugin
	python -m grpc_tools.protoc -I ${REPO_ROOT}/train_conductor/interfaces/ --python_out=${REPO_ROOT}/train_conductor/protobuf/ --pyi_out=${REPO_ROOT}/train_conductor/protobuf/ --grpc_python_out=${REPO_ROOT}/train_conductor/protobuf/  trainconductor.proto

.PHONY: docker-image
docker-image:
	${CONTAINER_ENGINE} build -t ${IMG}:${IMG_TAG} .

.PHONE: push-image
push-image:
	${CONTAINER_ENGINE} push ${IMG}:${IMG_TAG}

.PHONY: load-docker-image
load-image:
	${KIND} load docker-image ${IMG}:${IMG_TAG} -n $(KIND_CLUSTER_NAME)

# Deploy

.PHONY: deploy
deploy:
	kubectl apply -f ${REPO_ROOT}/deployment/runtime_configmap.yaml
	kubectl apply -f ${REPO_ROOT}/deployment/deployment-kind.yaml

.PHONY: undeploy
undeploy:
	kubectl delete -f ${REPO_ROOT}/deployment/runtime_configmap.yaml
	kubectl delete -f ${REPO_ROOT}/deployment/deployment-kind.yaml

# Download KinD
.PHONY: kind
kind: $(KIND)
$(KIND): $(REPO_ROOT_BIN)
	test -s $(KIND) || curl -Lo $(REPO_ROOT_BIN)/kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-${OS}-${ARCH}
	chmod +x $(REPO_ROOT_BIN)/kind


# Install python grpc code generator
.PHONY: protoc-python-plugin
protoc-python-plugin:
	python -m pip show grpcio-tools || python -m pip install -y grpcio-tools

.PHONY: cluster
cluster: $(KIND) ## Start kind development cluster.
	$(KIND) create cluster -n $(KIND_CLUSTER_NAME)

# Clean up
.PHONY: delete-cluster
delete-cluster: kind
	$(KIND) delete cluster -n $(KIND_CLUSTER_NAME)

