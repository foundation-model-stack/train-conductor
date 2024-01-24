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
from kubernetes.client import V1JobList, V1ListMeta


class MockK8sBatchV1Api:
    def __init__(self):
        self.job_list = V1JobList(items=[], metadata=V1ListMeta(resource_version=5000))

    def list_namespaced_job(self, *args, **kwargs):
        if self.job_list:
            return self.job_list

    def read_namespaced_job(self, name, *args, **kwargs):
        for job in self.job_list.items:
            if job.name == name:
                return job
