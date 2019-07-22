from .first_solution import SimpleSolution


if __name__ == '__main__':
    solution = SimpleSolution()
    solution.wait_for_start()
    while not solution.is_finish():
        solution.game_loop()