from State import State
import os
import re
import logging

from prettytable import PrettyTable

from StateMachine import StateMachine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")


def process_file(filename: str, state_machine: StateMachine) -> list[str]:
    strings_to_process = []
    with open(filename) as file:
        is_processing_FSM = True
        for line in file:
            if is_processing_FSM:
                is_processing_FSM = is_processing_FSM and state_machine.process_line(
                    line)
            else:
                if line.startswith(";"):
                    strings_to_process.append(line[1:-1])
                else:
                    logger.warning(
                        f"Skipping line {line.__repr__()}. Unacceptable format")
    return strings_to_process


def process_line(states: dict[str, State], line: str) -> bool:
    state = states["q0"]
    assert state.is_initial
    for char in line:
        try:
            state = state.consume_symbol(char)
        except ValueError as e:
            logger.error(e)
            return False
    return state.is_final


def main():
    files = [i for i in os.listdir() if re.match(
        ".*.txt$", i) and i != "requirements.txt"]
    print("Choose file to process")
    for n, filename in enumerate(files):
        print(f"{n}. {filename}")
    filename = ""
    while not filename:
        try:
            inp = int(input())
            filename = files[inp]
        except Exception:
            print("Incorrect input")
    state_machine = StateMachine()
    strings_to_process = process_file(filename, state_machine)
    state_machine.print_graph(filename)
    is_new = state_machine.determine()
    table = PrettyTable(["String", "Is accepted"])
    for string in strings_to_process:
        result = state_machine.consume_string(string, is_new)
        table.add_row([string, result])
    print(table)
    state_machine.print_graph(filename, is_new)
    while True:
        string_value = input("Input string: \n")
        print(state_machine.consume_string(string=string_value, new=is_new))


if __name__ == "__main__":
    main()
