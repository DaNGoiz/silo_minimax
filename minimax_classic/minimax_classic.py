import sys
import pickle

RED = "R"
BLUE = "B"

class Game:
    def __init__(self, silos=5, initial_state=None):
        self.silos = silos
        self.state = initial_state if initial_state else '.' * (self.silos * 3)
        self.evaluation_cache = {}
        self.count = 0

    def get_moves(self):
        red_moves = [(i, 'red') for i in range(self.silos) if self.state[i*3:i*3+3].count('.') > 0]
        blue_moves = [(i, 'blue') for i in range(self.silos) if self.state[i*3:i*3+3].count('.') > 0]
        return red_moves + blue_moves

    def make_move(self, team, move):
        pos = self.state[move*3:move*3+3].index('.')
        new_state = list(self.state)
        new_state[move*3+pos] = RED if team == 'red' else BLUE
        return ''.join(new_state)

    def unmake_move(self, original_state):
        self.state = original_state

    def is_great_victory(self):
        for team_char in [RED, BLUE]:
            silo_occupy_cnt = 0
            for i in range(0, len(self.state), 3):
                silo_state = self.state[i:i+3]
                team_ball_cnt = silo_state.count(team_char)
                top_silo_ball = silo_state[-1]
                if (team_ball_cnt >= 2) and (top_silo_ball == team_char):
                    silo_occupy_cnt += 1
            if (silo_occupy_cnt >= 3):
                return team_char
        return ""

    def is_terminal(self):
        if '.' not in self.state:
            return True
        if self.is_great_victory() != "":
            return True
        return False

    def evaluate(self):
        if self.is_great_victory() != "":
            score = 9999 if self.is_great_victory() == RED else -9999
            return score * (0.99 ** (self.state.count(RED) + self.state.count(BLUE)))

        score = self.state.count(RED) * 30 - self.state.count(BLUE) * 30

        if not self.is_terminal():
            silo_state_score_map = {
                "RRB": +0,
                "RR.": +5,
                "RBR": +10,
                "BRR": +10,
                "RRR": +10,
                "BBR": +0,
                "BB.": -5,
                "RBB": -10,
                "BRB": -10,
                "BBB": -10,
            }
            for silo in [self.state[i*3:i*3+3] for i in range(self.silos)]:
                if silo in silo_state_score_map.keys():
                    score += silo_state_score_map[silo]
        return score * (0.99 ** (self.state.count(RED) + self.state.count(BLUE)))

    def minimax(self, depth, team, parent_state=None, move_name=None, decision_map=None):
        if decision_map is None:
            decision_map = {}

        cache_key = (parent_state, depth, team)
        if cache_key in self.evaluation_cache:
            return self.evaluation_cache[cache_key]

        if depth == 0 or self.is_terminal():
            evaluation = self.evaluate()
            self.evaluation_cache[cache_key] = evaluation
            return evaluation

        best_value = -sys.maxsize if team == 'red' else sys.maxsize
        for move, move_team in self.get_moves():
            original_state = self.state
            self.state = self.make_move(move_team, move)
 
            value = self.minimax(depth - 1, team, self.state, move_name, decision_map)
            self.unmake_move(original_state)

            if team == 'red' and value > best_value or team == 'blue' and value < best_value:
                best_value = value
                decision_map[parent_state] = [move]
            elif value == best_value:
                if move not in decision_map[parent_state]:
                    decision_map[parent_state].append(move)
            
        
        self.evaluation_cache[cache_key] = best_value

        self.count += 1
        if self.count % 10000 == 0:
            print(f"No: {self.count}, State: {parent_state}, Best moves: {decision_map[parent_state] if parent_state in decision_map else None}, Best Value: {best_value}")

        return best_value

initial_state = None
silos_count = 5
game = Game(silos_count, initial_state=initial_state)
decision_map = {}
best_value = game.minimax(15, 'red', decision_map=decision_map)

with open('decision_map_classic.pkl', 'wb') as file:
    pickle.dump(decision_map, file)
