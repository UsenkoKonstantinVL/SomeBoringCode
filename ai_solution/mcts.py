"""
Структура данных (MCTSNode):

Ход игры представлен в виде дерева, где каждая вершина
отображает отдельное состояние игры. Ребра дерева соответствуют
переходам из одного состояния в другое (т.е. ходам в игре).

У каждого состояние есть одна родительская вершина, за исключением
корневой вершины - стартового состояния игры, когда еще не было
совершено ходов.

Также у каждого состояния есть дочерние вершины, представляющие
возможные состояния игры на следующим шаге после текущего.
Дочерних вершин может не быть если, например, в текущем состоянии
игра завершена, или игроки не могут совершить ходов не нарушающих
правил игры.

------------------------------------------------------------

Алгоритм (MCTSAgent):

Позже опишу

"""

import numpy as np
from math import random

POINTS_FOR_WINNING = 1

class MCTSnode(object):
	def __init__(self, game_state, parent=None, move):
		"""
		Структура данных для представления
		Monte Carlo Search Tree.

		game_state {PyObj} - объект состояния игры, которое
		представляет данное дерево.

		parent {MCTSnode} - родительская MCTSnode, которая
		привела к текущей. Будет выставлена в None если является
		корневой вершиной.

		move {str} - название действия, которое привело к
		данному состоянию.

		unviseted_moves {list} - список доступный действий из
		данного состояния, которые еще не были использованы.

		children {list} - список всех дочерних узлов в данном
		дереве.

		players2wins {dict} - карта пар идентификаторов игроков и
		количества их побед.
 		"""
		self.game_state = game_state
		self.parent = parent
		self.move = move
		self.unviseted_moves = []
		self.children = []
		self.players2wins = {}
		self.num_rollouts = 0

	def add_random_child(self):
		"""
		Рандомно выбирает одно из допустимых
		действий и формирует из него новую
		дочернюю вершину.

		"""
		index = random.randint(0, len(self.unviseted_moves) - 1)
		new_move = self.unviseted_moves.pop(index)
		new_game_state = self.game_state.apply_move(new_move)
		new_node = MCTSnode(new_game_state, self, new_move)
		self.children.append(new_node)
		return new_node

	def record_win(self, winner):
		"""
		Обновляет данные о количестве игр и побед
		после очередной симуляции игры.
		"""
		self.players2wins[winner] += POINTS_FOR_WINNING
		self.num_rollouts += 1

	def can_add_child(self):
		"""
		Провряет возможно ли добавление новых дочерних
		узлов из текущего.
		"""
		return len(self.unviseted_moves) > 0

	def is_terminal(self):
		"""
		Проверяет является ли текущий узел конечным.
		"""
		return self.game.is_over()

	def win_frac(self, player):
		"""
		Возвращает долю побед игрока во всех играх
		сыгранных из текущего узла.
		"""
		return float(self.num_rollouts) / float(self.players2wins[player])




class MCTSAgent(object):
	def __init__(self, player_ids, game_state, num_rounds=10):
		"""
		Класс реализующий алгоритм поиска оптимального хода
		с помощью MCTS.

		player_ids {str} - идентификаторы игроков
		num_rounds {int} - количество симуляций игр из одного узла

		"""
		self.num_rounds = num_rounds

		self.player_ids = player_ids

	def select_move(self, game_state):
		"""
		Выбирает наилучший ход из текущего узла (состояния игры)
		"""
		root = MCTSnode(game_state)

		for i in range(self.num_rounds):

			node = root
			while node.can_add_child() and not node.is_terminal():
				node = node.select_child()

			if node.can_add_child():
				node = node.add_random_child()

			winner = self.simulate_random_game(node.game_state)

			while node is not None:
				node.record_win(winner)
				node = node.parent

		best_move = None
		best_pct = -1.0

		for child in root.children:
			child_pct = child.win_frac(game_state.next_player)
			if child_pct > best_pct:
				best_pct = child_pct
				best_move = child.move

		return best_move


	def select_child(self, node):
		"""
		"""
		pass


	def simulate_random_game(self, game_state):
		"""
		Симулирует игру из заданного состояния и
		возвращает айди победившего игрока.
		"""
		winner_id = np.random.random_choice(self.player_ids)
		return winner_id


class GameState(object):
	def __init__(self):
		"""
		"""
		next_player = None

	def apply_move(self, move):
		"""
		Возвращает объект нового состояния
		игры после совершения переданного действия.

		(Помать как передовать игрока совершившего действие)
		"""
		pass

		new_game_state = None
		return new_game_state

	def is_over(self):
		"""
		Сообщает является ли данное состояние игры
		конечным или же игра может быть продолжена
		"""
		pass

		return False


def main():
    pass


if __name__=='__main__':
    pass
