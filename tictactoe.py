import pygame as pg
import sys
from random import randint




window_size = 900
size_of_cell = window_size // 3
inf = float('inf')
vec2 = pg.math.Vector2
center_of_cell = vec2(size_of_cell / 2)


class TicTacToe:
    def __init__(self, game):
        self.game = game
        self.field_image = self.get_scaled_image(path='Assets/field.png', res=[window_size] * 2)
        self.O_image = self.get_scaled_image(path='Assets/o.png', res=[size_of_cell] * 2)
        self.X_image = self.get_scaled_image(path='Assets/x.png', res=[size_of_cell] * 2)

        self.game_array = [[inf, inf, inf],
                           [inf, inf, inf],
                           [inf, inf, inf]]
        
        self.player = randint(0, 1)

        self.line_indices_array = [[(0, 0), (0, 1), (0, 2)],
                                   [(1, 0), (1, 1), (1, 2)],
                                   [(2, 0), (2, 1), (2, 2)],
                                   [(0, 0), (1, 0), (2, 0)],
                                   [(0, 1), (1, 1), (2, 1)],
                                   [(0, 2), (1, 2), (2, 2)],
                                   [(0, 0), (1, 1), (2, 2)],
                                   [(0, 2), (1, 1), (2, 0)]]
        self.winner = None
        self.game_steps = 0
        self.font = pg.font.SysFont('Arial', size_of_cell // 4, True)

    def check_winner(self):
        for line_indices in self.line_indices_array:
            sum_line = sum([self.game_array[i][j] for i, j in line_indices])
            if sum_line in {0, 3}:
                self.winner = 'XO'[sum_line == 0]
                self.winner_line = [vec2(line_indices[0][::-1]) * size_of_cell + center_of_cell,
                                    vec2(line_indices[2][::-1]) * size_of_cell + center_of_cell]

    def run_game_process(self):
        current_cell = vec2(pg.mouse.get_pos()) // size_of_cell
        col, row = map(int, current_cell)
        left_click = pg.mouse.get_pressed()[0]

        if left_click and self.game_array[row][col] == inf and not self.winner:
            self.game_array[row][col] = self.player
            self.player = not self.player
            self.game_steps += 1
            self.check_winner()

    def draw_objects(self):
        for y, row in enumerate(self.game_array):
            for x, obj in enumerate(row):
                if obj != inf:
                    self.game.screen.blit(self.X_image if obj else self.O_image, vec2(x, y) * size_of_cell)

    def draw_winner(self):
        if self.winner:
            pg.draw.line(self.game.screen, 'red', *self.winner_line, size_of_cell // 8)
            label = self.font.render(f"{self.winner} won !", True, "white ", "pink")
            self.game.screen.blit(label, (window_size // 2 - label.get_width() // 2, window_size // 4))

        elif self.game_steps == 9:
            label = self.font.render("Tie", True, "red", "pink")
            self.game.screen.blit(label, (window_size // 2 - label.get_width() // 2, window_size // 4))

    def draw(self):
        self.game.screen.blit(self.field_image, (0, 0))
        self.draw_objects()
        self.draw_winner()

    @staticmethod
    def get_scaled_image(path, res):
        img = pg.image.load(path)
        return pg.transform.smoothscale(img, res)

    def print_caption(self):
   
        pg.display.set_caption(f"{'OX'[self.player]} turn")

        if self.winner or self.game_steps == 9:
            pg.display.set_caption("Game Over !")
    

    def run(self):
        self.print_caption()
        self.draw()
        self.run_game_process()


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([window_size] * 2)
        self.clock = pg.time.Clock()
        self.tic_tac_toe = TicTacToe(self)

    def new_game(self):
        self.tic_tac_toe = TicTacToe(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
       
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
              
    def run(self):
        while True:

            self.tic_tac_toe.run()
            self.check_events()
            pg.display.update()
            self.clock.tick(60)





if __name__ == '__main__':
    game = Game()
    game.run()
