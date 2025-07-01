from typing import List, Optional


class Assignment:
    def __init__(self, type, name, value):
        self.type = type
        self.name = name
        self.value = value

class Block:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.assignments: List[Assignment] = []
        self.children: List[Block] = []

    def add_assignment(self, assignment: Assignment):
        self.assignments.append(assignment)

    def add_child(self, child: 'Block'):
        self.children.append(child)

    def __str__(self):
        return f"Block(name={self.name}, type={self.type}, assignments={len(self.assignments)}, children={len(self.children)})"

    def has_child(self, child_name: str) -> bool:
        return any(child.name == child_name for child in self.children)

    def get_child(self, child_name: str) -> Optional['Block']:
        for child in self.children:
            if child.name == child_name:
                return child
        return None

    def has_assignment(self, assignment_name: str) -> bool:
        return any(assignment.name == assignment_name for assignment in self.assignments)

    def get_assignment(self, assignment_name: str) -> Optional[Assignment]:
        for assignment in self.assignments:
            if assignment.name == assignment_name:
                return assignment
        return None