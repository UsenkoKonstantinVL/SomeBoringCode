from .q_model import QModel
from .game_env import GameEnv
from copy import deepcopy
import random


class Memory:
    def __init__(self, max_memory):
        self._max_memory = max_memory
        self._samples = []

    def add_sample(self, sample):
        self._samples.append(sample)
        if len(self._samples) > self._max_memory:
            self._samples.pop(0)

    def sample(self, no_samples):
        if no_samples > len(self._samples):
            return random.sample(self._samples, len(self._samples))
        else:
            return random.sample(self._samples, no_samples)


MEMORY_SIZE = 1000
BATCH_SIZE = 64
GAMES_COUNT = 10


def choose_command(q_values):
    return 0


if __name__ == '__main__':
    model = QModel()
    best_model = deepcopy(model)

    env = GameEnv()
    env.initialize_players(['q_model', 'best_q_model'])
    replay_buffer = Memory()
    finish_flag = False

    for game_id in range(GAMES_COUNT):
        
        state = env.start_game()

        q_model_total_reward = 0
        best_q_model_total_reward = 0

        while not finish_flag:
            q_values = model.predict(state)
            model_act = choose_command(q_values)
            env.act('q_model', model_act)

            q_values_ = best_model.predict(state)
            model_act_ = choose_command(q_values_)
            env.act('best_q_model', model_act_)

            new_state, reward, done = env.play()
            finish_flag = done

            q_model_reward = reward['q_model']
            best_q_model_reward = reward['best_q_model']
            
            replay_buffer.append([state, new_state, q_model_reward, model_act, done])

            state = new_state

        if q_model_total_reward > best_q_model_total_reward:
            best_model = model.clone()
    
        model.train(replay_buffer)
