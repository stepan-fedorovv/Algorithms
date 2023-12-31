import os
import re
from PDA import PushdownAutomata
import logging

logging.basicConfig(level=logging.INFO)


def main():
    files = sorted([i for i in os.listdir() if re.match(
        ".*.txt$", i) and i != "requirements.txt"])
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
    pda = PushdownAutomata.from_file(filename)
    if pda.is_determined:
        print(f"PDA is determined")
    else:
        print("PDA is not determined")
    if pda.string_to_process:
        res = pda.process_string()
        print(
            f"Processing string {pda.string_to_process}. Result is {res}")
        if res:
            print(f"Path: {'->'.join(pda.path)}")
    while True:
        result = pda.process_string(input("String to process: "))
        print(str(result))
        if result:
            print(f"Path {';'.join(pda.path)}")


if __name__ == '__main__':
    main()
