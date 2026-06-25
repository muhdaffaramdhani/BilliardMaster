import pygame
import sys
import math
from config import *
from ball import CueBall, ObjectBall
from table import Table
from cue import Cue
from physics import PhysicsEngine

def get_custom_font(size, bold=False, italic=False):
    font_names = ['Segoe UI', 'Trebuchet MS', 'Arial']
    for name in font_names:
        font_path = pygame.font.match_font(name, bold=bold, italic=italic)
        if font_path:
            try:
                return pygame.font.Font(font_path, size)
            except Exception:
                continue
    return pygame.font.SysFont('Arial', size, bold=bold, italic=italic)

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Billiard 8-Ball Master - Week 4 Cue Stick Mechanics")
        self.clock = pygame.time.Clock()
        self.font = get_custom_font(12, bold=True)
        self.reset_game_objects()

    def reset_game_objects(self):
        self.table = Table()
        self.cue_ball = CueBall(TABLE_X + 200, TABLE_Y + PLAY_HEIGHT // 2)
        self.balls = [self.cue_ball]
        
        self.cue = Cue(self.cue_ball)
        self.cue.sensitivity = 1.0  # default sensitivity
        
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
                
        self.is_moving = False

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get_loop() if hasattr(pygame.event, 'get_loop') else pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                
                if not self.is_moving:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            # Left click handles cue stick aiming/power/shoot states
                            if self.cue.handle_click():
                                self.is_moving = True
                        elif event.button == 3:
                            # Right click cancels shot
                            self.cue.cancel_shot()

            # Update stik hanya jika bola diam
            if not self.is_moving:
                self.cue.update(mouse_pos)
            
            # Physics sub-steps (10 sub-steps per frame)
            physics_steps = 10
            for step in range(physics_steps):
                for ball in self.balls:
                    if not ball.potted:
                        ball.pos += ball.velocity / physics_steps
                        ball.check_wall_collision(self.table.rect)
                        ball.check_pocket_collision(self.table.pockets)
                
                # Resolusi tumbukan antar bola
                for i in range(len(self.balls)):
                    for j in range(i + 1, len(self.balls)):
                        PhysicsEngine.resolve_collision(self.balls[i], self.balls[j])
            
            # Gesekan dan deteksi apakah bola masih bergerak
            moving_count = 0
            for ball in self.balls:
                if ball.potted: continue
                if ball.velocity.length() > 0.05:
                    ball.velocity *= ball.friction
                    moving_count += 1
                else:
                    ball.velocity = pygame.math.Vector2(0, 0)

            # Transisi dari bergerak ke diam
            if self.is_moving and moving_count == 0:
                self.is_moving = False
                self.cue.state = 0

            # Render
            self.screen.fill(UI_BG)
            self.table.draw(self.screen)
            
            for ball in self.balls:
                ball.draw(self.screen, self.font)
                
            # Render stik dan guideline jika bola diam
            if not self.is_moving:
                self.cue.draw(self.screen, self.balls, self.table.rect)
                
            # Render Power Bar
            bar_x, bar_y = SCREEN_WIDTH // 2 - 100, 25
            bar_w, bar_h = 200, 30
            pygame.draw.rect(self.screen, BLACK, (bar_x, bar_y, bar_w, bar_h), border_radius=5)
            pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=5)
            ratio = self.cue.power / self.cue.max_power
            if ratio > 0:
                fill_w = int((bar_w - 4) * ratio)
                fill_color = (255, int(255 * (1 - ratio)), 0) 
                pygame.draw.rect(self.screen, fill_color, (bar_x + 2, bar_y + 2, fill_w, bar_h - 4), border_radius=3)
                
                pow_txt = self.font.render("POWER", True, WHITE)
                txt_w = pow_txt.get_width()
                txt_h = pow_txt.get_height()
                bg_surf = pygame.Surface((txt_w + 10, txt_h + 4), pygame.SRCALPHA)
                bg_surf.fill((10, 10, 10, 180))
                
                dest_x = bar_x + bar_w // 2
                dest_y = bar_y + bar_h // 2
                bg_rect = bg_surf.get_rect(center=(dest_x, dest_y))
                self.screen.blit(bg_surf, bg_rect)
                
                txt_rect = pow_txt.get_rect(center=(dest_x, dest_y))
                self.screen.blit(pow_txt, txt_rect)
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = GameManager()
    game.run()