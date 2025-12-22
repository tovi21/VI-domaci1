from dots_and_boxes import DotsAndBoxes
from agents import ReflexAgent, RandomAgent

def main():
    # 1. Postavka Igre
    try:
        rows = int(input("Unesi broj redova (N): "))
        cols = int(input("Unesi broj kolona (M): "))
    except ValueError:
        print("Koristim podrazumijevano 2x2.")
        rows, cols = 2, 2
        
    game = DotsAndBoxes(rows, cols)
    
    # 2. Izbor Agenta
    agent = RandomAgent(game)
    
    print(f"\n--- IGRAS PROTIV {type(agent).__name__} ---")
    print("Ti si igrac 'B'. Agent je igrac 'A'.")
    print("Koordinate unosis kao: red kolona (npr. '0 1')")
    
    
    while not game.game_over(game.state):
        
        # Prikazi stanje
        game.print_state(game.state)
        curr_player = game.state['player']
        
        if curr_player == 'A':
            # --- POTEZ AGENTA ---
            print(f"Agent ({type(agent).__name__}) razmislja...")
            import time
            t0 = time.perf_counter()
            
            action = agent.decision(game.state)
            
            t1 = time.perf_counter()
            print(f"Agent odigrao: {action} (Vrijeme: {t1-t0:.4f}s)")
            
            if action is None:
                print("Agent nema poteza! (Ovo ne bi smjelo da se desi)")
                break
                
            game.state = game.get_successor(game.state, action)
            
        else:
            # --- POTEZ COVJEKA (B) ---
            print("Tvoj potez (red kolona): ")
            try:
                user_input = input().split()
                if not user_input: continue
                
                r, c = int(user_input[0]), int(user_input[1])
                
                # Validacija i pretvaranje (r, c) -> (r, c, line_type)
                possible_moves = game.get_actions(game.state)
                move_to_play = None
                
                for move in possible_moves:
                    if move[0] == r and move[1] == c:
                        move_to_play = move
                        break
                
                if move_to_play:
                    game.state = game.get_successor(game.state, move_to_play)
                else:
                    print("!!! NEVALIDAN POTEZ. Zauzeto ili nemoguce")
                    
            except (ValueError, IndexError):
                print("!!! GRESKA. Unesi dva broja.")

    # 4. KRAJ
    game.print_state(game.state)
    print("--- IGRA GOTOVA ---")
    scores = game.state['scores']
    
    if scores['A'] > scores['B']:
        print(f"Pobjednik je AGENT ({scores['A']} : {scores['B']})")
    elif scores['B'] > scores['A']:
        print(f"Pobjednik si TI ({scores['B']} : {scores['A']})")
    else:
        print(f"NERIJESENO ({scores['A']} : {scores['A']})")

if __name__ == "__main__":
    main()