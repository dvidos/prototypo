from enum import Enum, auto

class CompilerPhase(Enum):
    SYS_INIT = auto()
    VALIDATE = auto()
    TRANSFORM = auto()
    GENERATE = auto()
    SYS_FINALIZE = auto()
