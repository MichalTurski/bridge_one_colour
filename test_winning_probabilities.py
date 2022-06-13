from winning_probability import (
    IncompleteGameState,
    get_state_probability,
    get_move_possibilities,
    calculate_winning_probabilities,
)


def test_get_state_probability():
    assert (
        get_state_probability(
            nb_new_cards_op0=1,
            nb_new_cards_op1=1,
            nb_unknown_cards_op0=2,
            nb_unknown_cards_op1=6,
        )
        == 6 / 28
    )


def test_get_move_possibilities():
    game_state = IncompleteGameState(
        table_state=[[13, 11, 10, 9, 8, 7, 6], [], [5, 4, 2, 1], []],
        nb_unknown_cards_op0=1,
        nb_unknown_cards_op1=5,
        unassigned_cards=[],
    )
    assert set(get_move_possibilities(game_state)) == set(
        [(0, 13), (0, 11), (2, 5), (2, 2)]
    )


def test_get_move_possibilities_current_player():
    game_state = IncompleteGameState(
        table_state=[[13, 11, 10, 9, 8, 7, 6], [], [5, 4, 2, 1], []],
        nb_unknown_cards_op0=1,
        nb_unknown_cards_op1=5,
        unassigned_cards=[],
        current_trick=[13, 12],
        current_player=2,
    )
    assert set(get_move_possibilities(game_state)) == set([(2, 5), (2, 2)])


def test_calculate_winning_probabilities_trivial():
    incomplete_game_state = IncompleteGameState(
        table_state=[[13, 9], [12], [11], [10]],
        nb_unknown_cards_op0=0,
        nb_unknown_cards_op1=0,
        unassigned_cards=[],
    )
    assert calculate_winning_probabilities(incomplete_game_state) == {
        13: 1,
        9: 0,
        11: 1,
    }


def test_calculate_winning_probabilities():
    incomplete_game_state = IncompleteGameState(
        table_state=[[13, 11, 10, 9, 8, 7, 6], [], [5, 4, 2, 1], []],
        nb_unknown_cards_op0=13,
        nb_unknown_cards_op1=13,
        unassigned_cards=[3, 12],
    )
    assert calculate_winning_probabilities(incomplete_game_state) == {
        13: 0.52,
        11: 0,
        5: 0.76,
        2: 0.76,
    }


def test_calculate_winning_probabilities_unknown_1():
    incomplete_game_state = IncompleteGameState(
        table_state=[[13, 11, 10, 9, 8, 7, 6], [], [5, 4, 2, 1], []],
        nb_unknown_cards_op0=1,
        nb_unknown_cards_op1=1,
        unassigned_cards=[3, 12],
    )
    assert calculate_winning_probabilities(incomplete_game_state) == {
        13: 1,
        11: 0,
        5: 1,
        2: 1,
    }


def test_calculate_winning_probabilities_currect_trick():
    incomplete_game_state = IncompleteGameState(
        table_state=[[13, 11, 10, 9, 8, 7, 6], [], [4, 2, 1], []],
        nb_unknown_cards_op0=5,
        nb_unknown_cards_op1=5,
        unassigned_cards=[12],
        current_trick=[5, 3],
        current_player=0,
    )
    assert calculate_winning_probabilities(incomplete_game_state) == {13: 0.5, 11: 0.5}
