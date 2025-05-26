import queue
import threading

from src.sysmac import export_symbols_to_file
from src.sysmac_solution import SysmacSolution, get_solutions


def get_vars_from_solution(solutions_path, solution_uuid):
    solution = SysmacSolution(solutions_path, solution_uuid)
    symbols = solution.get_published_symbols()
    return solution, symbols


class WorkerThread(threading.Thread):
    def __init__(self, task_queue, result_queue):
        super().__init__(daemon=True)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        while True:
            try:
                command, args = self.task_queue.get(timeout=1)
                if command == 'get_solutions':
                    solutions_path = args[0]
                    data = get_solutions(solutions_path)
                    self.result_queue.put((command, data))
                elif command == 'get_vars_from_solution':
                    solution, symbols = get_vars_from_solution(*args)
                    data = {
                        'solution': solution,
                        'symbols': symbols
                    }
                    self.result_queue.put((command, data))
                elif command == 'save_symbols_to_file':
                    solution = args[0]
                    symbols = args[1]
                    filename = args[2]
                    export_symbols_to_file(symbols, filename)
                    data = {
                        'solution': solution,
                        'filename': filename
                    }
                    self.result_queue.put((command, data))
                elif command == "stop":
                    break
            except queue.Empty:
                continue
