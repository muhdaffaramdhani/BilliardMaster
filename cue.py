# cue.py — Week 2: Cue Stick Stub
import pygame
import math
from config import *

class Cue:
    def __init__(self, target_ball):
        self.target_ball = target_ball
        self.angle = 0
        self.width = 300
        self.height = 8
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (139, 69, 19), (0, 0, self.width, self.height), border_radius=4)
        pygame.draw.rect(self.image, (240, 240, 240), (0, 0, 10, self.height), border_radius=4)

    def update(self, mouse_pos):
        # Hitung sudut stik berdasarkan posisi mouse terhadap cue ball
        dx = self.target_ball.pos.x - mouse_pos[0]
        dy = self.target_ball.pos.y - mouse_pos[1]
        self.angle = math.atan2(dy, dx)

    def draw(self, surface):
        if self.target_ball.potted:
            return
            
        angle_degrees = math.degrees(-self.angle)
        rotated_stick = pygame.transform.rotate(self.image, angle_degrees)
        pull_back = 20
        
        offset_x = math.cos(self.angle) * (self.width/2 + pull_back)
        offset_y = math.sin(self.angle) * (self.width/2 + pull_back)
        center_x = self.target_ball.pos.x - offset_x
        center_y = self.target_ball.pos.y - offset_y
        
        rect = rotated_stick.get_rect(center=(center_x, center_y))
        surface.blit(rotated_stick, rect)