from uuid import UUID, uuid4
from ..domain import model
from .unit_of_work import AbstractUnitOfWork


def add_user(id: str, first_name: str, last_name: str, uow: AbstractUnitOfWork):
    user = model.User(UUID(id), first_name, last_name)
    with uow:
        uow.users.add(user)


def add_task(
    task_id: str,
    task_description: str,
    completed: bool,
    user_id: str,
    uow: AbstractUnitOfWork,
):
    task = model.Task(UUID(task_id), task_description, completed)
    with uow:
        user = uow.users.get(UUID(user_id))
        user.add_task(task)
        uow.users.save(user)
        uow.histories.add(
            model.TaskHistory(uuid4(), "add", UUID(task_id), UUID(user_id))
        )


def edit_task(
    task_id: str,
    task_description: str,
    completed: bool,
    user_id: str,
    uow: AbstractUnitOfWork,
):
    task = model.Task(UUID(task_id), task_description, completed)
    with uow:
        user = uow.users.get(UUID(user_id))
        user.edit_task(task)
        uow.users.save(user)
        uow.histories.add(
            model.TaskHistory(uuid4(), "edit", UUID(task_id), UUID(user_id))
        )


def delete_task(
    user_id: str,
    task_id: str,
    uow: AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get(UUID(user_id))
        user.delete_task(UUID(task_id))
        uow.users.save(user)

        uow.histories.add(
            model.TaskHistory(uuid4(), "delete", UUID(task_id), UUID(user_id))
        )


def change_order(
    user_id: str,
    orderList: list,
    uow: AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get(UUID(user_id))
        orderListClass = [
            model.TaskOrder(UUID(o["id"]), o["new_loc"]) for o in orderList
        ]
        user.change_order(orderListClass)
        uow.users.save(user)
