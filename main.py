from dots_and_boxes import DotsAndBoxes

n = int(input('Velicina tabele: '))
game = DotsAndBoxes(n)

state = game.state

game.print_state(state)