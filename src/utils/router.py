from typing import Protocol, runtime_checkable

from fastapi import APIRouter

# Define a custom protocol that requires a `router` attribute
@runtime_checkable
class RouterModule(Protocol):
    router: APIRouter