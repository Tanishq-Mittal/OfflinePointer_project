from typing import Literal
from pydantic import BaseModel, Field

class Control(BaseModel):
    id: str
    name: str
    role: str = "unknown"
    x: float
    y: float
    w: float = 1
    h: float = 1
    enabled: bool = True

class PickerOutput(BaseModel):
    control_id: str | None = None
    confidence: float = Field(ge=0, le=1)
    reason: str = ""

class Result(BaseModel):
    status: Literal["ok", "low_confidence", "not_found"]
    control_id: str | None = None
    confidence: float = 0
    candidates: list[str] = []
    model_used: str = ""
    latency_ms: float = 0
    tokens_per_sec: float = 0
    reason: str = ""
