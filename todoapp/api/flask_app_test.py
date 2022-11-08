from uuid import uuid4
import requests

url = "http://127.0.0.1:5000"
# url = "https://suleman-dot-hum-retail-dev.uc.r.appspot.com"


def test_add_user():
    data = {"id": str(uuid4()), "first_name": "Sami", "last_name": "Mahmood"}
    r = requests.post(f"{url}/add-user", json=data)

    assert r.status_code == 201


def test_add_task():
    # Add User
    user_id = str(uuid4())
    data = {"id": user_id, "first_name": "Sami", "last_name": "Mahmood"}
    r = requests.post(f"{url}/add-user", json=data)

    # Add Task
    data = {
        "id": str(uuid4()),
        "description": "do work",
        "completed": False,
        "user_id": user_id,
    }
    r = requests.post(f"{url}/add-task", json=data)

    assert r.status_code == 201


def test_edit_task():
    # Add User
    user_id = str(uuid4())
    data = {"id": user_id, "first_name": "Sami", "last_name": "Mahmood"}
    r = requests.post(f"{url}/add-user", json=data)

    # Add Task
    task_uuid = str(uuid4())
    data = {
        "id": task_uuid,
        "description": "do work",
        "completed": False,
        "user_id": user_id,
    }
    r = requests.post(f"{url}/add-task", json=data)

    assert r.status_code == 201

    # Edit Task
    data = {
        "id": task_uuid,
        "description": "do nothing",
        "completed": True,
        "user_id": user_id,
    }
    r = requests.post(f"{url}/edit-task", json=data)

    assert r.status_code == 201


def test_delete_task():
    # Add User
    user_id = str(uuid4())
    data = {"id": user_id, "first_name": "Sami", "last_name": "Mahmood"}
    r = requests.post(f"{url}/add-user", json=data)

    # Add Task
    task_id = str(uuid4())
    data = {
        "id": task_id,
        "description": "do work",
        "completed": False,
        "user_id": user_id,
    }
    r = requests.post(f"{url}/add-task", json=data)

    # Delete Task
    data = {"user_id": user_id, "task_id": task_id}
    r = requests.delete(f"{url}/delete-task", json=data)

    assert r.status_code == 201


def test_change_order():

    # Add User
    user_id = str(uuid4())
    data = {"id": user_id, "first_name": "Sami", "last_name": "Mahmood"}
    r = requests.post(f"{url}/add-user", json=data)

    # Add Task
    task_id_one = str(uuid4())
    data = {
        "id": task_id_one,
        "description": "do work",
        "completed": False,
        "user_id": user_id,
    }
    r = requests.post(f"{url}/add-task", json=data)

    # Add Task
    task_id_two = str(uuid4())
    data = {
        "id": task_id_two,
        "description": "do another work",
        "completed": False,
        "user_id": user_id,
    }
    r = requests.post(f"{url}/add-task", json=data)

    data = {"id": user_id, "order_list": [{"id": task_id_two, "new_loc": 0}]}
    r = requests.post(f"{url}/change-order", json=data)

    assert r.status_code == 201
