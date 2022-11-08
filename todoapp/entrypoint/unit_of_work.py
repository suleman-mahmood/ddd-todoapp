import psycopg2

from abc import ABC, abstractmethod
from ..adapters.repository import (
    UserRepository,
    HistoryRepository,
    FakeUserRepository,
    FakeHistoryRepository,
)


class AbstractUnitOfWork(ABC):
    users: UserRepository
    histories: HistoryRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args):
        self.commit()
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        super().__init__()
        self.users = FakeUserRepository()
        self.histories = FakeHistoryRepository()

    def commit(self):
        pass

    def rollback(self):
        pass


class UnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        self.connection = psycopg2.connect("dbname=todolist")
        # self.connection = psycopg2.connect(
        #     user="suleman",
        #     password="admin",
        #     host="/cloudsql/hum-retail-dev:us-central1:onboarding",
        #     database="suleman",
        # )
        self.cursor = self.connection.cursor()

        self.users = UserRepository(self.connection)
        self.histories = HistoryRepository(self.connection)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
