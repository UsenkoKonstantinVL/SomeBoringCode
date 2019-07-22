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
        is_finish - флаг окончания игры

    Основные функции класса:
        game_loop() - основной цикл стратегии
        parse_state() - ожидание прихода сообщения о новом тике игры
        wait_for_start() - ожидание старта игры, чтение параметров игры
        choose_cmd(cmd2score_dict) - выбор команды на основе словаря с оценками команд
        find_best_way(point, state, act) - нахождение лучшего маршрута до точки point
        get_points_of_interests(state) - возвращение массива интересующих нас точек
        is_finish() - возвращает флаг окончания игры
    """
    def __init__(self, *args, **kwargs):
        self.x_cells_count = 0
        self.y_cells_count = 0

        self.available_acts = [
            COMMAND_LEFT, COMMAND_RIGHT, 
            COMMAND_UP, COMMAND_DOWN
        ]

        self.is_finish = False

        super().__init__(*args, **kwargs)


    def game_loop(self):
        """
        Основной цикл алгоритма.
        """
        state = self.parse_state()

        if state.type == 'end_game':
            self.is_finish = True
            return

        act2score = {
            COMMAND_DOWN: 0,
            COMMAND_UP: 0,
            COMMAND_LEFT: 0,
            COMMAND_RIGHT: 0
        }

        points_of_interests = self.get_points_of_interests(state)

        for act in available_acts:
		# Находим пути он нашего местоположения до точек интереса
		# Выбираем из путей самый лучший, возвращаем его оценку
            best_score = 0
            for point in points_of_interests:
                score = self.find_best_way(point, state, act)
                if score > best_score:
                    best_score = score
                act2score[act] = best_score
            
        chosen_cmd = self.choose_act(act2score)  # случайный выбор действия
        print(json.dumps({"command": chosen_cmd, 'debug': chosen_cmd}))

    def parse_state(self):
        """
        Чтение данных о текущем тике.
        """
        input_text = input()
        return json.loads(input_text)

    def wait_for_start(self):
        """
        Ожидание начала игры, парсинг параметров игры.
        """
        input_text = input()
        input_dict = json.loads(input_text)
        self.x_cells_count = input_dict['x_cells_count']
        self.y_cells_count = input_dict['y_cells_count']

    def choose_cmd(self, cmd2score_dict):
        """
        Выбор команды на основе словаря с оценкой команд.
        """
        sum_score = sum(cmd2score_dict.values())

        action_list = []
        prob_list = []
        for cmd, score in cmd2score_dict.items():
            action_list.append(cmd)
            prob_list.append(score / sum_score)

        cmd = np.random.choice(action_list, p=prob_list)
        return cmd

    def get_points_of_interests(self, state):
        """
        Возвращает список интересующих нас точек.

        Args:
            state: состояние игры.
        """
        return [1]

    def find_best_way(self, point, state, act):
        """
        Нахождение лучшего маршрута до точки point с учетом предположительного действия act.
        Args: 
            point: целевая точка. 
            state: состояние игры.
            act: предположительное действие.
        """
        return 1

    def is_finish(self):
        """
        Возвращает флаг окончания игры.
        """
        return self.is_finish