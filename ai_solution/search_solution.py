import json
import numpy as np


COMMAND_LEFT = 'left'
COMMAND_RIGHT = 'right'
COMMAND_UP = 'up'
COMMAND_DOWN = 'down'


class SimpleSolution:
    """
    Первое решение.

    Основные атрибуты класса:
        x_cells_count - количество ячеек по X
        y_cells_count - количество ячеек по Y
        available_acts - список доступных команд
        target_point - целевая точка (куда мы идем)
        is_finish - флаг окончания игры

    Основные функции класса:
        game_loop() - основной цикл стратегии.
        do_step(cur_pos, best_path) - совершаем наш ход на основе 'cur_pos' - текущем положении.
            и 'best_path' - найденной траектории .
        search_path(matrix_env_state) - поиск найлучшей траектории до self.target_point.
        search_target(state) - поиск на игровом поле целевой точки.
        transform_state(state) - пекревод входных данных игры в матрицу для последующего поиска путя на ней.
        parse_state() - чтение данных на текущий шаг.
    """

    def __init__(self, *args, **kwargs):
        self.x_cells_count = 0
        self.y_cells_count = 0

        self.available_acts = [
            COMMAND_LEFT, COMMAND_RIGHT,
            COMMAND_UP, COMMAND_DOWN
        ]

        self.is_finish = False

        self.target_point = None

        super().__init__(*args, **kwargs)

    def game_loop(self):
        """
        Основной цикл алгоритма.
        """
        state = self.parse_state()

        if state.type == 'end_game':
            self.is_finish = True
            return

        if self.target_point is None:
            self.target_point = self.search_target(state)

        cur_pos = state['params']['i']['position']

        if cur_pos == self.target_point:
            self.target_point = self.search_target(state)

        matrix_env_state = self.transform_state(state)
        best_path = self.search_path(matrix_env_state)
        self.do_step(cur_pos, best_path)

    def do_step(self, cur_pos, best_path):
        """
        Выполнение хода.

        Args:
            cur_pos: текущее положение игрока.
            best_path: путь.
        """
        pass

    def search_path(self, matrix_env_state):
        """
        Поиск кратчайшего пути на матрице игрового состояния.

        Args:
            matrix_env_state: матрица игрового состояния

        Return:
            Найденный путь (последовательный список точек).
        """
        pass

    def search_target(self, state):
        """
        Поиск целевой точки.

        Args:
            state: состояние игры.

        Return:
            Целевая точка.
        """
        return state

    def transform_state(self, state):
        """
        Перевод состояния игры в матрицу состояния игры.

        Args:
            state: словарь состояния игры.

        Return:
             матрица состояния игры.
        """
        return state

    def parse_state(self):
        """
        Чтение данных на текущий шаг.
        """
        input_text = input()
        return json.loads(input_text)