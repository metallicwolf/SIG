olol = 'SALEDATE DATE'


def line_check(new_line: str):
    if new_line.rfind(',') > -1:
        new_line = new_line[:new_line.rfind(',')]
    if new_line.count('(') < new_line.count(')'):
        new_line = new_line[:new_line.rfind(')')]

    return new_line


print(line_check(olol))
