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
import logging
import sys
import os
from concurrent import futures
import urllib3


# First Party
from aconfig import Config

# Third Party
import grpc
from grpc_reflection.v1alpha import reflection

# Local
from train_conductor.protobuf import trainconductor_pb2, trainconductor_pb2_grpc
from train_conductor.training_servicer import TrainingServicer
from train_conductor.modules.watcher import Watcher
from train_conductor.utils import error_check

# TPP TODO: validate params before writing to db


class TrainingGRPCServer:
    def __init__(self, config_path: str):
        self.config = Config.from_yaml(config_path)

        if not os.environ.get("DISABLE_GRPC"):
            # Start tracking service names for reflection
            service_names = [reflection.SERVICE_NAME]

            self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

            trainconductor_pb2_grpc.add_TrainConductorServicer_to_server(
                TrainingServicer(self.config), self.server
            )
            service_names.append(
                trainconductor_pb2.DESCRIPTOR.services_by_name["TrainConductor"].full_name
            )

            # Finally enable service reflection after all services are added
            reflection.enable_server_reflection(service_names, self.server)

            self.server.add_insecure_port("[::]:8085")
            self.server.start()

        if not os.environ.get("DISABLE_WATCHER"):
            Watcher(self.config)
        self.server.wait_for_termination()


if __name__ == "__main__":
    config_file = "runtime_config.yml"
    if os.environ.get("RUNTIME_CONFIG_FILE"):
        config_file = os.environ.get("RUNTIME_CONFIG_FILE")
    error_check.file_check("<TCD74240296E>", config_file)

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    # TODO: Hack to supress certificate check warnings. Needs fixing.
    urllib3.disable_warnings()
    TrainingGRPCServer(config_file)
