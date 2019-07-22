from copy import deepcopy


class QModel():
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def predict(self, state):
        """
        Функция, возвращающая численный вектор, описывающий оценку действий в текущем состоянии.
        """
        pass

    def clone(self):
        return deepcopy(self)

    def train(self, memory):
        """
        Тренировка НС.
        """
        pass