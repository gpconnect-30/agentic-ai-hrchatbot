from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class ExecutionResult:
    status: str = "SUCCESS"
    action: Optional[str] = None
    source: Optional[str] = None
    data: Any = None
    error: Optional[str] = None
    checker: Optional[Dict[str, Any]] = None