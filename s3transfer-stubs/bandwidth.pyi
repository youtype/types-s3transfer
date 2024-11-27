"""
Type annotations for s3transfer.bandwidth module.

Copyright 2024 Vlad Emelianov
"""

from typing import IO, Any, TypeVar

from s3transfer.futures import TransferCoordinator

_R = TypeVar("_R")

class RequestExceededException(Exception):
    def __init__(self, requested_amt: int, retry_time: float) -> None:
        self.requested_amt: int
        self.retry_time: float

class RequestToken: ...

class TimeUtils:
    def time(self) -> float: ...
    def sleep(self, value: float) -> None: ...

class BandwidthLimiter:
    def __init__(self, leaky_bucket: LeakyBucket, time_utils: TimeUtils | None = ...) -> None: ...
    def get_bandwith_limited_stream(
        self,
        fileobj: IO[Any] | str | bytes,
        transfer_coordinator: TransferCoordinator,
        enabled: bool = ...,
    ) -> BandwidthLimitedStream: ...

class BandwidthLimitedStream:
    def __init__(
        self,
        fileobj: IO[Any] | str | bytes,
        leaky_bucket: LeakyBucket,
        transfer_coordinator: TransferCoordinator,
        time_utils: TimeUtils | None = ...,
        bytes_threshold: int = ...,
    ) -> None: ...
    def enable_bandwidth_limiting(self) -> None: ...
    def disable_bandwidth_limiting(self) -> None: ...
    def read(self, amount: int) -> str: ...
    def signal_transferring(self) -> None: ...
    def signal_not_transferring(self) -> None: ...
    def seek(self, where: int, whence: int = ...) -> None: ...
    def tell(self) -> int: ...
    def close(self) -> None: ...
    def __enter__(self: _R) -> _R: ...
    def __exit__(self, *args: object, **kwargs: Any) -> None: ...

class LeakyBucket:
    def __init__(
        self,
        max_rate: int,
        time_utils: TimeUtils | None = ...,
        rate_tracker: BandwidthRateTracker | None = ...,
        consumption_scheduler: ConsumptionScheduler | None = ...,
    ) -> None: ...
    def consume(self, amt: int, request_token: RequestToken) -> int: ...

class ConsumptionScheduler:
    def __init__(self) -> None: ...
    def is_scheduled(self, token: RequestToken) -> bool: ...
    def schedule_consumption(
        self, amt: int, token: RequestToken, time_to_consume: float
    ) -> float: ...
    def process_scheduled_consumption(self, token: RequestToken) -> None: ...

class BandwidthRateTracker:
    def __init__(self, alpha: float = ...) -> None: ...
    @property
    def current_rate(self) -> float: ...
    def get_projected_rate(self, amt: int, time_at_consumption: float) -> float: ...
    def record_consumption_rate(self, amt: int, time_at_consumption: float) -> None: ...
