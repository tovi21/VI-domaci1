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
