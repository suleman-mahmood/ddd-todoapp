from dataclasses import dataclass, field
from typing import Dict, List
from uuid import UUID

"""
Use Cases / Requirements:
- Multiple users
- Users can access their own todo lists
- Users can add tasks to their todo list
- Users can marks tasks as completed
- Users can edit a task
- Users can delete a task
- Users can reorder their tasks
- Users can view the history of their todo list for any given day

Behaviors - Use cases that changes the data:
- Add a new user
- Add a new task to a specific user's todo list
- Edit task
    - Mark task as completed
    - Change task description
- Delete task
- Order tasks

Invariants:
- A single unique task can only be added to a single user (Tasks are not shared)
- Two different tasks of the same user cannot have the same order_id

Entities:
- User
- Task

Value Objects:
- TaskHistory
- TaskOrder

Aggregates:
- User
- TaskHistory
"""

# -1 order means it is un-assigned upon initialization
@dataclass
class Task:
    id: UUID
    description: str
    completed: bool
    order: int = -1


@dataclass(frozen=True)
class TaskHistory:
    id: UUID
    action: str
    task_id: UUID
    user_id: UUID


@dataclass(frozen=True)
class TaskOrder:
    id: UUID
    new_loc: int


@dataclass
class User:
    id: UUID
    first_name: str
    last_name: str
    task_list: Dict[UUID, Task] = field(default_factory=dict)

    def add_task(self, task: Task):
        task.order = self._highest_order + 1
        self.task_list[task.id] = task

    def edit_task(self, task: Task):
        task.order = self.task_list[task.id].order
        self.task_list[task.id] = task

    def delete_task(self, task_id: UUID):
        # Pull the next items in the list up by one
        for (key, value) in self.task_list.items():
            if value.order > self.task_list[task_id].order:
                self.task_list[key].order -= 1

        self.task_list.pop(task_id)

    def change_order(self, order_list: List[TaskOrder]):
        for new_order in order_list:
            old_order = self.task_list[new_order.id].order

            # Push the next items in the list down by one
            for (key, value) in self.task_list.items():
                if value.order > old_order:
                    self.task_list[key].order -= 1

            # Push the next items in the list down by one
            for (key, value) in self.task_list.items():
                if value.order >= new_order.new_loc:
                    self.task_list[key].order += 1

            self.task_list[new_order.id].order = new_order.new_loc

    @property
    def _highest_order(self):
        return (
            max(self.task_list.values(), key=lambda task: task.order).order
            if self.task_list
            else -1
        )
