# Copyright The Caikit Authors
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
import base64
import os
import pickle
import logging

# First Party
from train_conductor.utils import error_check as error
import logging


def txt_to_obj(txt):
    base64_bytes = txt.encode("ascii")
    message_bytes = base64.b64decode(base64_bytes)
    obj = pickle.loads(message_bytes)
    return obj


def main():
    logging.info("Job has commenced to kick off training")

    runtime_env = txt_to_obj(os.environ.get("JOB_CONFIG_JSON_ENV_VAR"))

    # Identify our target training module and do basic parameter validation.
    module_class_ref = runtime_env.get("module_class")
    error.value_check("<TCD46582584E>", module_class_ref is not None)
    module_class = txt_to_obj(module_class_ref)

    # The entire kwargs dict should have been serialized as a whole
    serialized_kwargs = runtime_env.get("kwargs")
    kwargs = {}
    if serialized_kwargs:
        error.type_check("<TCD26466208E>", dict, kwargs=kwargs)
        for key, value in serialized_kwargs.items():
            kwargs[key] = txt_to_obj(value)

    # Deserialize each item in the args list
    serialized_args = runtime_env.get("args")
    args = []
    for arg in serialized_args:
        arg = txt_to_obj(arg)
        args.append(arg)

    model_path = runtime_env.get("save_path")
    if model_path:
        error.type_check("<TCD70238308E>", str, model_path=model_path)

    # Finally kick off trainig

    logging.debug("<TCD57616295D>", "Beginning training")

    model = module_class.train(*args, **kwargs)

    logging.debug("<TCD45386862D>", "Training complete, beginning save")
    model.save(model_path)

    logging.debug("<TCD39131219D>", "Save complete")



if __name__ == "__main__":
    main()
