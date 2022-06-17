from argparse import ArgumentParser
from winning_probability import IncompleteGameState, calculate_winning_probabilities
import json

parser = ArgumentParser()
parser.add_argument("--table_state", type=json.loads, required=True)
parser.add_argument("--nb_unknown_cards_op0", type=int, required=True)
parser.add_argument("--nb_unknown_cards_op1", type=int, required=True)
parser.add_argument("--unassigned_cards", type=json.loads, required=True)
parser.add_argument("--current_trick", type=json.loads, default=[])
parser.add_argument("--current_player", type=int, default=-1)
args = vars(parser.parse_args())

incomplete_game_state = IncompleteGameState(
    table_state=args["table_state"],
    nb_unknown_cards_op0=args["nb_unknown_cards_op0"],
    nb_unknown_cards_op1=args["nb_unknown_cards_op1"],
    unassigned_cards=args["unassigned_cards"],
    current_trick=args["current_trick"],
    current_player=args["current_player"],
)

calculate_winning_probabilities(incomplete_game_state)
