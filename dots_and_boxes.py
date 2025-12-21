from copy import deepcopy

class DotsAndBoxes:

    def __init__(self, n):
        self.n = n
        self.A_score = 0
        self.B_score = 0
        self.state = {
            'board' : [['o' if j % 2 == 0 
                        else ' ' 
                        for j in range(n*2-1)] if i % 2 == 0
                       else [' ' for j in range(n*2-1)] 
                       for i in range(n*2-1)],
            'player' : 'A'
        }

    def print_state(self, state):
        for row in state['board']:
            print(' '.join(row))
        print('A score:', self.A_score)
        print('B score:', self.B_score)
        print()

    def get_actions(self, state):
        actions = []
        for i in range(self.n*2-1):
            for j in range(self.n*2-1):
                if i % 2 == 0:
                    if j % 2 != 0:
                        if state['board'][i][j] == ' ':
                            actions.append((i, j, state['player'], '-'))
                else:
                    if j % 2 == 0:
                        if state['board'][i][j] == ' ':
                            actions.append((i, j, state['player'], '|'))
        return actions
    
    def get_successor(self, state, action):
        new_state = deepcopy(state)
        i, j, player, line = action

        new_state['board'][i][j] = line

        # provjera da li je zatvorena kocka
        if line == '-':
            # gornja kocka
            if i-1 >= 0 and state['board'][i-2][j] == '-' and state['board'][i-1][j-1] == '|' and state['board'][i-1][j+1] == '|':
                new_state['board'][i-1][j] = state['player']
                if state['player'] == 'A':
                    self.A_score += 1
                else:
                    self.B_score += 1
            # donja kocka
            elif i+1 <= self.n-1 and state['board'][i+2][j] == '-' and state['board'][i+1][j-1] == '|' and state['board'][i+1][j+1] == '|':
                new_state['board'][i+1][j] = state['player']
                if state['player'] == 'A':
                    self.A_score += 1
                else:
                    self.B_score += 1
            else:
                new_state['player'] = 'B' if player == 'A' else 'A'
        elif line == '|':
            # lijeva kocka
            if j >= 0 and state['board'][i][j-2] == '|' and state['board'][i-1][j-1] == '-' and state['board'][i+1][j-1] == '-':
                new_state['board'][i][j-1] = state['player']
                if state['player'] == 'A':
                    self.A_score += 1
                else:
                    self.B_score += 1
            # desna kocka
            elif j <= self.n-1 and state['board'][i][j+2] == '|' and state['board'][i-1][j+1] == '-' and state['board'][i+1][j+1] == '-':
                new_state['board'][i][j+1] = state['player']
                if state['player'] == 'A':
                    self.A_score += 1
                else:
                    self.B_score += 1
            else:
                new_state['player'] = 'B' if player == 'A' else 'A'

        return new_state
    
