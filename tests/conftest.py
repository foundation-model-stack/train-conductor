# Copyright The Train Conductor Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Standard
from contextlib import contextmanager
import os
import tempfile

# First Party
from aconfig import Config


# Third Party
import pytest
from pytest_mock import MockerFixture


# Local
from train_conductor.grpc_server import TrainingGRPCServer
from train_conductor.training_servicer import TrainingServicer
from tests.fixtures.mock_redis_client import MockK8sBatchV1Api, MockRedis

TEST_CONFIG_PATH = "tests/test_config.yml"


@pytest.fixture(scope="session")
def sample_train_servicer(sample_train_service) -> TrainingServicer:
    servicer = TrainingServicer(Config.from_yaml(TEST_CONFIG_PATH))
    yield servicer


@contextmanager
def runtime_grpc_test_server(session_mocker, *args, **kwargs):
    """Helper to wrap creation of RuntimeGRPCServer in temporary configurations"""
    with tempfile.TemporaryDirectory() as workdir:
        temp_log_dir = os.path.join(workdir, "metering_logs")
        temp_save_dir = os.path.join(workdir, "training_output")
        os.makedirs(temp_log_dir)
        os.makedirs(temp_save_dir)
        session_mocker.patch(
            "kubernetes.config.load_incluster_config", return_value=None
        )
        session_mocker.patch(
            "kubernetes.config.load_kube_config", return_value="ignore"
        )
        session_mocker.patch("kubernetes.client.BatchV1Api", MockK8sBatchV1Api)
        session_mocker.patch("redis.Redis", MockRedis)

        with TrainingGRPCServer(TEST_CONFIG_PATH) as server:
            # Give tests access to the workdir
            server.workdir = workdir
            yield server


@pytest.fixture(scope="session")
def runtime_grpc_server(session_mocker) -> TrainingGRPCServer:
    with runtime_grpc_test_server(session_mocker) as server:
        _check_server_readiness(server)
        yield server
