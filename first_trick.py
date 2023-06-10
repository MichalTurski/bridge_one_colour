import itertools
from copy import deepcopy
import numpy as np

from game_state import GameState, score_state
from winning_probability import IncompleteGameState, get_move_possibilities, remove


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
            possible_states.append(new_state)
    return possible_states


def last_card_in_trick(state: IncompleteGameState):
    assert len(state.current_trick) == 3
    assert state.current_player in {1, 3}
    possible_states = generate_possible_states(state)
    winning = []
    for s in possible_states:
        winning.append(score_state(s))
    return np.mean(winning)


def second_card_in_trick(state: IncompleteGameState):
    assert len(state.current_trick) == 1
    assert state.current_player in {1, 3}
    possible_states = generate_possible_states(state)
    state_scores = []
    for state_deterministic in possible_states:
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
            new_state.table_state[state.current_player] = remove(player_hand, card)
            new_state.current_trick.append(card)
            new_state.current_player = (new_state.current_player + 1) % 4
            third_card_winning_probas = player_move(new_state)
            # We assume the next player will pick his best choice.
            opponent_scores.append(max([p for _, _, p in third_card_winning_probas]))
        state_scores.append(min(opponent_scores))  # Opponent minimizes our winning probability.
    return np.mean(state_scores)


def player_move(state: IncompleteGameState):
    assert state.current_player in {-1, 0, 2}
    possible_moves = get_move_possibilities(state)
    player_card_score_triplets = []
    for player, card in possible_moves:
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
