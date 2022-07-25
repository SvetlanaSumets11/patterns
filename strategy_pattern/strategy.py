"""
Паттерн Стратегия

Назначение: Определяет семейство схожих алгоритмов и помещает каждый из них в собственный класс, после чего алгоритмы
можно взаимозаменять прямо во время исполнения программы.
"""


from __future__ import annotations

import json
from abc import ABC, abstractmethod
from uuid import UUID


class OperationManager:
    UUID_FIELDS = ('file_id', 'parent_dir_id', 'user_id')

    def __init__(self, operation: BaseOperation):
        self._operation = operation

    @property
    def operation(self) -> BaseOperation:
        return self._operation

    @operation.setter
    def operation(self, operation: BaseOperation):
        self._operation = operation

    @staticmethod
    def _is_valid_uuid(uuid_str: str, version=4) -> str:
        try:
            uuid_obj = UUID(uuid_str, version=version)
            assert str(uuid_obj) == uuid_str
        except (ValueError, AssertionError):
            raise ValueError(f'{uuid_str} is not a valid UUID')
        return uuid_str

    def perform_operation(self, payload: dict) -> str:
        if not payload:
            return 'Failed. Empty data passed'

        for field in self.UUID_FIELDS:
            id_value = payload.get(field)

            if id_value is None:
                continue
            if not id_value:
                return f'Failed. Parameter {field} is missed'
            if not self._is_valid_uuid(id_value):
                return f'Failed. {field} is invalid'

        result_msg = self.operation.perform(payload)
        return result_msg


class BaseOperation(ABC):
    @abstractmethod
    def perform(self, metadata: dict) -> str:
        pass

    @staticmethod
    def _update_file(parameters: dict) -> bool:
        try:
            with open('file.json', 'r') as file:
                file_data = json.loads(file.read())

            updated_file_data = file_data | parameters

            with open('file.json', 'w') as file:
                file.write(json.dumps(updated_file_data))
        except (FileNotFoundError, FileExistsError, KeyError):
            return False
        return True


class Move(BaseOperation):
    PARENT_DIR_ID_FIELD = 'parent_dir_id'

    def perform(self, metadata: dict) -> str:
        target_directory = {self.PARENT_DIR_ID_FIELD: metadata[self.PARENT_DIR_ID_FIELD]}
        moved = self._update_file(target_directory)
        if moved:
            return 'Success'
        return 'Failed. Error during file moving'


class Modify(BaseOperation):
    VALID_MODIFICATION_FIELDS = ('name', 'description')

    def perform(self, metadata: dict) -> str:
        invalid_fields = [key for key in metadata if key not in self.VALID_MODIFICATION_FIELDS]
        if invalid_fields:
            return f'Failed. You are trying to modify immutable fields {", ".join(invalid_fields)}'

        modified = self._update_file(metadata)
        if modified:
            return 'Success'
        return 'Failed. Error during file modification'


if __name__ == "__main__":
    operation_manager = OperationManager(Move())
    response = operation_manager.perform_operation({'parent_dir_id': '8ac91db9-4af8-4c82-b1a4-c64976601b83'})
    print(response)

    operation_manager = OperationManager(Modify())
    response = operation_manager.perform_operation({
        'description': 'Description',
        'name': 'Test name',
    })
    print(response)
