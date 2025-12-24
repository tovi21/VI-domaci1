import pygame
import sys
import time

# --- KONSTANTE ZA BOJE ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 100, 100)
BLUE  = (100, 100, 255)
GREY  = (220, 220, 220)       # Za Hover
GREEN = (0, 180, 0)           # Za Zadnji potez
DOT_COLOR = (50, 50, 50)

class DotsGUI:
    def __init__(self, game, width=600, height=600):
        pygame.init()
        self.game = game
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Dots and Boxes - AI Arena")
        self.font = pygame.font.SysFont("Arial", 32)
        
        self.n_dots_rows = game.rows + 1
        self.n_dots_cols = game.cols + 1
        self.padding = 100 
        
        available_w = width - 2 * self.padding
        available_h = height - 2 * self.padding
        self.spacing_x = available_w // (self.n_dots_cols - 1)
        self.spacing_y = available_h // (self.n_dots_rows - 1)

        self.last_action = None #
        
    def get_coords(self, r_dot, c_dot):
        x = self.padding + c_dot * self.spacing_x
        y = self.padding + r_dot * self.spacing_y
        return x, y

    def draw_line_by_coords(self, r, c, color):
            """Pomocna funkcija koja crta liniju na osnovu r, c iz matrice."""
            
            # Horizontalna: r paran, c neparan
            if r % 2 == 0: 
                dot_r = r // 2
                dot_c_left = (c - 1) // 2
                
                # PROVJERA GRANICA (za svaki slucaj)
                if dot_c_left + 1 >= self.n_dots_cols: return

                x1, y1 = self.get_coords(dot_r, dot_c_left)
                x2, y2 = self.get_coords(dot_r, dot_c_left + 1)
                pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), 6)
                
            # Vertikalna: r neparan, c paran
            else:
                dot_r_top = (r - 1) // 2
                dot_c = c // 2
                
                if dot_r_top + 1 >= self.n_dots_rows: return

                x1, y1 = self.get_coords(dot_r_top, dot_c)
                x2, y2 = self.get_coords(dot_r_top + 1, dot_c)
                pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), 6)

    def draw(self):
        self.screen.fill(WHITE)
        board = self.game.state['board']
        r_dim = len(board)
        c_dim = len(board[0])
        
        # 1. KUTIJE
        for r in range(1, r_dim, 2):
            for c in range(1, c_dim, 2):
                owner = board[r][c]
                if owner != ' ':
                    dot_r = (r - 1) // 2
                    dot_c = (c - 1) // 2
                    x, y = self.get_coords(dot_r, dot_c)
                    color = RED if owner == 'A' else BLUE
                    rect = (x + 5, y + 5, self.spacing_x - 10, self.spacing_y - 10)
                    pygame.draw.rect(self.screen, color, rect)

        # 2. LINIJE (Postojeće)
        for r in range(r_dim):
            for c in range(c_dim):
                cell = board[r][c]
                
                # Crtaj SAMO ako je eksplicitno linija
                if cell == '-' or cell == '|':
                    
                    color = BLACK
                    if self.last_action and r == self.last_action[0] and c == self.last_action[1]:
                        color = GREEN
                    
                    self.draw_line_by_coords(r, c, color)

        # 3. HOVER EFEKT (Sjenka)
        # Uzimamo poziciju miša
        mx, my = pygame.mouse.get_pos()
        potential_move = self.get_clicked_line((mx, my))
        
        if potential_move:
            pr, pc = potential_move
            # Crtamo sivo samo ako je linija prazna
            if board[pr][pc] == ' ':
                self.draw_line_by_coords(pr, pc, GREY)

        # 4. TACKE
        for r in range(self.n_dots_rows):
            for c in range(self.n_dots_cols):
                x, y = self.get_coords(r, c)
                pygame.draw.circle(self.screen, DOT_COLOR, (x, y), 8)

        # 5. SKOR
        scores = self.game.state['scores']
        text = f"A: {scores['A']}   B: {scores['B']}"
        img = self.font.render(text, True, BLACK)
        self.screen.blit(img, (self.width//2 - 50, 20))
        
        curr = self.game.state['player']
        col = RED if curr == 'A' else BLUE
        turn_text = f"Na potezu: {curr}"
        img2 = self.font.render(turn_text, True, col)
        self.screen.blit(img2, (self.width//2 - 60, self.height - 50))

        pygame.display.flip()


    def get_clicked_line(self, pos):
        """Pretvara (x, y) miša u (r, c) poteza."""
        mx, my = pos
        
        # 1. Nađi najbližu tačku
        # (Obrnuta formula od get_coords)
        if self.spacing_x == 0 or self.spacing_y == 0: return None
        
        c_dot = round((mx - self.padding) / self.spacing_x)
        r_dot = round((my - self.padding) / self.spacing_y)
        
        # Ograniči da ne izađemo van table
        c_dot = max(0, min(c_dot, self.n_dots_cols - 1))
        r_dot = max(0, min(r_dot, self.n_dots_rows - 1))
        
        # Koordinate te tačke
        dx, dy = self.get_coords(r_dot, c_dot)
        
        # 2. Odredi smjer klika (Gore, Dolje, Lijevo, Desno)
        diff_x = mx - dx
        diff_y = my - dy
        
        # Zona mrtvog ugla (da ne kliknemo tačno na tačku)
        if abs(diff_x) + abs(diff_y) < 15: return None 
        
        move = None
        
        # Da li je klik horizontalan ili vertikalan?
        if abs(diff_x) > abs(diff_y): 
            # Horizontalno (Lijevo ili Desno)
            if diff_x > 0: # Desno
                # Linija desno od tačke (r, c)
                # U matrici: red = 2*r, kolona = 2*c + 1
                if c_dot < self.n_dots_cols - 1:
                    move = (2 * r_dot, 2 * c_dot + 1)
            else: # Lijevo
                # Linija lijevo od tačke (r, c) -> isto što i desno od (r, c-1)
                if c_dot > 0:
                    move = (2 * r_dot, 2 * (c_dot - 1) + 1)
        else:
            # Vertikalno (Gore ili Dolje)
            if diff_y > 0: # Dolje
                # Linija ispod tačke (r, c)
                # U matrici: red = 2*r + 1, kolona = 2*c
                if r_dot < self.n_dots_rows - 1:
                    move = (2 * r_dot + 1, 2 * c_dot)
            else: # Gore
                if r_dot > 0:
                    move = (2 * (r_dot - 1) + 1, 2 * c_dot)
                    
        return move

    def wait_for_click(self):
        """Petlja koja čeka dok čovjek ne klikne validan potez."""
        while True:
            # Obrada događaja (da se prozor ne zamrzne)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Lijevi klik
                        move = self.get_clicked_line(event.pos)
                        
                        # Ako smo kliknuli na liniju, provjeri jel validna (prazna)
                        if move:
                            r, c = move
                            board = self.game.state['board']
                            # Provjera granica za svaki slučaj
                            if 0 <= r < len(board) and 0 <= c < len(board[0]):
                                if board[r][c] == ' ':
                                    # Dodaj treći element (tip linije)
                                    # Ako je red paran -> '-', ako je neparan -> '|'
                                    line_type = '-' if r % 2 == 0 else '|'
                                    return (r, c, line_type)
            
            # Crtaj stalno dok čekamo (zbog hover efekta)
            # Ovdje ne znamo last_action iz main-a, pa šaljemo None.
            # (Hover će raditi, ali zelena linija zadnjeg poteza će možda treperiti ili nestati
            # dok čovjek razmišlja, osim ako ne proslijedimo last_action i u ovu funkciju.
            # Za sad je ok i bez toga).
            self.draw() 
            time.sleep(0.02)