import os
from multiprocessing.managers import BaseManager as _BaseManager
from typing import IO, Any, Callable, Type, Union

rename_file = os.rename

class BaseManager(_BaseManager):
    def shutdown(self) -> None: ...

def accepts_kwargs(func: Callable[..., Any]) -> bool: ...

SOCKET_ERROR: Type[ConnectionError]
MAXINT: None

def seekable(fileobj: Union[IO[Any], str, bytes]) -> bool: ...
def readable(fileobj: Union[IO[Any], str, bytes]) -> bool: ...
def fallocate(fileobj: Union[IO[Any], str, bytes], size: int) -> None: ...
