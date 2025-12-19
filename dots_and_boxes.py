

class DotsAndBoxes:

    def __init__(self, n):
        self.n = n
        self.state = {
            'board' : [['o' if j % 2 == 0 
                        else ' ' 
                        for j in range(n*2)] if i % 2 == 0
                       else [' ' for j in range(n*2)] 
                       for i in range(n*2)],
            'player' : 'A'
        }

    def print_state(self, state):
        for row in state['board']:
            print(' '.join(row))
        print()