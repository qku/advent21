import io
import numpy as np


def load_input(f):
    with open(f) as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if line == '\n':
                split_i = i

        instructions = lines[split_i+1:]

    instructions = [i.split()[-1].split('=') for i in instructions]
    # convert to (axis, crease) tuple
    d = {'x': 1, 'y': 0}
    instructions = [(d[i[0]], int(i[1])) for i in instructions]

    dots = np.loadtxt(f, delimiter=',', dtype=int, max_rows=split_i)
    return dots, instructions


def get_paper(dots):
    columns, rows = dots.max(axis=0) + 1
    paper = np.zeros((rows, columns), dtype=int)

    for x, y in dots:
        paper[y, x] = 1

    return paper


def do_fold(paper, axis, crease):
    sides = np.split(paper, [crease, crease + 1], axis=axis)
    folded_paper = sides[0] + np.flip(sides[2], axis=axis)
    return folded_paper


def count_after_first_fold(f):
    dots, instructions = load_input(f)
    paper = get_paper(dots)

    axis, crease = instructions[0]
    paper_folded = do_fold(paper, axis, crease)
    return np.count_nonzero(paper_folded)


def print_paper(paper):
    bio = io.BytesIO()
    paper[paper > 0] = 1
    np.savetxt(bio, paper, delimiter='', fmt='%1i')
    print_string = bio.getvalue().decode('utf-8')
    print_string = print_string.replace('0', ' ')
    print_string = print_string.replace('1', '#')
    print(print_string)


def print_after_all_folds(f):
    dots, instructions = load_input(f)
    paper = get_paper(dots)

    for axis, crease in instructions:
        paper = do_fold(paper, axis, crease)

    print_paper(paper)


n = count_after_first_fold('input.txt')
print(f'Dots after first fold: {n}')

print_after_all_folds('input.txt')
