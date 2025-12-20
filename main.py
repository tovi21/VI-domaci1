import random
from dots_and_boxes import DotsAndBoxes

n = int(input('Velicina tabele: '))
game = DotsAndBoxes(n)

state = game.state

# game.print_state(state)
# print(game.get_actions(state))

# action = random.choice(game.get_actions(state))
# print(action)
# new_state = game.get_successor(state, action)
# game.print_state(new_state)

# action1 = random.choice(game.get_actions(new_state))
# print(action1)
# new_state1 = game.get_successor(new_state, action1)
# game.print_state(new_state1)

# action2 = random.choice(game.get_actions(new_state1))
# print(action2)
# new_state2 = game.get_successor(new_state1, action2)
# game.print_state(new_state2)

# action3 = random.choice(game.get_actions(new_state2))
# print(action3)
# new_state3 = game.get_successor(new_state2, action3)
# game.print_state(new_state3)