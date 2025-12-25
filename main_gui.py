from dots_and_boxes import DotsAndBoxes
from agents import ReflexAgent, RandomAgent, AlphaBetaAgent, HumanAgent
from gui import DotsGUI
import pygame
import time

def play_with_gui():
    # 1. Setup
    print("--- DOTS AND BOXES (GUI MODE) ---")
    rows = 15 # Možeš staviti input() ovdje ako želiš
    cols = 15
    
    game = DotsAndBoxes(rows, cols)
    gui = DotsGUI(game) # Pokrećemo prozor
    
    # 2. Agenti
    # (Za test, stavi sebe protiv AI-a)
    agent_a = HumanAgent(game)
    agent_b = AlphaBetaAgent(game)
    
    print(f"Mec: {type(agent_a).__name__} vs {type(agent_b).__name__}")

    last_action = None #
    
    # 3. Glavna Petlja
    while not game.game_over(game.state):
        
        gui.draw()
        pygame.event.pump() #  odrzava prozor zivim 
        
        curr_player = game.state['player']
        current_agent = agent_a if curr_player == 'A' else agent_b
        
        action = None
        
        # Ako je covjek na redu, koristimo GUI za klik
        if isinstance(current_agent, HumanAgent):
            action = gui.wait_for_click() # 
        else:
            # AI razmislja
            # (Malo pauze da ne bude prebrzo)
            time.sleep(0.5) 
            gui.draw() # ozvjezi ekran prije razmisljanja
            
            t0 = time.perf_counter()
            action = current_agent.decision(game.state)
            t1 = time.perf_counter()
            print(f"AI ({curr_player}) razmišljao: {t1-t0:.2f}s")
            
        # izvrsi potez
        if action:
            game.state = game.get_successor(game.state, action)
            gui.last_action = action
            print(f"Odigrano: {action}")
        
    # Kraj
    gui.draw()
    print("KRAJ IGRE!")
    time.sleep(5) # sacekaj da vidimo rezultat

if __name__ == "__main__":
    play_with_gui()