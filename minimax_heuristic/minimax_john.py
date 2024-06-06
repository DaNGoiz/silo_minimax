import pickle
import numpy as np
import sys
from functools import cache

RED = "R"
BLUE = "B"

class Game2:
    def __init__(self, silos=5, initial_state=None):
        self.silo_cnt = silos
        self.state = initial_state if initial_state else '.' * (self.silo_cnt * 3)
        self.evaluation_cache = {}
        self.max_depth = 15
        self.depth_trigger = 12
        self.count = 0

    def get_moves(self, state):
        return [i for i in range(self.silo_cnt) if state[i*3:i*3+3].count('.') > 0]

    def make_move(self, state, team, move):
        pos = state[move*3:move*3+3].index('.')
        new_state = list(state)
        new_state[move*3+pos] = RED if team == 'red' else BLUE
        return ''.join(new_state)

    def is_terminal(self, state):
        if '.' not in state:
            return True
        if self.is_great_victory(state) != "":
            return True
        return False

    def is_great_victory(self, state):
        for team_char in [RED, BLUE]:
            silo_occupy_cnt = 0
            for i in range(0, len(state), 3):
                silo_state = state[i:i+3]
                team_ball_cnt = silo_state.count(team_char)
                top_silo_ball = silo_state[-1]
                if (team_ball_cnt >= 2) and (top_silo_ball == team_char):
                    silo_occupy_cnt += 1
            if (silo_occupy_cnt >= 3):
                return team_char
        return ""

    def evaluate(self, state):
        if self.is_great_victory(state) != "":
            score = 9999 if self.is_great_victory(state) == RED else -9999
            return score * (0.99 ** (state.count(RED) + state.count(BLUE)))

        score = state.count(RED) * 30 - state.count(BLUE) * 30

        if not self.is_terminal(state):
            silo_state_score_map = {
                "RRB": +0,
                "RR.": +5,
                "RBR": +10,
                "BRR": +10,
                "BBR": +0,
                "BB.": -5,
                "RBB": -10,
                "BRB": -10,
            }
            for silo in [state[i*3:i*3+3] for i in range(self.silo_cnt)]:
                if silo in silo_state_score_map.keys():
                    score += silo_state_score_map[silo]
        return score * (0.99 ** (state.count(RED) + state.count(BLUE)))

    @cache
    def minimax(self, depth, team, parent_state=None):
        if parent_state is None:
            parent_state = '.' * (self.silo_cnt * 3)

        # cache_key = (parent_state, depth, team)
        # if cache_key in self.evaluation_cache:
        #     return self.evaluation_cache[cache_key], decision_map.get(parent_state, [])

        if depth == 0 or self.is_terminal(parent_state):
            evaluation = self.evaluate(parent_state)
            # self.evaluation_cache[cache_key] = evaluation
            return evaluation, []

        moves = np.array(self.get_moves(parent_state))
        # print(f"count: {self.count}: moves: {moves}")
        best_value = -sys.maxsize if team == 'red' else sys.maxsize
        best_moves = np.empty(0)
        if team == "red":
            new_states = np.array([self.make_move(parent_state, team, move) for move in moves])
            scores = np.array([self.minimax(depth - 1, "blue", new_state)[0] for new_state in new_states])
            best_value = np.max(scores)
            best_moves = moves[np.argwhere(scores == np.amax(scores))]
            best_state = new_states[np.argwhere(scores == np.amax(scores))]
            # print(f"red,  state: {parent_state}: count: {self.count}: best_value: {best_value}, best_moves: {best_moves}, best state: {best_state}")
            # print(f"red,  state: {parent_state}: count: {self.count}: new_states: {new_states}, scores: {scores}")
        elif team == "blue":
            new_states = np.array([self.make_move(parent_state, team, move) for move in moves])
            scores = np.array([self.minimax(depth - 1, "red", new_state)[0] for new_state in new_states])
            best_value = np.min(scores)
            best_moves = moves[np.argwhere(scores == np.amin(scores))]
            best_state = new_states[np.argwhere(scores == np.amin(scores))]
            # print(f"blue, state: {parent_state}: count: {self.count}: best_value: {best_value}, best_moves: {best_moves}, best state: {best_state}")
            # print(f"blue, state: {parent_state}: count: {self.count}: new_states: {new_states}, scores: {scores}")

        # self.evaluation_cache[cache_key] = best_value
        # decision_map[parent_state] = best_moves

        self.count += 1
        # if self.count % 10000 == 0:
        #     print(f"No: {self.count}, State: {parent_state}, Best moves: {decision_map[parent_state] if parent_state in decision_map else None}, Best Value: {best_value}")

        return best_value, best_moves.flatten().tolist()

initial_state = None
silos_count = 5
# game2 = Game2(silos_count, initial_state=initial_state)
# decision_map2 = {}
# best_value2, best_moves2 = game2.minimax(15, 'red', parent_state="BRRBB.BBBRR.RRR", decision_map=decision_map2)
# print(best_value2)
# print(best_moves2)

new_decision_map = {}
count2 = 0
for state in all_states:
    game2 = Game2(silos_count, initial_state=initial_state)
    best_value2, best_moves2 = game2.minimax(15, 'red', parent_state=state)
    new_decision_map[state] = best_moves2

    if count2 % 10000 == 0:
        print(f"No: {count2}: state: {state}, best value: {best_value2}, best moves: {best_moves2}")
    count2 += 1

with open('decision_map_heuristic_new3.pkl', 'wb') as file:
    pickle.dump(new_decision_map, file)