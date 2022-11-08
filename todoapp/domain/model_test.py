from uuid import uuid4
from .model import User, Task, TaskOrder


def make_user_and_task():
    user = User(uuid4(), "suleman", "mahmood")
    task = Task(uuid4(), "do household chores", False)

    return user, task


# Add task to a user's own todo list
def test_add_task_to_users_list():
    user, task = make_user_and_task()
    user.add_task(task)

    assert user.task_list == {task.id: task}


# Delete task
def test_delete_task_in_users_list():
    user, task = make_user_and_task()
    user.add_task(task)
    assert user.task_list == {task.id: task}

    user.delete_task(task.id)
    assert user.task_list == {}


# Order tasks
def test_change_tasks_order():
    user, task = make_user_and_task()
    task2 = Task(uuid4(), "do office work", False)
    task3 = Task(uuid4(), "do laundry", False)

    user.add_task(task)
    user.add_task(task2)
    user.add_task(task3)

    # Check original list for order
    assert user.task_list[task.id].order == 0
    assert user.task_list[task2.id].order == 1
    assert user.task_list[task3.id].order == 2

    # Pass a list of task ids and their new order
    user.change_order([TaskOrder(task2.id, 0)])
    assert user.task_list[task.id].order == 1
    assert user.task_list[task2.id].order == 0
    assert user.task_list[task3.id].order == 2

    user.change_order([TaskOrder(task.id, 0)])
    assert user.task_list[task.id].order == 0
    assert user.task_list[task2.id].order == 1
    assert user.task_list[task3.id].order == 2

    user.change_order([TaskOrder(task3.id, 1), TaskOrder(task.id, 2)])
    assert user.task_list[task.id].order == 2
    assert user.task_list[task2.id].order == 1
    assert user.task_list[task3.id].order == 0
