"""
Паттерн Строитель

Назначение: Позволяет создавать сложные объекты пошагово. Строитель даёт возможность использовать один и тот же код
строительства для получения разных представлений объектов.
"""


from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class Builder(ABC):
    @property
    @abstractmethod
    def product(self):
        pass

    @abstractmethod
    def add_cheese(self):
        pass

    @abstractmethod
    def add_mushrooms(self):
        pass

    @abstractmethod
    def add_pineapples(self):
        pass


class PizzaCreator(Builder):
    def __init__(self):
        self.reset()

    def reset(self):
        self._product = Pizza()

    @property
    def product(self) -> Pizza:
        product = self._product
        self.reset()
        return product

    def add_cheese(self):
        self._product.add('cheese')

    def add_mushrooms(self):
        self._product.add('mushrooms')

    def add_pineapples(self):
        self._product.add('pineapples')


class Pizza:
    def __init__(self):
        self.compound = ['dough', 'tomatoes', 'cucumbers', 'ketchup']

    def add(self, part: Any):
        self.compound.append(part)

    def form_order(self, first_name: str, last_name: str, address: str):
        order_info = {
            'name': f'{first_name} {last_name}',
            'address': address,
            'compound': self.compound,
        }
        return order_info


class Director:
    def __init__(self):
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder):
        self._builder = builder

    def build_full_featured_product(self, **ingredients):
        constituents = {
            'cheese': self.builder.add_cheese,
            'mushrooms': self.builder.add_mushrooms,
            'pineapples': self.builder.add_pineapples,
        }
        for name, availability in ingredients.items():
            if not availability:
                continue
            creator = constituents.get(name)
            if creator:
                creator()


if __name__ == '__main__':
    director = Director()
    builder = PizzaCreator()
    director.builder = builder
    director.build_full_featured_product(cheese=True, mushrooms=False, pineapples=False)
    order = builder.product.form_order(
        first_name='Svetlana',
        last_name='Sumets',
        address='Mr John Smith. 132, My Street, Kingston, New York',
    )
    print(order)
