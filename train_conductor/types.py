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
from enum import Enum


class TrainingStatus(Enum):
    PLACEHOLDER_UNSET = 0
    PENDING = 1
    QUEUED = 2
    RUNNING = 3
    SUSPENDED = 4
    COMPLETED = 5
    CANCELED = 6
    FAILED = 7
    DELETED = 8


UNCOMPLETED_STATES = [
    TrainingStatus.PENDING,
    TrainingStatus.PLACEHOLDER_UNSET,
    TrainingStatus.QUEUED,
    TrainingStatus.RUNNING,
]

COMPLETED_STATES = [
    TrainingStatus.CANCELED,
    TrainingStatus.COMPLETED,
    TrainingStatus.DELETED,
    TrainingStatus.FAILED,
    TrainingStatus.SUSPENDED,
]
