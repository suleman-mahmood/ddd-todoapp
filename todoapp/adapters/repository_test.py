from ..domain.model import User, Task, TaskHistory
from .repository import FakeUserRepository, FakeHistoryRepository
from uuid import uuid4


"""
Test cases using fake repository
"""


def get_user_task_task2():
    task = Task(uuid4(), "do household chores", False)
    task2 = Task(uuid4(), "do office work", False)
    user = User(uuid4(), "suleman", "mahmood", {task.id: task, task2.id: task2})

    return user, task, task2


def test_fake_user_repository_can_add_a_user():
    user, task, task2 = get_user_task_task2()

    repo = FakeUserRepository()
    repo.add(user)

    assert repo.users[user.id].id == user.id
    assert repo.users[user.id].first_name == user.first_name
    assert repo.users[user.id].last_name == user.last_name
    assert repo.users[user.id].task_list == {task.id: task, task2.id: task2}


def test_fake_user_repository_can_get_a_user():
    user, task, task2 = get_user_task_task2()

    repo = FakeUserRepository()
    repo.add(user)

    fetched_user = repo.get(user.id)

    assert fetched_user.id == user.id
    assert fetched_user.first_name == user.first_name
    assert fetched_user.last_name == user.last_name
    assert fetched_user.task_list == {task.id: task, task2.id: task2}


# def test_fake_user_repository_can_delete_task():
#     user, task, task2 = get_user_task_task2()

#     repo = FakeUserRepository()
#     repo.add(user)
#     repo.delete_user_task(task.id)

#     fetched_user = repo.get(user.id)

#     assert fetched_user.id == user.id
#     assert fetched_user.first_name == user.first_name
#     assert fetched_user.last_name == user.last_name
#     assert fetched_user.task_list == {task2.id: task2}


def test_fake_history_repository_can_add_history():
    user, task, task2 = get_user_task_task2()

    repo = FakeHistoryRepository()
    hist = TaskHistory(uuid4(), "add", task.id, user.id)
    repo.add(hist)
    hist2 = TaskHistory(uuid4(), "add", task2.id, user.id)
    repo.add(hist2)

    assert repo.history[user.id] == {hist, hist2}


def test_fake_history_repository_can_get_history():
    user, task, task2 = get_user_task_task2()

    repo = FakeHistoryRepository()
    hist = TaskHistory(uuid4(), "add", task.id, user.id)
    repo.add(hist)
    hist2 = TaskHistory(uuid4(), "add", task2.id, user.id)
    repo.add(hist2)

    fetched_history = repo.get(hist.id)
    fetched_history2 = repo.get(hist2.id)

    assert fetched_history == hist
    assert fetched_history2 == hist2


def test_fake_history_repository_can_get_user_history():
    user, task, task2 = get_user_task_task2()

    repo = FakeHistoryRepository()
    hist = TaskHistory(uuid4(), "add", task.id, user.id)
    repo.add(hist)
    hist2 = TaskHistory(uuid4(), "add", task2.id, user.id)
    repo.add(hist2)

    fetched_history = repo.get_user_history(user.id)

    assert fetched_history == set([hist, hist2])
