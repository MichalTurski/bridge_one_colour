import itertools
from copy import deepcopy
import numpy as np
from argparse import ArgumentParser
import json

from game_state import GameState, score_state
from winning_probability import IncompleteGameState, get_move_possibilities, remove, get_state_probability

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

def generate_possible_states(state: IncompleteGameState) -> list[GameState]:
    assert state.current_player in {1, 3}
    possible_states = []

    player_1_max_len = min(state.nb_unknown_cards_op0, len(state.unassigned_cards)) + 1
    player_1_min_len = max(0, len(state.unassigned_cards) - state.nb_unknown_cards_op1)
    assert player_1_min_len <= state.nb_unknown_cards_op0,\
        f"Opponents can't have {state.nb_unknown_cards_op0} and {state.nb_unknown_cards_op1} unassigned cards " \
        f"while there remains {len(state.unassigned_cards)} unassigned cards."
    for player_1_len in range(player_1_min_len, player_1_max_len):
        for player_1_cards in itertools.combinations(state.unassigned_cards, player_1_len):
            player_3_cards = [c for c in state.unassigned_cards if c not in player_1_cards]
            new_state = GameState(deepcopy(state.table_state), deepcopy(state.current_player), deepcopy(state.current_trick))
            new_state.table_state[1].extend(player_1_cards)
            new_state.table_state[3].extend(player_3_cards)
            state_probability = 0.2
            state_probability = get_state_probability(
                player_1_len,
                len(state.unassigned_cards) - player_1_len,
                state.nb_unknown_cards_op0,
                state.nb_unknown_cards_op1,
            )
            possible_states.append([new_state, state_probability])
    return possible_states


def last_card_in_trick(state: IncompleteGameState):
    assert len(state.current_trick) == 3
    assert state.current_player in {1, 3}
    prob_winning = 0
    for s, prob in generate_possible_states(state):
        if score_state(s):
            prob_winning += prob
    return prob_winning


def second_card_in_trick(state: IncompleteGameState):
    assert len(state.current_trick) == 1
    assert state.current_player in {1, 3}
    state_scores = 0
    for state_deterministic, state_probability in generate_possible_states(state):
        print(f'Possible state: {state_deterministic.table_state}, probability={state_probability}')
        player_hand = state_deterministic.table_state[state.current_player]
        possible_cards = [c for c in player_hand if c + 1 not in player_hand]
        if not possible_cards:
            possible_cards = [0]

        opponent_scores = []
        for card in possible_cards:
            new_state = deepcopy(state)
            if card == 0:
                new_state.nb_unknown_cards_op0 = 0
                new_state.nb_unknown_cards_op1 = 0
                second_op = (new_state.current_player + 2) % 4
                new_state.table_state[second_op].extend(new_state.unassigned_cards)
                new_state.unassigned_cards = []
            elif card in new_state.unassigned_cards:
                if new_state.current_player == 1:
                    new_state.nb_unknown_cards_op0 -= 1
                else:
                    new_state.nb_unknown_cards_op1 -= 1
                new_state.unassigned_cards = remove(new_state.unassigned_cards, card)
            new_state.table_state[state.current_player] = remove(new_state.table_state[new_state.current_player], card)
            new_state.current_trick.append(card)
            new_state.current_player = (new_state.current_player + 1) % 4
            third_card_winning_probas = player_move(new_state)
            # We assume the next player will pick his best choice (highest card in case of tie)
            opponent_card = sorted(sorted(third_card_winning_probas, key=lambda x: x[1], reverse=True), key=lambda x: x[2], reverse=True)[0][1]
            # We check whether the game is won or not after this choice.
            new_state_deterministic = deepcopy(state_deterministic)
            current_player = new_state_deterministic.current_player
            new_state_deterministic.table_state[current_player] = remove(new_state_deterministic.table_state[current_player], card)
            new_state_deterministic.table_state[(current_player+1)%4] = remove(new_state_deterministic.table_state[(current_player+1)%4], opponent_card)
            new_state_deterministic.current_trick.extend([card, opponent_card])
            new_state_deterministic.current_player = (current_player+2)%4
            score = score_state(new_state_deterministic)
            print(f'Opponent knows that if he play {card} then third move would be {opponent_card} which means {"WIN" if score==1 else "LOSE"} for us, (third card winning probabilities: {third_card_winning_probas})')
            opponent_scores.append(int(score))
        if min(opponent_scores) == 1:
            print("Whatever opponent plays we WIN!")
            state_scores += state_probability
        else:
            print('Opponent can choose a card for which we LOSE!')
        print('')
    return np.mean(state_scores)


def player_move(state: IncompleteGameState):
    assert state.current_player in {-1, 0, 2}
    possible_moves = get_move_possibilities(state)
    player_card_score_triplets = []
    for player, card in possible_moves:
        if state.current_player == -1:
            print(f"\nAnalyzing first move as player:{player}, card:{card}")
        new_state = deepcopy(state)
        if new_state.current_player == -1:
            new_state.current_player = player
        player_hand = new_state.table_state[player]
        new_state.table_state[player] = remove(player_hand, card)
        new_state.current_trick.append(card)
        new_state.current_player = (new_state.current_player + 1) % 4
        if len(new_state.current_trick) == 3:
            win_proba = last_card_in_trick(new_state)
        else:
            win_proba = second_card_in_trick(new_state)
        player_card_score_triplets.append((player, card, win_proba))
    return player_card_score_triplets

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
    print(f'SUMMARY: {player_move(state)}')

if __name__ == "__main__":
    main()
