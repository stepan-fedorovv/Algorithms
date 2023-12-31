from Parser import Parser
import logging


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = Parser.from_file('./Cgrammar.txt')
    print('\nParsing table')
    parser.print_table(parser.parsing_table, save_to_csv='parsing_table.csv')
    parser.add_sync()
    print('\nSyntax analysis table')
    parser.print_table(parser.syntax_analysis_table,
                       save_to_csv='syntax_analysis.csv')
    with open('test2.txt') as file:
        program_text = file.read()
        errors = parser.test_string(program_text)
        text_pos = 0
        err_cnt = 0
        line_errors = []
        while err_cnt < len(errors)-1 or text_pos < len(program_text)-1:
            if text_pos == len(program_text) and errors[err_cnt].position == -1:
                print(errors[err_cnt].message)
                err_cnt += 1
                continue
            if errors:
                if errors[err_cnt].position == text_pos:
                    if errors[err_cnt].message:
                        line_errors.append(errors[err_cnt].message)
                    if program_text[text_pos] != '\n':
                        print(program_text[text_pos], end='')
                    if len(errors)-1 > err_cnt:
                        err_cnt += 1
                elif program_text[text_pos] != '\n':
                    print(program_text[text_pos], end='')
            elif program_text[text_pos] != '\n':
                print(program_text[text_pos], end='')
            if program_text[text_pos] == '\n':
                print("\t", line_errors if line_errors else '')
                line_errors = []
            text_pos += 1
            if text_pos == 75:
                pass


if __name__ == '__main__':
    main()
