from core.compiler_phase import CompilerPhase
from typing import List


class SystemHook:
    def __init__(self, phase: CompilerPhase, callback):
        self.phase = phase
        self.callback = callback

class BlockHook:
    def __init__(self, phase: CompilerPhase, block_type: str, callback):
        self.phase = phase
        self.block_type = block_type
        self.callback = callback

class PluginRegistration:
    def __init__(self, name: str, system_hooks: List[SystemHook] = None, block_hooks: List[BlockHook] = None):
        self.name = name
        self.system_hooks: List[SystemHook] = [] if system_hooks is None else system_hooks
        self.block_hooks: List[BlockHook] = [] if block_hooks is None else block_hooks

    def add_system_hook(self, phase: CompilerPhase, callback):
        self.system_calls.append(SystemHook(phase, callback))

    def add_block_hook(self, phase: CompilerPhase, block_type: str, callback):
        self.block_hooks.append(BlockHook(phase, block_type, callback))



