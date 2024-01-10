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
import importlib
from uuid import uuid4
import json
from datetime import datetime

# First Party
from aconfig import Config

# Third Party
from google.protobuf import timestamp_pb2
from google.protobuf.message import Message as ProtoMessageType
from grpc import ServicerContext
from google.protobuf.json_format import MessageToDict

# Local
from .protobuf import trainconductor_pb2_grpc
from .protobuf.trainconductor_pb2 import TrainingStatusResponse, TrainingJob
from train_conductor.interfaces import TrainingStatus


class TrainingServicer(trainconductor_pb2_grpc.TrainConductorServicer):
    """Provides methods that implement functionality of training servicer"""

    def __init__(self, config: Config):
        self.config = config
        db_helper_cls = getattr(
            importlib.import_module(self.config.datastore.helper_module_path),
            self.config.datastore.helper_class,
        )
        self.db_client = db_helper_cls(self.config)

    def Train(self, request: ProtoMessageType, context: ServicerContext):
        """Fine-tune a model using HF SFT Trainer"""
        try:
            job_id = str(uuid4())
            request_dict = MessageToDict(request, preserving_proto_field_name=True)
            param_dict = request_dict.get("parameters")
            param_dict["output_dir"] = request_dict.get("output_path") or self.config.trainer_config.output_dir
            params = json.dumps(param_dict, indent=4)
            request_dict.pop("parameters")
            request_dict.update(
                {"parameters": params, "status": TrainingStatus.PLACEHOLDER_UNSET.name}
            )
            self.db_client.write_record(job_id, request_dict)
            return TrainingJob(
                training_id=job_id, model_name=request_dict.get("model_name")
            )
        except Exception as err:
            raise Exception("Unhandled exception during training") from err

    def GetTrainingStatus(self, request: ProtoMessageType, context: ServicerContext):
        """Get the status of a training job"""
        try:
            training_info = self.db_client.read_record(request.training_id)
            submission_timestamp = training_info.get("submission_timestamp")
            completion_timestamp = training_info.get("completion_timestamp")
            return TrainingStatusResponse(
                training_id=request.training_id,
                state=training_info.get("status"),
                reasons=[str(error) for error in training_info.get("errors")]
                if training_info.get("errors")
                else [],
                submission_timestamp=self._convert_timestamp(submission_timestamp)
                if submission_timestamp
                else None,
                completion_timestamp=self._convert_timestamp(completion_timestamp)
                if completion_timestamp
                else None,
            )
        except Exception as err:
            raise Exception(
                "Failed to get status for training id {}".format(request.training_id)
            ) from err

    def CancelTraining(self, request: ProtoMessageType, context: ServicerContext):
        """Cancel a training job."""
        try:
            self.db_client.write_field(
                request.training_id, "status", TrainingStatus.CANCELED.name
            )

            training_info = self.db_client.read_record(request.training_id)

            return TrainingStatusResponse(
                training_id=request.training_id,
                state=training_info.get("status"),
                reasons=[str(error) for error in training_info.get("errors")]
                if training_info.get("errors")
                else [],
            )
        except Exception as err:
            raise Exception(
                "Failed to cancel training for training id {}".format(
                    request.training_id
                )
            ) from err

    def _convert_timestamp(self, ts_str):
        ts_dt = datetime.strptime(ts_str, "%m/%d/%Y %H:%M:%S")
        return timestamp_pb2.Timestamp(
            seconds=int(ts_dt.timestamp()), nanos=int(ts_dt.microsecond * 1e3)
        )
