import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from logic.quarto_logic import Quarto

def test_diag_0():
    actions = [3, 0, 1, 5, 5, 10, 0, 15]
    test = Quarto()
    for a in actions:
        test.transition(a)
    assert test.end() == 0

def test_diag_1():
    actions = [3, 3, 1, 6, 5, 9, 0, 12]
    test = Quarto()
    for a in actions:
        test.transition(a)
    assert test.end() == 0

def test_row_0():
    actions = [3, 0, 1, 1, 5, 2, 0, 3]
    test = Quarto()
    for a in actions:
        test.transition(a)
    assert test.end() == 0

def test_row_1():
    actions = [3, 4, 1, 5, 5, 6, 0, 7]
    test = Quarto()
    for a in actions:
        test.transition(a)
    assert test.end() == 0

def test_row_2():
    actions = [3, 8, 1, 9, 5, 10, 0, 11]
    test = Quarto()
    for a in actions:
        test.transition(a)
    assert test.end() == 0

def test_row_3():
    actions = [3, 12, 1, 13, 5, 14, 0, 15]
    test = Quarto()
    for a in actions:
        test.transition(a)
    assert test.end() == 0

def test_col_0():
    actions = [3, 0, 1, 4, 5, 8, 0, 12]
    test = Quarto()
    for a in actions:
        test.transition(a)
    assert test.end() == 0

def test_col_1():
    actions = [3, 1, 1, 5, 5, 9, 0, 13]
    test = Quarto()
    for a in actions:
        test.transition(a)
    assert test.end() == 0

def test_col_2():
    actions = [3, 2, 1, 6, 5, 10, 0, 14]
    test = Quarto()
    for a in actions:
        test.transition(a)
    assert test.end() == 0

def test_col_3():
    actions = [3, 3, 1, 7, 5, 11, 0, 15]
    test = Quarto()
    for a in actions:
        test.transition(a)
    assert test.end() == 0

# def test_tie():
#     actions = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15]
#     test = Quarto()
#     for a in actions:
#         test.transition(a)
#     assert test.end() == -1


