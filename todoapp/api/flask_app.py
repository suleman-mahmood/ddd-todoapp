from flask import Flask, request

from ..entrypoint import commands, unit_of_work

app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to my Todo List application!", 200


@app.route("/add-user", methods=["POST"])
def add_user():
    commands.add_user(
        request.json["id"],
        request.json["first_name"],
        request.json["last_name"],
        unit_of_work.UnitOfWork(),
    )
    return "OK", 201


@app.route("/add-task", methods=["POST"])
def add_task():
    commands.add_task(
        request.json["id"],
        request.json["description"],
        request.json["completed"],
        request.json["user_id"],
        unit_of_work.UnitOfWork(),
    )
    return "OK", 201


@app.route("/edit-task", methods=["POST"])
def edit_task():
    commands.edit_task(
        request.json["id"],
        request.json["description"],
        request.json["completed"],
        request.json["user_id"],
        unit_of_work.UnitOfWork(),
    )
    return "OK", 201


@app.route("/delete-task", methods=["DELETE"])
def delete_task():
    commands.delete_task(
        request.json["user_id"],
        request.json["task_id"],
        unit_of_work.UnitOfWork(),
    )
    return "OK", 201


@app.route("/change-order", methods=["POST"])
def change_order():
    commands.change_order(
        request.json["id"],
        request.json["order_list"],
        unit_of_work.UnitOfWork(),
    )
    return "OK", 201
