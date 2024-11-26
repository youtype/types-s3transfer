"""
Test file for stubs.

Copyright 2024 Vlad Emelianov
"""

from s3transfer.futures import TransferCoordinator
from s3transfer.upload import InterruptReader

reader = InterruptReader(fileobj="str", transfer_coordinator=TransferCoordinator())
reader.read(None)
reader.read("None")
