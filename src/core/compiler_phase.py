from enum import Enum, auto

class CompilerPhase(Enum):
    SYS_INIT = auto()           # prepare entries in context
    TYPE_COLLECTION = auto()
    VALIDATE = auto()
    TRANSFORM = auto()
    POPULATE = auto()           # using blocks, populate context
    SYS_GENERATE_OUT = auto()   # using context, generate output files
    SYS_FINALIZE = auto()
