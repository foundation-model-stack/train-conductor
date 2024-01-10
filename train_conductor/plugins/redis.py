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
import os
import logging

# Third Party
import redis
import aconfig

# Local
from train_conductor.interfaces.database import DatabaseBase
from train_conductor.utils.error_check import type_check, file_check


class RedisHelper(DatabaseBase):
    def __init__(self, config: aconfig.Config):
        self.config = config
        logging.info("Attempting connection to Redis")
        redis_config = self.config.datastore.connection
        redis_host = redis_config.host
        type_check("<TCD47773352E>", str, redis_host=redis_host)
        redis_port = redis_config.port
        type_check("<TCD47773353E>",int, redis_port=redis_port)
        redis_db_num = redis_config.db_num
        type_check("<TCD47773354E>", int, redis_db_num=redis_db_num)
        user = redis_config.user or None
        password = os.environ.get("REDIS_PASSWORD")
        ca_cert = os.environ.get("REDIS_CA_FILE")
        if ca_cert:
            file_check("<TCD08017879E>", ca_cert)
        ssl_enable = False
        if ca_cert:
            ssl_enable = True
        self._client = redis.Redis(
            host=redis_host, port=redis_port, db=redis_db_num, decode_responses=True,
            username=user, password=password, ssl_ca_certs=ca_cert, ssl=ssl_enable
        )

    def write_record(self, key: str, record: dict) -> int:
        added_fields = self._client.hset(key, mapping=record)
        return added_fields

    def write_field(self, key: str, field: str, value):
        added_fields = self._client.hset(key, field, value)
        return added_fields

    def read_record(self, key: str) -> dict:
        record = self._client.hgetall(key)
        return record

    def read_field(self, key: str, field: str):
        return self._client.hget(key, field)

    def has_key(self, key: str) -> bool:
        return self._client.exists(key)

    def iterate_entries(self, filter: str = None, cursor=None):
        return self._client.scan(cursor=cursor, match=filter)

    def read_many_entries(self, keys):
        return self._client.mget(keys)

    def start_listener(self, db_update_event_handler):
        def exit_event_handler(msg):
            print(msg)
            thread.stop()

        pubsub = self._client.pubsub()
        pubsub.psubscribe(**{"__keyspace@0__:*": db_update_event_handler})
        pubsub.psubscribe(**{"__keyevent@0__:expired": exit_event_handler})
        thread = pubsub.run_in_thread(sleep_time=0.01)
