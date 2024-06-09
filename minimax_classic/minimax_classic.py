import sys
import pickle

class Game:
    def __init__(self, silos=5, initial_state=None):
        self.silos = silos
        self.state = initial_state if initial_state else '.' * (self.silos * 3)
        self.evaluation_cache = {}
        self.count = 0

    def get_moves(self):
        moves = []
        for i in range(self.silos):
            if '.' in self.state[i*3:i*3+3]:
                moves.append((i, 'red'))
                moves.append((i, 'blue'))
        return moves

    def make_move(self, team, move):
        pos = self.state[move*3:move*3+3].index('.')
        new_state = list(self.state)
        new_state[move*3 + pos] = 'R' if team == 'red' else 'B'
        return ''.join(new_state)

    def unmake_move(self, original_state):
        self.state = original_state

    def is_terminal(self):
        if '.' not in self.state:
            return True
        for team_char in ['R', 'B']:
            for i in range(self.silos):
                sub = self.state[i*3:i*3+3]
                if sub.count(team_char) == 2 and sub[0] == team_char:
                    if self.state.count(team_char) >= 3:
                        return True
        return False

    def evaluate(self, team):
        score = self.state.count('R') * 30 if team == 'red' else self.state.count('B') * 30
        return score

    def minimax(self, depth, team, parent_state=None, decision_map=None):
        if decision_map is None:
            decision_map = {}

        cache_key = (parent_state, depth, team)
        if cache_key in self.evaluation_cache:
            return self.evaluation_cache[cache_key]

        if depth == 0 or self.is_terminal():
            evaluation = self.evaluate(team)
            self.evaluation_cache[cache_key] = evaluation
            return evaluation

        best_value = -sys.maxsize if team == 'red' else sys.maxsize
        for move, move_team in self.get_moves():
            original_state = self.state
            self.state = self.make_move(move_team, move)
 
            value = self.minimax(depth - 1, team, self.state, decision_map)
            self.unmake_move(original_state)

            if (team == 'red' and value > best_value) or (team == 'blue' and value < best_value):
                best_value = value
                decision_map[parent_state] = [move]
            elif value == best_value:
                decision_map[parent_state].append(move)
            
        self.evaluation_cache[cache_key] = best_value

        self.count += 1
        print(f"No: {self.count}, State: {parent_state}, Best moves: {decision_map[parent_state] if parent_state in decision_map else None}, Best Value: {best_value}")

        return best_value

initial_state = None
silos_count = 5
game = Game(silos_count, initial_state=initial_state)
decision_map = {}
best_value = game.minimax(15, 'red', decision_map=decision_map)

with open('decision_map_origin.pkl', 'wb') as file:
    pickle.dump(decision_map, file)
