from copy import deepcopy
from dataclasses import dataclass, field
from typing import List


@dataclass()
class GameState:
    table_state: List[List[int]]  # Cards, which each player holds
    current_player: int = -1  # Player who should add card now, 0=N, 1=E, 2=S, 3=W
    current_trick: List[int] = field(default_factory=lambda: [])  # Cards added in current trick so far
    # E.g. of not started game
    # current_player: int = -1 # Game not started yet, hence there is no current player
    # current_trick = [] # There is no current trick
    # table_state = [[13, 11, 10, 9], # Cards of N
    #                [7, 6, 5], # E
    #                [8, 1], # S
    #                [12, 4, 3, 2]] # W
    #
    # After first card played:
    # current_player: int = 1 # East should add card now
    # current_trick = [13] # N gave ace
    # table_state = [[11, 10, 9], # Cards of N, note he ued his ace
    #                [7, 6, 5], # E
    #                [8, 1], # S
    #                [12, 4, 3, 2]] # W

    def curr_p_goal(self) -> bool:
        return self.current_player in {0, 2}


def _try_possibilities(game_state: GameState) -> bool:
    my_cards = game_state.table_state[game_state.current_player]
    if not my_cards:
        state_copy = deepcopy(game_state)
        state_copy.current_trick.append(0)
        return score_state(state_copy)  # No choice, nothing to copy
    else:
        for idx, card in enumerate(my_cards):
            state_copy = deepcopy(game_state)
            del state_copy.table_state[game_state.current_player][idx]
            state_copy.current_trick.append(card)
            state_copy.current_player = (state_copy.current_player + 1) % 4
            score = score_state(state_copy)
            if score == game_state.curr_p_goal():  # If this card guarantees player goal, don't look further.
                return score
        return not game_state.curr_p_goal()  # Player couldn't pick any card, which guarantees his goal.


def _score_trick(game_state: GameState):
    assert len(game_state.current_trick) == 4
    assert game_state.current_player >= 0
    assert len(game_state.current_trick) > 0

    max_card = max(game_state.current_trick)
    if max_card == game_state.current_trick[0] or max_card == game_state.current_trick[2]:
        return True
    else:
        return False


def _new_trick(game_state: GameState):
    if len(game_state.table_state[0]) == 0 and len(game_state.table_state[2]) == 0:
        # Player NS can't take any more tricks, he reached his goal.
        return True

    for player in {0, 2}:
        for idx, card in enumerate(game_state.table_state[player]):  # For each card on NS.
            state_copy = deepcopy(game_state)
            state_copy.current_trick = [card]
            state_copy.current_player = player + 1
            del state_copy.table_state[player][idx]
            if score_state(state_copy):  # If some card guarantees winning, let's play it.
                return True
    return False  # No card guarantees winning, give up.


def score_state(game_state: GameState) -> bool:
    if len(game_state.current_trick) == 4:
        if not _score_trick(game_state):
            return False
        else:
            return _new_trick(game_state)
    elif len(game_state.current_trick) == 0:
        return _new_trick(game_state)
    else:
        return _try_possibilities(game_state)
