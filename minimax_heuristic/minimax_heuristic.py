import sys
import pickle

class Game:
    def __init__(self, silos=5, initial_state=None):
        self.silos = silos
        self.state = initial_state if initial_state else '.' * (self.silos * 3)
        self.evaluation_cache = {}
        self.max_depth = 15
        self.depth_trigger = 12
        self.count = 0

    def get_moves(self):
        red_moves = [(i, 'red') for i in range(self.silos) if self.state[i*3:i*3+3].count('.') > 0]
        blue_moves = [(i, 'blue') for i in range(self.silos) if self.state[i*3:i*3+3].count('.') > 0]
        return red_moves + blue_moves

    def make_move(self, team, move):
        pos = self.state[move*3:move*3+3].index('.')
        new_state = list(self.state)
        new_state[move*3+pos] = 'R' if team == 'red' else 'B'
        return ''.join(new_state)

    def unmake_move(self, original_state):
        self.state = original_state

    def is_terminal(self):
        if '.' not in self.state:
            return True
        for team_char in ['R', 'B']:
            if sum(sub.count(team_char) == 2 and sub[0] == team_char for sub in [self.state[i*3:i*3+3] for i in range(self.silos)]) >= 3:
                return True
        return False

    def evaluate(self, team):
        score = self.state.count('R') * 30 if team == 'red' else self.state.count('B') * 30

        for team_char in ['R', 'B']:
            for sub in [self.state[i*3:i*3+3] for i in range(self.silos)]:
                if sub.count(team_char) == 2 and sub.count('R') >= 1:
                    score += 10
                if sub.count(team_char) == 2 and sub.count('B') >= 1:
                    score -= 10
        return score

    def heuristic_search(self, depth, team):
        best_moves = []
        best_score = -sys.maxsize if team == 'red' else sys.maxsize
        
        for move, move_team in self.get_moves():
            original_state = self.state
            self.state = self.make_move(move_team, move)
            score = self.heuristic_evaluation(team)
            
            if (team == 'red' and score > best_score) or (team == 'blue' and score < best_score):
                best_moves = [move]
                best_score = score
            elif score == best_score:
                best_moves.append(move)
                
            self.unmake_move(original_state)
        
        return best_moves, best_score
    
    def heuristic_evaluation(self, team):
        score = self.state.count('R') * 30 if team == 'red' else self.state.count('B') * 30

        # can add more heuristic evaluations here
        # if self.state[0] == 'R':
        #     score += 12345678 # debug

        for team_char in ['R', 'B']:
            for sub in [self.state[i*3:i*3+3] for i in range(self.silos)]:
                if sub.count(team_char) == 2 and sub.count('R') >= 1:
                    score += 1000
                if sub.count(team_char) == 2 and sub.count('B') >= 1:
                    score -= 1000
        return score

    def minimax(self, depth, team, parent_state=None, move_name=None, decision_map=None):
        if decision_map is None:
            decision_map = {}

        cache_key = (parent_state, depth, team)
        if cache_key in self.evaluation_cache:
            return self.evaluation_cache[cache_key], decision_map.get(parent_state, [])

        if depth == 0 or self.is_terminal():
            evaluation = self.evaluate(team)
            self.evaluation_cache[cache_key] = evaluation
            return evaluation, []

        if depth <= self.max_depth - self.depth_trigger:
            heuristic_moves, heuristic_score = self.heuristic_search(depth, team)
            for move in heuristic_moves:
                if parent_state not in decision_map:
                    decision_map[parent_state] = []
                decision_map[parent_state].append(move)

        best_value = -sys.maxsize if team == 'red' else sys.maxsize
        best_moves = []
        for move, move_team in self.get_moves():
            original_state = self.state
            self.state = self.make_move(move_team, move)
            
            value, _ = self.minimax(depth - 1, team, self.state, move_name, decision_map)
            self.unmake_move(original_state)
            
            if (team == 'red' and value > best_value) or (team == 'blue' and value < best_value):
                best_value = value
                best_moves = [move]
            elif value == best_value:
                best_moves.append(move)

        self.evaluation_cache[cache_key] = best_value
        decision_map[parent_state] = best_moves

        self.count += 1
        print(f"No: {self.count}, State: {parent_state}, Best moves: {decision_map[parent_state] if parent_state in decision_map else None}, Best Value: {best_value}")
        
        return best_value, best_moves

initial_state = None
silos_count = 5
game = Game(silos_count, initial_state=initial_state)
decision_map = {}
best_value, best_moves = game.minimax(15, 'red', decision_map=decision_map)

with open('decision_map_heuristic.pkl', 'wb') as file:
    pickle.dump(decision_map, file)