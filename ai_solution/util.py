from copy import deepcopy

POSITION_CHANGE = {
    'left': [-1, 0],
    'right': [1, 0],
    'up': [0, 1],
    'down': [0, -1]
}

def get_next_point(state, act):
    player_pos = state['params']['players']['i']['position']
    position_change = POSITION_CHANGE[act]
    new_pos = deepcopy(player_pos)
    new_pos[0] += position_change[0]
    new_pos[1] += position_change[1]

    return new_pos


def check_for_available(pos, state):
    x_max = state['params']['x_cells_count']
    y_max = state['params']['y_cells_count']

    if pos[0] < 0 or pos[0] >= x_max:
        return False

    if pos[1] < 0 or pos[1] >= y_max:
        return False

    return True


def construct_paths(point, next_point, state):
    pass


def compute_path_score(path, state):
    pass