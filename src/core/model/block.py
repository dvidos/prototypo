from typing import List


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
