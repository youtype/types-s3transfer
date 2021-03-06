from typing import IO, Any, Callable, Iterator, List, Optional, Sequence, Tuple, TypeVar, Union

from s3transfer.bandwidth import BandwidthLimiter
from s3transfer.compat import readable as readable
from s3transfer.compat import seekable as seekable
from s3transfer.futures import IN_MEMORY_UPLOAD_TAG as IN_MEMORY_UPLOAD_TAG
from s3transfer.futures import TransferCoordinator, TransferFuture
from s3transfer.manager import TransferConfig
from s3transfer.tasks import CompleteMultipartUploadTask as CompleteMultipartUploadTask
from s3transfer.tasks import CreateMultipartUploadTask as CreateMultipartUploadTask
from s3transfer.tasks import SubmissionTask as SubmissionTask
from s3transfer.tasks import Task as Task
from s3transfer.utils import ChunksizeAdjuster as ChunksizeAdjuster
from s3transfer.utils import DeferredOpenFile as DeferredOpenFile
from s3transfer.utils import OSUtils, ReadFileChunk
from s3transfer.utils import get_callbacks as get_callbacks
from s3transfer.utils import get_filtered_dict as get_filtered_dict

_R = TypeVar("_R")

class AggregatedProgressCallback:
    def __init__(self, callbacks: Sequence[Callable[..., Any]], threshold: int = ...) -> None: ...
    def __call__(self, bytes_transferred: int) -> None: ...
    def flush(self) -> None: ...

class InterruptReader:
    def __init__(
        self, fileobj: Union[IO[Any], str, bytes], transfer_coordinator: TransferCoordinator
    ) -> None: ...
    def read(self, amount: Optional[int] = ...) -> str: ...
    def seek(self, where: int, whence: int = ...) -> None: ...
    def tell(self) -> int: ...
    def close(self) -> None: ...
    def __enter__(self: _R) -> _R: ...
    def __exit__(self, *args: Any, **kwargs: Any) -> None: ...

class UploadInputManager:
    def __init__(
        self,
        osutil: OSUtils,
        transfer_coordinator: TransferCoordinator,
        bandwidth_limiter: Optional[BandwidthLimiter] = ...,
    ) -> None: ...
    @classmethod
    def is_compatible(cls, upload_source: Any) -> bool: ...
    def stores_body_in_memory(self, operation_name: str) -> bool: ...
    def provide_transfer_size(self, transfer_future: TransferFuture) -> None: ...
    def requires_multipart_upload(
        self, transfer_future: TransferFuture, config: TransferConfig
    ) -> bool: ...
    def get_put_object_body(self, transfer_future: TransferFuture) -> bytes: ...
    def yield_upload_part_bodies(
        self, transfer_future: TransferFuture, chunksize: int
    ) -> Iterator[Tuple[int, ReadFileChunk]]: ...

class UploadFilenameInputManager(UploadInputManager):
    @classmethod
    def is_compatible(cls, upload_source: Any) -> bool: ...
    def stores_body_in_memory(self, operation_name: str) -> bool: ...
    def provide_transfer_size(self, transfer_future: TransferFuture) -> None: ...
    def requires_multipart_upload(
        self, transfer_future: TransferFuture, config: TransferConfig
    ) -> bool: ...
    def get_put_object_body(self, transfer_future: TransferFuture) -> bytes: ...
    def yield_upload_part_bodies(
        self, transfer_future: TransferFuture, chunksize: int
    ) -> Iterator[Tuple[int, ReadFileChunk]]: ...

class UploadSeekableInputManager(UploadFilenameInputManager):
    @classmethod
    def is_compatible(cls, upload_source: Any) -> bool: ...
    def stores_body_in_memory(self, operation_name: str) -> bool: ...
    def provide_transfer_size(self, transfer_future: TransferFuture) -> None: ...

class UploadNonSeekableInputManager(UploadInputManager):
    def __init__(
        self,
        osutil: OSUtils,
        transfer_coordinator: TransferCoordinator,
        bandwidth_limiter: Optional[BandwidthLimiter] = ...,
    ) -> None: ...
    @classmethod
    def is_compatible(cls, upload_source: Any) -> bool: ...
    def stores_body_in_memory(self, operation_name: str) -> bool: ...
    def provide_transfer_size(self, transfer_future: TransferFuture) -> None: ...
    def requires_multipart_upload(
        self, transfer_future: TransferFuture, config: TransferConfig
    ) -> bool: ...
    def get_put_object_body(self, transfer_future: TransferFuture) -> bytes: ...
    def yield_upload_part_bodies(
        self, transfer_future: TransferFuture, chunksize: int
    ) -> Iterator[Tuple[int, ReadFileChunk]]: ...

class UploadSubmissionTask(SubmissionTask):
    UPLOAD_PART_ARGS: List[str]
    COMPLETE_MULTIPART_ARGS: List[str]

class PutObjectTask(Task): ...
class UploadPartTask(Task): ...
