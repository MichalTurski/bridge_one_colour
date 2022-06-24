from argparse import ArgumentParser
from winning_probability import (
    IncompleteGameState,
    calculate_winning_probabilities,
    get_move_possibilities,
    remove,
)
from game_state import _score_trick
import json
from copy import deepcopy


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--table_state", type=json.loads, required=True)
    parser.add_argument("--nb_unknown_cards_op0", type=int, required=True)
    parser.add_argument("--nb_unknown_cards_op1", type=int, required=True)
    parser.add_argument("--unassigned_cards", type=json.loads, required=True)
    parser.add_argument("--current_trick", type=json.loads, default=[])
    parser.add_argument("--current_player", type=int, default=-1)
    args = vars(parser.parse_args())
    return args


def get_input_out_of_choices(choices):
    """
    Asks user for an integer input until user provide choice out of choices.
    :param choices: list of accepted user inputs
    """
    output = None
    while True:
        print(f"Please provide a card to play (possible choices: {choices})")
        try:
            output = int(input())
        except Exception:
            print(f"Please provide integer from {choices}")
        if output in choices:
            return output


def get_played_move(incomplete_game_state, played_card):
    """
    Function for checking which player made a move based on played card.
    It returns tuple (player, played_card).
    """
    if incomplete_game_state.current_player != -1:
        return (incomplete_game_state.current_player, played_card)
    if played_card in incomplete_game_state.table_state[0]:
        return (0, played_card)
    if played_card in incomplete_game_state.table_state[2]:
        return (2, played_card)
    return ValueError


def make_move(state, move):
    """
    Returns tuple (incomplete_game_state, is_lost) where
    incomplete_game_state is a state after making move,
    is_lost is True if the trick is lost (after 4 players played cards)
    """

    new_state = deepcopy(state)
    new_state.table_state[move[0]] = remove(new_state.table_state[move[0]], move[1])

    new_state.current_trick = state.current_trick + [move[1]]
    new_state.current_player = (move[0] + 1) % 4

    if move[1] in state.unassigned_cards:
        new_state.unassigned_cards = remove(state.unassigned_cards, move[1])
        if move[0] == 1:
            new_state.nb_unknown_cards_op0 = state.nb_unknown_cards_op0 - 1
        elif move[0] == 3:
            new_state.nb_unknown_cards_op1 = state.nb_unknown_cards_op1 - 1

    if move[1] == 0:
        if move[0] == 1:
            new_state.nb_unknown_cards_op0 = 0
        elif move[0] == 3:
            new_state.nb_unknown_cards_op1 = 0

    if len(new_state.current_trick) < 4:
        is_lost = False
        return new_state, is_lost
    elif len(new_state.current_trick) == 4:
        is_lost = not _score_trick(new_state)
        new_state.current_trick = []
        new_state.current_player = -1
        return new_state, is_lost


def main():
    args = parse_args()

    state = IncompleteGameState(
        table_state=args["table_state"],
        nb_unknown_cards_op0=args["nb_unknown_cards_op0"],
        nb_unknown_cards_op1=args["nb_unknown_cards_op1"],
        unassigned_cards=args["unassigned_cards"],
        current_trick=args["current_trick"],
        current_player=args["current_player"],
    )

    while True:
        if state.current_player in [-1, 0, 2]:
            calculate_winning_probabilities(state)

        possible_cards = [move[1] for move in get_move_possibilities(state)]

        played_card = get_input_out_of_choices(choices=possible_cards)
        played_move = get_played_move(state, played_card)
        state, is_lost = make_move(state=state, move=played_move)

        if is_lost:
            print("You lost the game!")
            break
        if len(state.current_trick) == 0:
            if (len(state.table_state[0]) + len(state.table_state[2]) == 0) | (
                len(state.table_state[1])
                + len(state.table_state[3])
                + len(state.unassigned_cards)
                == 0
            ):
                print("You won the game!")
                break


if __name__ == "__main__":
    main()
