from dots_and_boxes import DotsAndBoxes
from agents import ReflexAgent, RandomAgent, AlphaBetaAgent, HumanAgent
import time

def get_agent_choice(player_name):
    print(f"\nIzaberi Agenta za igraca: {player_name}:")
    print("1. Human (Ti)")
    print("2. RandomAgent (Glup)")
    print("3. ReflexAgent (Pohlepan)")
    print("4. AlphaBetaAgent (Pametan)")
    
    while True:
        try:
            choice = int(input("Unos (1-4): "))
            if choice == 1: return HumanAgent
            if choice == 2: return RandomAgent
            if choice == 3: return ReflexAgent
            if choice == 4: return AlphaBetaAgent
        except ValueError:
            pass
        print("Pogresan unos. Probaj opet.")

def main():
    # --- 1. KONFIGURACIJA TABLE ---
    print("--- DOTS AND BOXES ARENA ---")
    try:
        rows = int(input("Unesi broj redova (N): "))
        cols = int(input("Unesi broj kolona (M): "))
    except ValueError:
        print("Greska. Koristim 2x2.")
        rows, cols = 2, 2

    game = DotsAndBoxes(rows, cols)

    # --- 2. IZBOR  ---
    AgentClassA = get_agent_choice("A (Prvi)")
    AgentClassB = get_agent_choice("B (Drugi)")

    agent_a = AgentClassA(game)
    agent_b = AgentClassB(game)

    print(f"\MEC POCINJE: {type(agent_a).__name__} (A) vs {type(agent_b).__name__} (B)")
    print("=" * 50)

    # --- 3. GLAVNA PETLJA ---
    while not game.game_over(game.state):
        
        # Prikaz stanja
        game.print_state(game.state)
        
        # Odredi ko je na redu
        curr_player_id = game.state['player']
        current_agent = agent_a if curr_player_id == 'A' else agent_b
        
        print(f"Na potezu: Igrac {curr_player_id} ({type(current_agent).__name__})")
        
        # Mjerenje vremena
        t0 = time.perf_counter()
        
        # --- ODLUKA ---
        action = current_agent.decision(game.state)
        
        t1 = time.perf_counter()
        elapsed = t1 - t0
        
        # Provjera da li je agent vratio None (predaja/bug)
        if action is None:
            print(f"CRITICAL: Agent {curr_player_id} nije vratio potez! Kraj igre.")
            break
            
        print(f"Odigrano: {action[0]} {action[1]} ({action[2]}) --- Vrijeme: {elapsed:.4f}s")
        print("-" * 30)
        
        game.state = game.get_successor(game.state, action)

    # --- 4. KRAJ IGRE ---
    print("\n" + "=" * 50)
    print("IGRA ZAVRSENA!")
    game.print_state(game.state)
    
    scores = game.state['scores']
    print(f"KONACAN SKOR -> A: {scores['A']} | B: {scores['B']}")
    
    if scores['A'] > scores['B']:
        print(f"POBJEDNIK: IGRAC A ({type(agent_a).__name__})")
    elif scores['B'] > scores['A']:
        print(f"POBJEDNIK: IGRAC B ({type(agent_b).__name__})")
    else:
        print("NERIJESENO!")

if __name__ == "__main__":
    main()