from copy import deepcopy

class DotsAndBoxes:

    def __init__(self, n, m=None):
        # Podrska za MxN (ako je m None, onda je kvadratna NxN)
        self.rows = n
        self.cols = m if m is not None else n
        
        # Matrica table:
        # Redovi su 2*rows + 1, Kolone su 2*cols + 1
        r_dim = 2 * self.rows + 1
        c_dim = 2 * self.cols + 1
        
        board = [[' ' for _ in range(c_dim)] for _ in range(r_dim)]
        
        # Postavljanje tacaka 'o'
        for i in range(0, r_dim, 2):
            for j in range(0, c_dim, 2):
                board[i][j] = '•'

        self.state = {
            'board': board,
            'player': 'A',
            'scores': {'A': 0, 'B': 0}, # Skorovi su dio stanja
            'boxes_closed': 0 # Brojac zatvorenih kutija (za kraj igre)
        }

        self.total_boxes = self.rows * self.cols




    def print_state(self, state):
        
        header = "   " + "".join([f"{x:2} " for x in range(len(state['board'][0]))])
        print(header)
        
        for i, row in enumerate(state['board']):
            row_str = ""
            for cell in row:
                row_str += f"{cell:2} " # svaka celija zauzima 2 karaktera + razmak
            print(f"{i:2} {row_str}")
        
        print(f"Score - A: {state['scores']['A']}, B: {state['scores']['B']}")
        print(f"Player on move: {state['player']}")
        print()




    def get_actions(self, state):
        actions = []
        r_dim = len(state['board'])
        c_dim = len(state['board'][0])
        
        for r in range(r_dim):
            for c in range(c_dim):
                # Horizontalne linije: r je parno, c je neparno
                if r % 2 == 0 and c % 2 != 0:
                    if state['board'][r][c] == ' ':
                        actions.append((r, c, '-'))
                # Vertikalne linije: r je neparno, c je parno
                elif r % 2 != 0 and c % 2 == 0:
                    if state['board'][r][c] == ' ':
                        actions.append((r, c, '|'))
        return actions
    


    
    def get_successor(self, state, action):
        new_state = deepcopy(state)
        r, c, line = action
        player = state['player']
        
        # 1. Postavi liniju
        new_state['board'][r][c] = line
        
        # 2. Provjeri da li je zatvorena kutija
        box_made = False
        
        if line == '-': # Horizontalna linija
            # Provjeri GORNJU kutiju
            if r - 2 >= 0:
                # Gledamo: liniju iznad (r-2), lijevo (r-1, c-1), desno (r-1, c+1)
                if (new_state['board'][r-2][c] == '-' and 
                    new_state['board'][r-1][c-1] == '|' and 
                    new_state['board'][r-1][c+1] == '|'):
                    
                    new_state['scores'][player] += 1
                    new_state['boxes_closed'] += 1
                    # Oznacimo kutiju (centar je r-1, c)
                    new_state['board'][r-1][c] = player
                    box_made = True
            
            # Provjeri DONJU kutiju
            if r + 2 < len(new_state['board']):
                if (new_state['board'][r+2][c] == '-' and 
                    new_state['board'][r+1][c-1] == '|' and 
                    new_state['board'][r+1][c+1] == '|'):
                    
                    new_state['scores'][player] += 1
                    new_state['boxes_closed'] += 1
                    new_state['board'][r+1][c] = player
                    box_made = True

        elif line == '|': # Vertikalna linija
            # Provjeri LIJEVU kutiju
            if c - 2 >= 0:
                if (new_state['board'][r][c-2] == '|' and 
                    new_state['board'][r-1][c-1] == '-' and 
                    new_state['board'][r+1][c-1] == '-'):
                    
                    new_state['scores'][player] += 1
                    new_state['boxes_closed'] += 1
                    new_state['board'][r][c-1] = player
                    box_made = True
            
            # Provjeri DESNU kutiju
            if c + 2 < len(new_state['board'][0]):
                if (new_state['board'][r][c+2] == '|' and 
                    new_state['board'][r-1][c+1] == '-' and 
                    new_state['board'][r+1][c+1] == '-'):
                    
                    new_state['scores'][player] += 1
                    new_state['boxes_closed'] += 1
                    new_state['board'][r][c+1] = player
                    box_made = True

        # 3. Promjena igraca (samo ako NIJE napravljena kutija)
        if not box_made:
            new_state['player'] = 'B' if player == 'A' else 'A'
            
        return new_state




    def game_over(self, state):
        return state['boxes_closed'] == self.total_boxes