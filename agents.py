import random
import time

class Agent:
    def __init__(self, game):
        self.game = game

    
    def decision(self, state):
        pass # definise se za svakog agenta zasebno


    def game_loop(self):
        pass



class RandomAgent(Agent):
    def decision(self, state):
        actions = self.game.get_actions(state)
        if not actions: return None # jer prazna lista ,[] = False
        return random.choice(actions)


class ReflexAgent(Agent):
    # Pohlepni: 
    #   -> ako ima potez da zatvori kutiju igra ga 
    #   -> inace, kao radnom, igra nasumicno
    def decision(self, state):
        actions = self.game.get_actions(state)

        for action in actions:
            next_state = self.game.get_successor(state, action)

            # je li se povecao skor?
            player = state['player']
            current_score = state['scores'][player]
            new_score = next_state['scores'][player]

            if new_score > current_score:
                return action
        
        # inace bilo koji potez
        return random.choice(actions)
    


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-

class AlphaBetaAgent(Agent):
    
    def __init__(self, game):
        super().__init__(game)
        # vrijeme je limit pa nema max_depth
    

    def decision(self, state):
        start_time = time.time()

        board_size = len(state['board']) * len(state['board'][0]) # Broj polja u matrici
        
        self.transposition_table = {} 
        self.nodes_visited = 0
        self.tt_hits = 0
        self.transposition_table = {}

        safety_margin = 0.1
            
        time_limit = 10.0 - safety_margin


        best_move = None
        depth = 1

        # povecavamo dubinu dok imamo vremena
        while True:

            current_time = time.time()

            if current_time - start_time > time_limit:
                break

            try:
                # pokusaj da se nadje najbolje resenja na ovoj dubini
                move = self.alpha_beta_search(state, depth, start_time, time_limit)
                if move: # ako smo imali vremena zadrzimo za tu dubinu anjbolji potez
                    best_move = move
                
                # ako smo zavrsili pretragu do kraja igre ne moramo dalje
                if self.is_terminal_search:
                    break
            
            except TimeoutError: # kad istekne vrijeme msamo bacimo error i odma izlazimo iz duboke rekruzije
                print(f'Isteklo vrijeme na dubini {depth}') 
                print(f"Nodes: {self.nodes_visited}, TT Hits: {self.tt_hits}, Depth reached: {depth}")
                break

            depth += 1

        return best_move



    def order_moves(self, state, actions):

            good_moves = []
            normal_moves = []

            
            board = state['board']
            
            for action in actions:
                r, c, line = action
                makes_box = False
                
                if line == '-': # Horizontalna
                    #  gore
                    if r-2 >= 0:
                        if (board[r-2][c] == '-' and board[r-1][c-1] == '|' and board[r-1][c+1] == '|'):
                            makes_box = True
                    #  dolje
                    if not makes_box and r+2 < len(board):
                        if (board[r+2][c] == '-' and board[r+1][c-1] == '|' and board[r+1][c+1] == '|'):
                            makes_box = True
                            
                elif line == '|': # Vertikalna
                    #  lijevo
                    if c-2 >= 0:
                        if (board[r][c-2] == '|' and board[r-1][c-1] == '-' and board[r+1][c-1] == '-'):
                            makes_box = True
                    #  desno
                    if not makes_box and c+2 < len(board[0]):
                        if (board[r][c+2] == '|' and board[r-1][c+1] == '-' and board[r+1][c+1] == '-'):
                            makes_box = True
                
                if makes_box:
                    good_moves.append(action)
                else:
                    normal_moves.append(action)
                    
            random.shuffle(normal_moves)
            return good_moves + normal_moves


    def alpha_beta_search(self, state, depth, start_time, time_limit):
        
        alpha = float('-inf')
        beta = float('+inf')
        best_v = float('-inf')
        best_a = None

        self.is_terminal_search = False

        actions = self.game.get_actions(state)
        # mozda da se sortiraju akcije 
        actions = self.order_moves(state, actions)

        for a in actions:
            # provjeri vrijeme
            if time.time() - start_time > time_limit:
                raise TimeoutError
            
            new_state = self.game.get_successor(state, a)

            # !!bitno!!: ko je na potezu
            # ako sam ja (agent - A) opet na potezu zovemo max_value
            # inace zovemo min_value

            my_player = state['player']
            next_player = new_state['player']

            if next_player == my_player:
                # opet Agent sto znaci dodatni potez , to znaci:
                # -> dubina se ne smanjuje jer obicno dodatni potez ne kosta dubinu da bi vidjeli kraj lanca
                v = self.max_value(new_state, depth, alpha, beta, start_time, time_limit, my_player)
            else:
                v = self.min_value(new_state, depth - 1, alpha, beta, start_time, time_limit, my_player)

            if v > best_v:
                best_v = v
                best_a = a
            
            alpha = max(alpha, best_v)

        return best_a    
    


    def max_value(self, state, depth, alpha, beta, start_time, time_limit, my_player):
        self.nodes_visited += 1
        # Novo: provjera 'cacha'-a
        state_key = self.get_state_key(state)

        # kesiramo vrijednost koju smo vratili, ali to je validno samo ako nismo radili cutoff
        if state_key in self.transposition_table:
            entry = self.transposition_table[state_key]
            if entry['depth'] >= depth:
                self.tt_hits += 1
                return entry['value']

        # baza
        if self.game.game_over(state):
            self.is_terminal_search = True
            val = self.evaluate_state(state, my_player)
            # Keširaj i kraj!
            self.transposition_table[state_key] = {'value': val, 'depth': depth}
            return val
        
        if depth == 0:
            val = self.evaluate_state(state, my_player)
            self.transposition_table[state_key] = {'value': val, 'depth': depth}
            return val
        
        if time.time() - start_time > time_limit:
            raise TimeoutError
        

        v = float('-inf')
        actions = self.game.get_actions(state)
        actions = self.order_moves(state, actions)

        for a in actions:

            if time.time() - start_time > time_limit:
                raise TimeoutError
                        
            new_state = self.game.get_successor(state, a)
            next_player = new_state['player']


            # logika za dodatni potez
            if next_player == my_player:
                # opet zovi sebe i ne smanjuj dubinu
                v2 = self.max_value(new_state, depth, alpha, beta, start_time, time_limit, my_player)
            else:
                v2 = self.min_value(new_state, depth - 1, alpha, beta, start_time, time_limit, my_player)

            v = max(v, v2)

            if v >= beta:
                 # kesiranje prije izlaska (ovo je donja granica, ali cuvamo je)
                self.transposition_table[state_key] = {'value': v, 'depth': depth}
                return v
            
            alpha = max(alpha, v)

        self.transposition_table[state_key] = {'value': v, 'depth': depth}
        return v
    



    def min_value(self, state, depth, alpha, beta, start_time, time_limit, my_player):
        self.nodes_visited += 1



        # --- Kesiranje ---
        state_key = self.get_state_key(state)
        
        if state_key in self.transposition_table:
            entry = self.transposition_table[state_key]
            if entry['depth'] >= depth:
                self.tt_hits += 1
                return entry['value']

        if self.game.game_over(state):
            self.is_terminal_search = True
            val = self.evaluate_state(state, my_player)
            self.transposition_table[state_key] = {'value': val, 'depth': depth}
            return val
        
        if depth == 0:
            val = self.evaluate_state(state, my_player)
            self.transposition_table[state_key] = {'value': val, 'depth': depth}
            return val
        
        if time.time() - start_time > time_limit:
            raise TimeoutError
        

        v = float('+inf')
        actions = self.game.get_actions(state)
        actions = self.order_moves(state, actions)

        for a in actions:
            
            if time.time() - start_time > time_limit:
                raise TimeoutError

            new_state = self.game.get_successor(state, a)
            next_player = new_state['player']

            # 'my_player' je i dalje Agent(A) ali je trenutno na potezu B
            # ako sam ja 'min_value' znaci da je trenutno na potezu protivnik
            # ako je nexxt_player != my_player onda igra protivnik

            if next_player != my_player: # dodatni potez za protivnika 
                # analogno, zove se min i ne smannjuje se dubina
                v2 = self.min_value(new_state, depth, alpha, beta, start_time, time_limit, my_player)
            else:
                v2 = self.max_value(new_state, depth, alpha, beta, start_time, time_limit, my_player)
        
            v = min(v, v2)

            if v <= alpha:
                self.transposition_table[state_key] = {'value': v, 'depth': depth}
                return v
            
            beta = min(beta, v)
    
        self.transposition_table[state_key] = {'value': v, 'depth': depth}
        return v
    


    def evaluate_state(self, state, my_player):

        my_score = state['scores'][my_player]

        opponent = 'B' if my_player == 'A' else 'A'
        opp_score = state['scores'][opponent]

        base_score = my_score - opp_score

        # ako je kraj igre dodajemo ogroman bonus za pobjedu
        if self.game.game_over(state):
            if my_score > opp_score: return 1000 + base_score
            elif opp_score > my_score: return -1000 + base_score
            else: return 0 # remi
        

        # Lanci i 3 strane kutije
        # -> moramo brojati koliko ima kutija sa 3 zatvorene stranice (to su ziceri), i koliko je lanaca (zatvoren sa dvije)

        threes = 0
        twos = 0

        # prolazimo sve kutije 
        board = state['board']
        # (kutije su sa neparnim indeksima ) 

        for r in range(1, len(board),2):
            for c in range(1, len(board[0]),2):

                if board[r][c] != ' ' : continue

                # brojimo zidove oko trnutne kutije
                walls = 0
                if board[r-1][c] == '-' : walls +=1
                if board[r+1][c] == '-' : walls +=1
                if board[r][c-1] == '|' : walls +=1
                if board[r][c+1] == '|' : walls +=1

                if walls == 3: threes += 1
                if walls == 2: twos += 1

        
        # formula: 
        # -> ako sam ja(agent) na potezu, 'three' su moju poeni i uzimamo ih
        # -> ako je protivnik na potezu, 'three' su njegovi poeni (uzece ih)

        current_player = state['player']

        if current_player == my_player:
            heuristic = base_score*10 + threes*5 + twos*1
        else:
             heuristic = base_score*10 - threes*5 - twos*1

        # base_score su najvredniji
        # threes: kutije sa 3 zida su skoro poeni, ko je na potezu ih dobija
        # twos: samo potencial
        # -> poenta: ako ostavimo protivniku tabelu punu trojki izgibili smo jer ce hruristika biti veoma negativna

        return heuristic
    


    # Pokusaj optimizacije
    #  i) scena 1
    #   -> ja povucem gornju liniju (stanja A)
    #   -> protivnik povuce donju (sad smo u stanje B)
    # ii) scena 2
    #   -> protivnik povuce gornju (stanje C)
    #   -> ja povucem donju (stanje D)
    # 
    # +--> B i D su ista stanja, tabela bi izgeladal isto a minimax posto to ne zna bi oba stabla trazio nezavisno
    #
    # Resenje: napravimo recnik sa stanjima i vrijednostima 
    # -> problems to smo do sad radili stanja da su lista listi sto ne moze biti kljuc u recniku
    #   +-> pretvorimo ih u torku torki
    
    def get_state_key(self, state):
        board = state['board']

        board_tuple = tuple(tuple(row) for row in board)

        # sad dodamo informaicju o igracu, jer stanje nije isto ako ja na redu A ili B
        key = (board_tuple, state['player'])

        return key
    
    


# Da mozemo da igramo protiv njega

class HumanAgent(Agent):

    
    def decision(self, state):
        
        print("Tvoj potez (red kolona): ")
        while True:
            try:
                user_input = input().split()
                if not user_input: continue
                r, c = int(user_input[0]), int(user_input[1])
                
                # Validacija
                possible_moves = self.game.get_actions(state)
                for move in possible_moves:
                    if move[0] == r and move[1] == c:
                        return move # Vrati validan potez
                
                print("!!! NEVALIDAN POTEZ. Probaj opet.")
            except:
                print("!!! GRESKA. Unesi dva broja.")