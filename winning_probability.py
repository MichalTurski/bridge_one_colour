import itertools
import math
from copy import deepcopy
from dataclasses import dataclass, field
from typing import List

from game_state import GameState, score_state


@dataclass()
class IncompleteGameState:
    table_state: List[List[int]]  # Cards, which each player holds
    nb_unknown_cards_op0: int  # Number of unknown cards of player 1 (opponent 0)
    nb_unknown_cards_op1: int  # Number of unknown cards of player 3 (opponent 1)
    unassigned_cards: List[int]  # Cards not assigned to any player yet
    current_player: int = -1  # Player who should add card now, 0=N, 1=E, 2=S, 3=W
    current_trick: List[int] = field(
        default_factory=lambda: []
    )  # Cards added in current trick so far


def get_state_probability(
    nb_new_cards_op0, nb_new_cards_op1, nb_unknown_cards_op0, nb_unknown_cards_op1
):
    nb_new_cards = nb_new_cards_op0 + nb_new_cards_op1
    nb_unknown_cards = nb_unknown_cards_op0 + nb_unknown_cards_op1

    return math.comb(
        nb_unknown_cards - nb_new_cards, nb_unknown_cards_op0 - nb_new_cards_op0
    ) / math.comb(nb_unknown_cards, nb_unknown_cards_op0)


def get_move_possibilities(state):
    """
    Return list of possible moves of a current player in a given incomplete state.
    If user has consecutive cards, only one maximal is returned (since they are equivalent).
    If player has unknown cards, all unassigned cards are possible to play.
    """
    possible_players = [0, 2] if state.current_player == -1 else [state.current_player]
    table_state = deepcopy(state).table_state
    possibilities = []
    for player in possible_players:
        possibilities = possibilities + [
            (player, card)
            for card in table_state[player]
            if card + 1 not in table_state[player]
        ]
    if len(possibilities) == 0:
        possibilities = [(possible_players[0], 0)]

    if possible_players == [[1]]:
        if (
            state.nb_unknown_cards_op0
            if possible_players == [1]
            else state.nb_unknown_cards_op1
        ) > 0:
            possibilities += [
                (possible_players[0], card) for card in state.unassigned_cards
            ]
    return possibilities


def remove(list, element):
    """
    Removes an element from the list
    """
    return [x for x in list if x != element]


def calculate_winning_probabilities(incomplete_state):
    """
    incomplete_state: incomplete_game_state
    """
    unassigned_cards = incomplete_state.unassigned_cards
    nb_unknown_cards_op0 = incomplete_state.nb_unknown_cards_op0
    nb_unknown_cards_op1 = incomplete_state.nb_unknown_cards_op1

    next_move_win_prob = {}

    for move in get_move_possibilities(incomplete_state):
        state = deepcopy(incomplete_state).table_state
        state[move[0]] = remove(state[move[0]], move[1])
        print(f"If you play {move[1]} the following scenarios are possible:")

        for nb_new_cards_op0 in range(
            max(0, len(unassigned_cards) - nb_unknown_cards_op1),
            min(len(unassigned_cards), nb_unknown_cards_op0) + 1,
        ):
            state_prob = get_state_probability(
                nb_new_cards_op0,
                len(unassigned_cards) - nb_new_cards_op0,
                incomplete_state.nb_unknown_cards_op0,
                incomplete_state.nb_unknown_cards_op1,
            )

            for new_cards_op0 in itertools.combinations(
                unassigned_cards, nb_new_cards_op0
            ):
                cards_op = [
                    state[1] + list(new_cards_op0),
                    state[3] + list(set(unassigned_cards) - set(new_cards_op0)),
                ]
                is_winning = score_state(
                    GameState(
                        table_state=[state[0], cards_op[0], state[2], cards_op[1],],
                        current_player=move[0] + 1,
                        current_trick=incomplete_state.current_trick + [move[1]],
                    )
                )

                next_move_win_prob[move[1]] = (
                    next_move_win_prob.get(move[1], 0) + state_prob * is_winning
                )

                print(
                    "opponents cards:",
                    cards_op,
                    "probability:",
                    state_prob,
                    "winning:",
                    is_winning,
                )
        print("\n")
    winning_probabilities = dict(
        sorted(next_move_win_prob.items(), key=lambda item: -item[1])
    )

    print(
        f"SUMMARY\n"
        f"Current game state: {incomplete_state}\n\n"
        f"Depending on your move you have the following winning probability: {winning_probabilities}"
    )

    return winning_probabilities
