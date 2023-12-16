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
import abc

class DatabaseBase(abc.ABC):

    @abc.abstractclassmethod
    def __init__(self, config: dict) -> None:
        super().__init__()

    @abc.abstractclassmethod
    def write_record(self, key: str, record: dict):
        """
        Write a record to the database
        """

    @abc.abstractclassmethod
    def read_record(self, key: str) -> dict:
        """
        Given an entry key, read a record from the database
        """

    @abc.abstractclassmethod
    def read_field(self, key: str, field: str):
        """
        Given an entry key and a field name, return value of field
        """

    @abc.abstractclassmethod
    def write_field(self, key: str, field: str, value):
        """
        Given an entry key and a field name, return value of field
        """

    @abc.abstractclassmethod
    def has_key(self, key: str) -> bool:
        """
        Indicates whether a key exists in a database
        """

    @abc.abstractclassmethod
    def iterate_entries(self, filter: str):
        """
        Return an object that allows the caller to iterate over a list of records
        """

    @abc.abstractclassmethod
    def read_many_entries(keys):
        """
        Given a list of keys, return a list of records
        """

    def get_client(self):
        return self._client