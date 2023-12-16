from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CANCELED: TrainingStatus
COMPLETED: TrainingStatus
DELETED: TrainingStatus
DESCRIPTOR: _descriptor.FileDescriptor
FAILED: TrainingStatus
PENDING: TrainingStatus
PLACEHOLDER_UNSET: TrainingStatus
QUEUED: TrainingStatus
RUNNING: TrainingStatus
SUSPENDED: TrainingStatus

class TrainingInfoRequest(_message.Message):
    __slots__ = ["training_id"]
    TRAINING_ID_FIELD_NUMBER: _ClassVar[int]
    training_id: str
    def __init__(self, training_id: _Optional[str] = ...) -> None: ...

class TrainingJob(_message.Message):
    __slots__ = ["model_name", "training_id"]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    TRAINING_ID_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    training_id: str
    def __init__(self, training_id: _Optional[str] = ..., model_name: _Optional[str] = ...) -> None: ...

class TrainingParameters(_message.Message):
    __slots__ = ["base_model", "bf16", "data_path", "dataset_text_field", "evaluation_strategy", "fsdp", "fsdp_config", "gradient_accumulation_steps", "include_tokens_per_second", "learning_rate", "logging_steps", "lr_scheduler_type", "num_train_epochs", "packing", "per_device_eval_batch_size", "per_device_train_batch_size", "response_template", "save_strategy", "warmup_ratio", "weight_decay"]
    BASE_MODEL_FIELD_NUMBER: _ClassVar[int]
    BF16_FIELD_NUMBER: _ClassVar[int]
    DATASET_TEXT_FIELD_FIELD_NUMBER: _ClassVar[int]
    DATA_PATH_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    FSDP_CONFIG_FIELD_NUMBER: _ClassVar[int]
    FSDP_FIELD_NUMBER: _ClassVar[int]
    GRADIENT_ACCUMULATION_STEPS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TOKENS_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    LEARNING_RATE_FIELD_NUMBER: _ClassVar[int]
    LOGGING_STEPS_FIELD_NUMBER: _ClassVar[int]
    LR_SCHEDULER_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUM_TRAIN_EPOCHS_FIELD_NUMBER: _ClassVar[int]
    PACKING_FIELD_NUMBER: _ClassVar[int]
    PER_DEVICE_EVAL_BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    PER_DEVICE_TRAIN_BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    SAVE_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    WARMUP_RATIO_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_DECAY_FIELD_NUMBER: _ClassVar[int]
    base_model: str
    bf16: bool
    data_path: str
    dataset_text_field: str
    evaluation_strategy: str
    fsdp: str
    fsdp_config: str
    gradient_accumulation_steps: int
    include_tokens_per_second: bool
    learning_rate: float
    logging_steps: int
    lr_scheduler_type: str
    num_train_epochs: int
    packing: bool
    per_device_eval_batch_size: int
    per_device_train_batch_size: int
    response_template: str
    save_strategy: str
    warmup_ratio: float
    weight_decay: float
    def __init__(self, base_model: _Optional[str] = ..., data_path: _Optional[str] = ..., bf16: bool = ..., num_train_epochs: _Optional[int] = ..., per_device_train_batch_size: _Optional[int] = ..., per_device_eval_batch_size: _Optional[int] = ..., gradient_accumulation_steps: _Optional[int] = ..., evaluation_strategy: _Optional[str] = ..., save_strategy: _Optional[str] = ..., learning_rate: _Optional[float] = ..., weight_decay: _Optional[float] = ..., warmup_ratio: _Optional[float] = ..., lr_scheduler_type: _Optional[str] = ..., logging_steps: _Optional[int] = ..., fsdp: _Optional[str] = ..., fsdp_config: _Optional[str] = ..., include_tokens_per_second: bool = ..., packing: bool = ..., response_template: _Optional[str] = ..., dataset_text_field: _Optional[str] = ...) -> None: ...

class TrainingRequest(_message.Message):
    __slots__ = ["model_name", "output_path", "parameters"]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_PATH_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    output_path: str
    parameters: TrainingParameters
    def __init__(self, model_name: _Optional[str] = ..., output_path: _Optional[str] = ..., parameters: _Optional[_Union[TrainingParameters, _Mapping]] = ...) -> None: ...

class TrainingStatusResponse(_message.Message):
    __slots__ = ["completion_timestamp", "reasons", "state", "submission_timestamp", "training_id"]
    COMPLETION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    REASONS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SUBMISSION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TRAINING_ID_FIELD_NUMBER: _ClassVar[int]
    completion_timestamp: _timestamp_pb2.Timestamp
    reasons: _containers.RepeatedScalarFieldContainer[str]
    state: TrainingStatus
    submission_timestamp: _timestamp_pb2.Timestamp
    training_id: str
    def __init__(self, training_id: _Optional[str] = ..., state: _Optional[_Union[TrainingStatus, str]] = ..., submission_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., completion_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., reasons: _Optional[_Iterable[str]] = ...) -> None: ...

class TrainingStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
