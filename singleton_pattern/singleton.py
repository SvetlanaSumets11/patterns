"""
Паттерн Одиночка

Назначение: Гарантирует, что у класса есть только один экземпляр, и предоставляет к нему глобальную точку доступа.
У каждого наследника класса тоже будет по одному экземпляру.
"""

import logging
import sqlite3

from environs import Env

env = Env()
env.read_env('.env')
URL = SQLALCHEMY_DATABASE_URI = env('DATABASE_URI')


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):

    def __init__(self, url: str):
        self.connection = self.create_connection(url)

    @staticmethod
    def create_connection(url: str) -> sqlite3.Connection:
        connection = None
        try:
            connection = sqlite3.connect(database=url)
        except sqlite3.Error as e:
            logging.error(f'Error connecting to database: {e}')
        return connection

    def select_all_peers(self) -> list:
        cursor = self.connection.cursor()
        cursor.execute('SELECT type, last_update_on FROM peers')
        rows = cursor.fetchall()
        return rows


if __name__ == '__main__':
    singleton_1 = Singleton(url=URL)
    singleton_2 = Singleton(url=URL)

    if id(singleton_1) == id(singleton_2):
        print('Singleton works, both variables contain the same instance.')
    else:
        print('Singleton failed, variables contain different instances.')

    print(singleton_1.select_all_peers())
    print(singleton_2.select_all_peers())
