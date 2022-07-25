"""
Паттерн Фабричный Метод

Назначение: Определяет общий интерфейс для создания объектов в суперклассе,
позволяя подклассам изменять тип создаваемых объектов.
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from random import uniform


class ParticipantCreator(ABC):
    def __init__(self, first_name: str, last_name: str, age: int, ratings: list):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.ratings = ratings

    @abstractmethod
    def register_participant(self):
        pass

    def calculate_score(self) -> str:
        participant = self.register_participant()
        final_score = participant.get_final_score(self.ratings)
        return final_score / 100


class StudentCreator(ParticipantCreator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def register_participant(self) -> Participant:
        test_grade = uniform(0, 10)
        return Student(test_grade)


class SchoolkidCreator(ParticipantCreator):
    grading_system = 12

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def register_participant(self) -> Participant:
        test_grade = uniform(0, 10)
        return Schoolkid(test_grade)


class Participant(ABC):
    def __init__(self, test_grade: float):
        self.test_grade = test_grade

    @property
    @abstractmethod
    def grading_system(self):
        pass

    @abstractmethod
    def get_final_score(self, rating: list) -> str:
        pass


class Student(Participant):
    grading_system = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_final_score(self, rating: list) -> float:
        return sum(rating) / self.grading_system + self.test_grade


class Schoolkid(Participant):
    grading_system = 12

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_final_score(self, rating: list) -> str:
        return sum(rating) / self.grading_system + self.test_grade / self.grading_system


def client_code(creator: ParticipantCreator) -> None:
    print(f'The final rating of the participant is {creator.calculate_score()} points')


if __name__ == '__main__':
    client_code(StudentCreator(first_name='Svetlana', last_name='Sumets', age=21, ratings=[96, 90, 61, 75, 80]))
    client_code(SchoolkidCreator(first_name='Rita', last_name='Ovsanyk', age=16, ratings=[8, 7, 12, 10, 9]))
