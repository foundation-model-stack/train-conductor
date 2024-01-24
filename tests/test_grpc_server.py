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

# Third Party
from kubernetes import client

# Local
from tests.conftest import runtime_grpc_server


def test_run_server(mocker, runtime_grpc_server):
    with runtime_grpc_server() as server:
        print("hi")
    client.BatchV1Api.create_namespaced_job.assert_called_with(
        name="some-name", namespace="test-namespace"
    )
