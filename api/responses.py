from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class BaseResponse:
    success: bool
    message: Optional[str] = None


@dataclass
class UserCreationResponse(BaseResponse):
    accessToken: Optional[str] = None
    refreshToken: Optional[str] = None
    user: Optional[Dict[str, Any]] = None


@dataclass
class LoginResponse(BaseResponse):
    accessToken: Optional[str] = None
    refreshToken: Optional[str] = None
    user: Optional[Dict[str, Any]] = None


@dataclass
class OrderCreationResponse(BaseResponse):
    name: Optional[str] = None
    order: Optional[Dict[str, Any]] = None
