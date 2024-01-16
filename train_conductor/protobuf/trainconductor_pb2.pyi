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
    __slots__ = ["bias", "data_path", "dataset_text_field", "fsdp", "fsdp_config", "gradient_accumulation_steps", "include_tokens_per_second", "learning_rate", "logging_steps", "lora_alpha", "lora_dropout", "lr_scheduler_type", "model_max_length", "model_name_or_path", "num_train_epochs", "num_virtual_tokens", "packing", "peft_method", "per_device_eval_batch_size", "per_device_train_batch_size", "prompt_tuning_init", "prompt_tuning_init_text", "r", "response_template", "target_modules", "tokenizer_name_or_path", "torch_dytpe", "use_flash_attn", "warmup_ratio", "weight_decay"]
    BIAS_FIELD_NUMBER: _ClassVar[int]
    DATASET_TEXT_FIELD_FIELD_NUMBER: _ClassVar[int]
    DATA_PATH_FIELD_NUMBER: _ClassVar[int]
    FSDP_CONFIG_FIELD_NUMBER: _ClassVar[int]
    FSDP_FIELD_NUMBER: _ClassVar[int]
    GRADIENT_ACCUMULATION_STEPS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TOKENS_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    LEARNING_RATE_FIELD_NUMBER: _ClassVar[int]
    LOGGING_STEPS_FIELD_NUMBER: _ClassVar[int]
    LORA_ALPHA_FIELD_NUMBER: _ClassVar[int]
    LORA_DROPOUT_FIELD_NUMBER: _ClassVar[int]
    LR_SCHEDULER_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_MAX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_OR_PATH_FIELD_NUMBER: _ClassVar[int]
    NUM_TRAIN_EPOCHS_FIELD_NUMBER: _ClassVar[int]
    NUM_VIRTUAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
    PACKING_FIELD_NUMBER: _ClassVar[int]
    PEFT_METHOD_FIELD_NUMBER: _ClassVar[int]
    PER_DEVICE_EVAL_BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    PER_DEVICE_TRAIN_BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    PROMPT_TUNING_INIT_FIELD_NUMBER: _ClassVar[int]
    PROMPT_TUNING_INIT_TEXT_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    TARGET_MODULES_FIELD_NUMBER: _ClassVar[int]
    TOKENIZER_NAME_OR_PATH_FIELD_NUMBER: _ClassVar[int]
    TORCH_DYTPE_FIELD_NUMBER: _ClassVar[int]
    USE_FLASH_ATTN_FIELD_NUMBER: _ClassVar[int]
    WARMUP_RATIO_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_DECAY_FIELD_NUMBER: _ClassVar[int]
    bias: float
    data_path: str
    dataset_text_field: str
    fsdp: str
    fsdp_config: str
    gradient_accumulation_steps: int
    include_tokens_per_second: bool
    learning_rate: float
    logging_steps: str
    lora_alpha: int
    lora_dropout: float
    lr_scheduler_type: str
    model_max_length: int
    model_name_or_path: str
    num_train_epochs: float
    num_virtual_tokens: int
    packing: bool
    peft_method: str
    per_device_eval_batch_size: int
    per_device_train_batch_size: int
    prompt_tuning_init: str
    prompt_tuning_init_text: str
    r: int
    response_template: str
    target_modules: _containers.RepeatedScalarFieldContainer[str]
    tokenizer_name_or_path: str
    torch_dytpe: str
    use_flash_attn: bool
    warmup_ratio: float
    weight_decay: float
    def __init__(self, model_name_or_path: _Optional[str] = ..., data_path: _Optional[str] = ..., num_train_epochs: _Optional[float] = ..., per_device_train_batch_size: _Optional[int] = ..., per_device_eval_batch_size: _Optional[int] = ..., gradient_accumulation_steps: _Optional[int] = ..., learning_rate: _Optional[float] = ..., weight_decay: _Optional[float] = ..., warmup_ratio: _Optional[float] = ..., lr_scheduler_type: _Optional[str] = ..., logging_steps: _Optional[str] = ..., fsdp: _Optional[str] = ..., fsdp_config: _Optional[str] = ..., include_tokens_per_second: bool = ..., packing: bool = ..., response_template: _Optional[str] = ..., dataset_text_field: _Optional[str] = ..., use_flash_attn: bool = ..., torch_dytpe: _Optional[str] = ..., model_max_length: _Optional[int] = ..., peft_method: _Optional[str] = ..., r: _Optional[int] = ..., lora_alpha: _Optional[int] = ..., target_modules: _Optional[_Iterable[str]] = ..., bias: _Optional[float] = ..., lora_dropout: _Optional[float] = ..., prompt_tuning_init: _Optional[str] = ..., num_virtual_tokens: _Optional[int] = ..., prompt_tuning_init_text: _Optional[str] = ..., tokenizer_name_or_path: _Optional[str] = ...) -> None: ...

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
