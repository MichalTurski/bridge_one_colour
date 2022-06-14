from game_state import GameState, score_state


def test_take_from_up():
    game_state = GameState(table_state=[[13, 12, 11, 10, 9],
                           [8, 7, 6],
                           [5, 4, 3],
                           [2, 1]])
    assert score_state(game_state) == True


def test_missing_ace():
    game_state = GameState(table_state=[[12, 11, 10, 9],
                           [8, 7, 6],
                           [5, 4, 3],
                           [2, 1, 13]])
    assert score_state(game_state) == False


def test_possible_impasse():
    game_state = GameState(table_state=[[13, 11, 10, 9],
                           [8, 7, 6],
                           [5, 4, 3],
                           [12, 2, 1]])
    assert score_state(game_state) == True


def test_impossible_impasse():
    game_state = GameState(table_state=[[13, 11, 10, 9],
                           [12, 8, 7, 6],
                           [5, 4, 3],
                           [2, 1]])
    assert score_state(game_state) == False


def test_impasse_correctly_played():
    game_state = GameState(table_state=[[13, 11, 10, 9],
                           [8, 7, 6],
                           [4, 3],
                           [12, 2, 1]],
                           current_trick=[5],
                           current_player=3)
    assert score_state(game_state) == True


def test_impasse_incorrectly_played():
    game_state = GameState(table_state=[[11, 10, 9],
                           [8, 7, 6],
                           [5, 4, 3],
                           [12, 2, 1]],
                           current_trick=[13],
                           current_player=1)
    assert score_state(game_state) == False


def test_empty_W_hand():
    game_state = GameState(table_state=[[13, 10, 9, 8, 7, 6],
                           [],
                           [5, 4, 2, 1],
                           [3, 12]],
                           current_player=1,
                           current_trick=[11])
    assert score_state(game_state) == False
