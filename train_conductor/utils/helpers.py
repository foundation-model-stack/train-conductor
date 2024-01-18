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
from datetime import datetime

# Third Party
from google.protobuf import timestamp_pb2


def convert_timestamp(ts_str):
    ts_dt = datetime.strptime(ts_str, "%m/%d/%Y %H:%M:%S")
    return timestamp_pb2.Timestamp(
        seconds=int(ts_dt.timestamp()), nanos=int(ts_dt.microsecond * 1e3)
    )
