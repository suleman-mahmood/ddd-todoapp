from uuid import uuid4
from .unit_of_work import FakeUnitOfWork
from . import commands
from ..domain import model


def make_user():
    return model.User(uuid4(), "Suleman", "Mahmod")


def make_task():
    return model.Task(uuid4(), "do household chores", False)


def test_add_users():
    uow = FakeUnitOfWork()

    user1, user2 = make_user(), make_user()

    commands.add_user(str(user1.id), user1.first_name, user1.last_name, uow)
    commands.add_user(str(user2.id), user2.first_name, user2.last_name, uow)

    fetched_user1 = uow.users.get(user1.id)
    fetched_user2 = uow.users.get(user2.id)

    assert fetched_user1.id == user1.id
    assert fetched_user1.first_name == user1.first_name
    assert fetched_user1.last_name == user1.last_name

    assert fetched_user2.id == user2.id
    assert fetched_user2.first_name == user2.first_name
    assert fetched_user2.last_name == user2.last_name


def test_add_tasks():
    uow = FakeUnitOfWork()

    user = make_user()
    commands.add_user(str(user.id), user.first_name, user.last_name, uow)

    task1 = make_task()
    commands.add_task(
        str(task1.id), task1.description, task1.completed, str(user.id), uow
    )

    task2 = make_task()
    commands.add_task(
        str(task2.id), task2.description, task2.completed, str(user.id), uow
    )

    fetched_user = uow.users.get(user.id)
    task1.order = 0
    task2.order = 1

    assert fetched_user.task_list == {
        task1.id: task1,
        task2.id: task2,
    }


def test_edit_tasks():
    uow = FakeUnitOfWork()

    user = make_user()
    commands.add_user(str(user.id), user.first_name, user.last_name, uow)

    task1 = make_task()
    commands.add_task(
        str(task1.id), task1.description, task1.completed, str(user.id), uow
    )

    task2 = make_task()
    commands.add_task(
        str(task2.id), task2.description, task2.completed, str(user.id), uow
    )

    task2.description = "Do nothing"
    task2.completed = True
    commands.edit_task(
        str(task2.id), task2.description, task2.completed, str(user.id), uow
    )

    fetched_user = uow.users.get(user.id)
    task1.order = 0
    task2.order = 1

    assert fetched_user.task_list == {
        task1.id: task1,
        task2.id: task2,
    }


def test_delete_task():
    uow = FakeUnitOfWork()

    user = make_user()
    commands.add_user(str(user.id), user.first_name, user.last_name, uow)

    task1 = make_task()
    commands.add_task(
        str(task1.id), task1.description, task1.completed, str(user.id), uow
    )

    task2 = make_task()
    commands.add_task(
        str(task2.id), task2.description, task2.completed, str(user.id), uow
    )

    fetched_user = uow.users.get(user.id)
    task1.order = 0
    task2.order = 1

    assert fetched_user.task_list == {
        task1.id: task1,
        task2.id: task2,
    }

    # Now check for deletion
    commands.delete_task(str(user.id), str(task1.id), uow)
    task2.order = 0

    assert fetched_user.task_list == {task2.id: task2}


def test_change_order():
    # Create a user and two tasks to it
    uow = FakeUnitOfWork()

    user = make_user()
    commands.add_user(str(user.id), user.first_name, user.last_name, uow)

    task1 = make_task()
    commands.add_task(
        str(task1.id), task1.description, task1.completed, str(user.id), uow
    )

    task2 = make_task()
    commands.add_task(
        str(task2.id), task2.description, task2.completed, str(user.id), uow
    )

    fetched_user = uow.users.get(user.id)
    task1.order = 0
    task2.order = 1

    assert fetched_user.task_list == {
        task1.id: task1,
        task2.id: task2,
    }

    # Now check for order change
    commands.change_order(str(user.id), [{"id": str(task2.id), "new_loc": 0}], uow)
    task1.order = 1
    task2.order = 0

    assert fetched_user.task_list == {
        task1.id: task1,
        task2.id: task2,
    }
