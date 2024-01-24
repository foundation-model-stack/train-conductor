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
import random


class MockRedis:
    def __init__(self, cache=dict(), *args, **kwargs):
        self.cache = cache

    def get(self, key):
        """Emulate get."""
        if key in self.cache:
            return self.cache[key]

    def set(self, key, value, *args, **kwargs):
        """Emulate set."""
        if self.cache:
            self.cache[key] = value
            return "OK"

    def hget(self, hash, key):
        """Emulate hget."""
        if hash in self.cache:
            if key in self.cache[hash]:
                return self.cache[hash][key]

    def hset(self, hash, key, value, *args, **kwargs):
        """Emulate hset."""
        if self.cache:
            self.cache[hash][key] = value
            return 1

    def exists(self, key):
        """Emulate exists."""
        if key in self.cache:
            return 1
        return 0

    def scan(self, cursor=None, match=None):
        """Emulate scan."""
        return 0, self.cache.keys()

    def pipeline(self):
        """Emulate a redis-python pipeline."""
        return MockRedisPipeline(self)

    def cache_overwrite(self, cache=dict()):
        self.cache = cache

    def pubsub(self):
        """Emulate pubsub."""
        return MockRedisPubSub()


class MockRedisPubSub:
    def psubscribe(self, *args, **kwargs):
        """Emulate psubscribe."""
        pass

    def run_in_thread(self, *args, **kwargs):
        """Emulate run_in_thread."""
        pass


class MockRedisPipeline:
    """Imitate a redis-python pipeline object so unit tests can run without
    needing a real Redis server."""

    result = []

    def __init__(self, redis):
        self.redis = redis

    def execute(self):
        """Emulate the execute method. All piped commands are executed immediately in this mock, so
        this is a no-op."""
        return self.result

    def hgetall(self, hashkey):
        """Emulate hgetall."""
        self.result.append(self.redis[hashkey])
