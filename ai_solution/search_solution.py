import json
import numpy as np


COMMAND_LEFT = 'left'
COMMAND_RIGHT = 'right'
COMMAND_UP = 'up'
COMMAND_DOWN = 'down'

M_I_POS_VALUE = 1
M_I_TERRITORY_VALUE = 1
M_I_LINE_VALUE = 1

M_PL_POS_VALUE = 1
M_PL_TERRITORY_VALUE = 1
M_PL_LINE_VALUE = 1


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
        self.command_acts = {
            [-1,  0]: COMMAND_LEFT,
            [ 1,  0]: COMMAND_RIGHT,
            [ 0, -1]: COMMAND_DOWN,
            [ 0,  1]: COMMAND_UP
        }

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
        best_path = self.search_path(matrix_env_state, cur_pos, self.target_point)
        self.do_step(cur_pos, best_path)

    def do_step(self, cur_pos, best_path):
        """
        Выполнение хода.

        Args:
            cur_pos: текущее положение игрока.
            best_path: путь.
        """
        cmd = ''

        cur_pos_index = -1
        for i in range(len(best_path)):
            if best_path[i] == cur_pos:
                cur_pos_index = i
                break

        next_pos = best_path[cur_pos_index + 1]

        next_move_act = []
        next_move_act[0] = next_pos[0] - cur_pos[0]
        next_move_act[1] = next_pos[1] - cur_pos[1]

        cmd = self.command_acts[next_move_act] 

        print(cmd)

    def search_path(self, matrix_env_state, cur_pos, target_pos):
        """
        Поиск кратчайшего пути на матрице игрового состояния.

        Args:
            matrix_env_state: матрица игрового состояния.
                Матрица имеет вид 2D numpy матрицы размеры которой
                x_cells_count на y_cells_count.
            cur_pos: текущее положение, имеет вид: [x y] - список из двух элементов.
            target_pos: целевое положение, имеет вид: [x y] - список из двух элементов.

        Return:
            Найденный путь (последовательный список точек от нашего положения до целевого положения).
            Пример пути:
            [[1 1] [2 1] [3 2]]
        """
        return cur_pos

    def search_target(self, state):
        """
        Поиск целевой точки.

        Args:
            state: состояние игры.

        Return:
            Целевая точка.
        """
        boarders = state['params']['i']['territory']

        choosen_point = np.random.choice(boarders)
        return choosen_point

    def transform_state(self, state):
        """
        Перевод состояния игры в матрицу состояния игры.

        Args:
            state: словарь состояния игры.

        Return:
             матрица состояния игры.
             np.matrix[width x height]
        """
        def fill_matrix(
                matrix,
                player_state,
                position_value,
                territory_value,
                line_value
        ):
            player_pos = player_state['position']
            x, y = player_pos[0], player_pos[1]
            matrix[x, y] = position_value

            for territory_pos in player_state['territory']:
                t_x = territory_pos[0]
                t_y = territory_pos[1]
                matrix[t_x, t_y] = territory_value

            for line_pos in player_state['lines']:
                l_x = line_pos[0]
                l_y = line_pos[1]
                matrix[l_x, l_y] = line_value

            return matrix

        new_state = np.zeros((self.x_cells_count, self.y_cells_count))
        players = state['params']['players']

        for player in players:
            if player == 'i':
                new_state = fill_matrix(
                    new_state,
                    players[player],
                    M_I_POS_VALUE,
                    M_I_TERRITORY_VALUE,
                    M_I_LINE_VALUE
                )
            else:
                new_state = fill_matrix(
                    new_state,
                    players[player],
                    M_PL_POS_VALUE,
                    M_PL_TERRITORY_VALUE,
                    M_PL_LINE_VALUE
                )
        return state

    def parse_state(self):
        """
        Чтение данных на текущий шаг.
        """
        input_text = input()
        return json.loads(input_text)
