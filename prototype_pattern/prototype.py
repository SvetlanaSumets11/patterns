import copy

"""
Прототип — это порождающий паттерн, который позволяет копировать объекты любой сложности без привязки 
к их конкретным классам.
"""


class SelfReferencingEntity:
    def __init__(self):
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent


class Schoolchild:
    def __init__(self, name: str, school_num: int, class_num: int, grades: list, circular_ref):
        self.name = name
        self.class_num = class_num
        self.school_num = school_num
        self.grades = grades
        self.circular_ref = circular_ref

    def __copy__(self):
        grades = copy.copy(self.grades)
        name = copy.copy(self.name)
        school_num = copy.copy(self.school_num)
        class_num = copy.copy(self.class_num)
        circular_ref = copy.copy(self.circular_ref)

        new = self.__class__(name, school_num, class_num, grades, circular_ref)
        new.__dict__.update(self.__dict__)

        return new

    def __deepcopy__(self, memo=None):
        if memo is None:
            memo = {}

        grades = copy.deepcopy(self.grades, memo)
        circular_ref = copy.deepcopy(self.circular_ref, memo)

        new = self.__class__(self.name, self.class_num, self.school_num, grades, circular_ref)
        new.__dict__ = copy.deepcopy(self.__dict__, memo)

        return new


if __name__ == "__main__":
    grades = [96, 91, [65, 76, 100, 91], [88, 79, 66]]
    circular_ref = SelfReferencingEntity()
    component = Schoolchild(
        name='Svetlana Sumets',
        school_num=142,
        class_num=5,
        grades=grades,
        circular_ref=circular_ref)
    circular_ref.set_parent(component)

    shallow_copied_component = copy.copy(component)

    shallow_copied_component.grades.append(100)
    if component.grades[-1] == 100:
        print('Adding elements to shallow_copied_component`s, grades adds it to component`s grades.')
    else:
        print('Adding elements to shallow_copied_component`s, grades doesn`t add it to component`s grades')

    component.grades[2].append(60)
    if 60 in shallow_copied_component.grades[2]:
        print('Changing obj in the component`s grades changes that obj in shallow_copied_component`s grades.')
    else:
        print('Changing obj in the component`s grades doesn`t change that obj in shallow_copied_component`s grades.')

    deep_copied_component = copy.deepcopy(component)

    deep_copied_component.grades.append(100)
    if component.grades[-1] == 100:
        print('Adding elements to deep_copied_component`s grades adds it to component`s grades.')
    else:
        print('Adding elements to deep_copied_component`s grades doesn`t add it to component`s grades.')

    component.grades[2].append(60)
    if 60 in deep_copied_component.grades[2]:
        print('Changing obj in the component`s grades changes that obj in deep_copied_component`s grades.')
    else:
        print('Changing obj in the component`s grades doesn`t change that obj in deep_copied_component`s grades.')

    print(id(deep_copied_component.circular_ref.parent))
    print(id(deep_copied_component.circular_ref.parent.circular_ref.parent))
