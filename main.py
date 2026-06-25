import pygame
import sys
import math
from config import *
from ball import CueBall, ObjectBall
from table import Table
from cue import Cue

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Billiard 8-Ball Master - Week 2 Baseline")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 10, bold=True)
        self.reset_game_objects()

    def reset_game_objects(self):
        self.table = Table()
        self.cue_ball = CueBall(TABLE_X + 200, TABLE_Y + PLAY_HEIGHT // 2)
        self.balls = [self.cue_ball]
        
        self.cue = Cue(self.cue_ball)
        
        start_x = TABLE_X + 600
        start_y = TABLE_Y + PLAY_HEIGHT // 2
        
        colors = [YELLOW, BLUE, RED, PURPLE, ORANGE, GREEN, MAROON, BLACK, 
                  YELLOW, BLUE, RED, PURPLE, ORANGE, GREEN, MAROON]
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        
        ball_idx = 0
        rows = 5
        for col in range(rows):
            for row in range(col + 1):
                x = start_x + (col * (BALL_RADIUS * 2 + 1))
                y = start_y - (col * BALL_RADIUS) + (row * (BALL_RADIUS * 2 + 1))
                
                num = numbers[ball_idx]
                if num == 8: c = BLACK
                elif num <= 7: c = colors[num-1]
                else: c = colors[num-9]
                
                self.balls.append(ObjectBall(x, y, c, num))
                ball_idx += 1
                if ball_idx >= 15: break

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get_loop() if hasattr(pygame.event, 'get_loop') else pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            # Update stik
            self.cue.update(mouse_pos)
            
            # Update bola (gesekan/pergerakan, walau kecepatannya masih 0)
            for ball in self.balls:
                ball.update()
                ball.check_wall_collision(self.table.rect)

            # Render
            self.screen.fill(UI_BG)
            self.table.draw(self.screen)
            
            for ball in self.balls:
                ball.draw(self.screen, self.font)
                
            self.cue.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = GameManager()
    game.run()