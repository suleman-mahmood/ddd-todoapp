from abc import ABC, abstractmethod
from typing import List, Dict, Set
from uuid import UUID

from ..domain.model import User, Task, TaskHistory


class HistoryAbstractRepository(ABC):
    @abstractmethod
    def add(self, history: TaskHistory):
        pass

    @abstractmethod
    def get(self, history_id: UUID) -> TaskHistory:
        pass

    @abstractmethod
    def get_user_history(self, user_id: UUID) -> Set[TaskHistory]:
        pass


class FakeHistoryRepository(HistoryAbstractRepository):
    def __init__(self):
        self.history: Dict[UUID, Set[TaskHistory]] = {}

    def add(self, history):
        if history.user_id not in self.history:
            self.history[history.user_id] = set()

        self.history[history.user_id].add(history)

    def get(self, history_id):
        for history in self.history.values():
            for hist in history:
                if hist.id == history_id:
                    return hist

    def get_user_history(self, user_id):
        return self.history[user_id]


class HistoryRepository(HistoryAbstractRepository):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add(self, history):
        sql = """
            insert into histories (history_id, action_taken, task_id)
            values (%s, %s, %s) 
        """
        self.cursor.execute(
            sql, [str(history.id), history.action, str(history.task_id)]
        )

    def get(self, history_id):
        sql = """
            select history_id, action_taken, task_id 
            from histories
            where history_id = %s
        """
        self.cursor.execute(sql, [str(history_id)])
        row = self.cursor.fetchone()

        sql = """
            select user_id
            from tasks
            where task_id = %s
        """
        self.cursor.execute(sql, [row[2]])
        row2 = self.cursor.fetchone()

        return TaskHistory(UUID(row[0]), row[1], UUID(row[2]), UUID(row2[0]))

    def get_user_history(self, user_id):
        history = set()

        sql = """
            select history_id, action_taken, task_id
            from histories
            where task_id in (
                select task_id from tasks where user_id = %s
            )
        """
        self.cursor.execute(sql, [str(user_id)])
        rows = self.cursor.fetchall()

        for row in rows:
            history.add(TaskHistory(UUID(row[0]), row[1], UUID(row[2]), user_id))

        return history


class UserAbstractRepository(ABC):
    @abstractmethod
    def add(self, user: User):
        pass

    @abstractmethod
    def get(self, user_id: UUID) -> User:
        pass

    @abstractmethod
    def save(self, user: User):
        pass


class FakeUserRepository(UserAbstractRepository):
    def __init__(self):
        self.users: Dict[UUID, User] = {}

    def add(self, user):
        self.users[user.id] = user

    def get(self, user_id):
        return self.users[user_id]

    def save(self, user):
        self.users[user.id] = user


class UserRepository(UserAbstractRepository):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add(self, user):
        sql = """
            insert into users(user_id, first_name, last_name)
            values (%s, %s, %s)
        """
        self.cursor.execute(sql, [str(user.id), user.first_name, user.last_name])

        for task in user.task_list.values():
            sql = """
                insert into tasks(task_id, task_description, is_completed, task_order, is_deleted, user_id)
                values (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(
                sql,
                [
                    str(task.id),
                    task.description,
                    task.completed,
                    task.order,
                    False,
                    str(user.id),
                ],
            )

    def get(self, user_id):
        sql = """
            SELECT user_id, first_name, last_name
            FROM users
            WHERE user_id = %s
        """
        self.cursor.execute(sql, [str(user_id)])
        row = self.cursor.fetchone()

        user = User(UUID(row[0]), row[1], row[2])

        sql = """
            SELECT task_id, task_description, is_completed, task_order
            FROM tasks
            WHERE user_id = %s AND is_deleted = %s
        """
        self.cursor.execute(sql, [str(user_id), False])
        rows = self.cursor.fetchall()

        tasks = {}
        for row in rows:
            tasks[UUID(row[0])] = Task(UUID(row[0]), row[1], row[2], row[3])

        user.task_list = tasks
        return user

    def save(self, user):
        # Mark all tasks as deleted
        sql = """
            update tasks
            set is_deleted = %s
            where user_id = %s
        """
        self.cursor.execute(sql, [True, str(user.id)])

        for task in user.task_list.values():
            sql = """
                update tasks
                set task_id = %s, task_description = %s, is_completed = %s, task_order = %s, is_deleted = %s, user_id = %s
                where task_id = %s
            """
            self.cursor.execute(
                sql,
                [
                    str(task.id),
                    task.description,
                    task.completed,
                    task.order,
                    True,
                    str(user.id),
                    str(task.id),
                ],
            )
