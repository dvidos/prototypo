from typing import List, Optional, Dict


class Assignment:
    def __init__(self, type: Optional[str], name: Optional[str], value: Optional[str]):
        self.type: Optional[str] = type
        self.name: Optional[str] = name
        self.value: Optional[str] = value

    def __str__(self):
        return f"Assignment(type={self.type}, name={self.name}, value={self.value})"


class Block:
    def __init__(self, name: Optional[str], type: Optional[str]):
        self.name: Optional[str] = name
        self.type: Optional[str] = type
        self._assignments: List[Assignment] = []
        self._children: List[Block] = []
        self._assignments_per_name: Dict[str, Assignment] = {}
        self._children_per_name: Dict[str, 'Block'] = {}

    def __str__(self):
        return f"Block(name={self.name}, type={self.type}, assignments={len(self._assignments)}, children={len(self._children)})"

    def has_child(self, child_name: str) -> bool:
        return child_name in self._children_per_name

    def get_child(self, child_name: str) -> Optional['Block']:
        return self._children_per_name.get(child_name)

    def add_child(self, child: 'Block'):
        self._children.append(child)
        self._children_per_name[child.name] = child

    def get_children(self) -> List['Block']:
        return self._children

    def has_assignment(self, assignment_name: str) -> bool:
        return assignment_name in self._assignments_per_name

    def get_assignment(self, assignment_name: str) -> Optional[Assignment]:
        return self._assignments_per_name.get(assignment_name)

    def add_assignment(self, assignment: Assignment):
        self._assignments.append(assignment)
        self._assignments_per_name[assignment.name] = assignment

    def get_assignment_value(self, assignment_name: str, default_value: str) -> str:
        assignment = self.get_assignment(assignment_name)
        return assignment.value if assignment else default_value
