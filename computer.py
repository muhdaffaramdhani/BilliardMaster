import math
import random
import pygame
from config import *

class BilliardAI:
    """Class untuk mengelola kecerdasan buatan (AI) musuh billiard dengan 4 tingkat kesulitan"""
    def __init__(self, difficulty=1):
        self.difficulty = difficulty  # 0: EASY, 1: MEDIUM, 2: HARD, 3: MASTER
        self.error_ranges = [0.05, 0.02, 0.005, 0.0]  # Radian kesalahan aiming

    def calculate_shot(self, balls, table, player_assignments, cue_ball):
        p_type = player_assignments[2]
        
        # Tentukan bola mana saja yang boleh dipukul
        if p_type is None:
            # Open table: semua bola selain bola putih (0) dan hitam (8), kecuali hanya tersisa bola hitam
            allowed_nums = [b.number for b in balls if b.number != 0 and b.number != 8 and not b.potted]
            if not allowed_nums:
                allowed_nums = [8]
        else:
            if p_type == 'solid':
                allowed_nums = [num for num in range(1, 8) if next((b for b in balls if b.number == num and not b.potted), None)]
            else:  # stripe
                allowed_nums = [num for num in range(9, 16) if next((b for b in balls if b.number == num and not b.potted), None)]
            
            # Jika semua bola target sudah masuk, baru boleh memukul bola 8
            if not allowed_nums:
                allowed_nums = [8]
                
        allowed_balls = [b for b in balls if b.number in allowed_nums and not b.potted]
        
        # EASY (0): 50% kesempatan memilih bola acak untuk ditembak secara asal-asalan
        # MEDIUM (1): 20% kesempatan memilih bola acak
        random_choice = False
        if self.difficulty == 0 and random.random() < 0.5:
            random_choice = True
        elif self.difficulty == 1 and random.random() < 0.2:
            random_choice = True
            
        if random_choice and allowed_balls:
            # Pilih bola secara acak dan langsung bidik ke lubang terdekat
            target = random.choice(allowed_balls)
            pockets = table.pockets
            closest_pocket = min(pockets, key=lambda p: math.hypot(target.pos.x - p[0], target.pos.y - p[1]))
            
            dx_pocket = target.pos.x - closest_pocket[0]
            dy_pocket = target.pos.y - closest_pocket[1]
            dist_pocket = math.hypot(dx_pocket, dy_pocket)
            
            if dist_pocket > 0:
                dir_x = dx_pocket / dist_pocket
                dir_y = dy_pocket / dist_pocket
                contact_x = target.pos.x + dir_x * (BALL_RADIUS * 2)
                contact_y = target.pos.y + dir_y * (BALL_RADIUS * 2)
                
                dx_cue = contact_x - cue_ball.pos.x
                dy_cue = contact_y - cue_ball.pos.y
                
                best_angle = math.atan2(dy_cue, dx_cue)
                best_power = 11.0
                
                # Tambahkan error sesuai tingkat kesulitan
                err = self.error_ranges[self.difficulty]
                if err > 0:
                    best_angle += random.uniform(-err, err)
                    best_power += random.uniform(-err * 30, err * 30)
                return best_angle, min(max(best_power, 5.0), 20.0)

        # Cari tembakan terbaik berdasarkan skor kalkulasi lintasan
        best_score = -float('inf')
        best_angle = 0
        best_power = 12.0
        
        pockets = table.pockets
        
        for ball in allowed_balls:
            for pocket in pockets:
                dx_pocket = ball.pos.x - pocket[0]
                dy_pocket = ball.pos.y - pocket[1]
                dist_pocket = math.hypot(dx_pocket, dy_pocket)
                if dist_pocket == 0: continue
                
                # Titik kontak yang berlawanan arah dengan lubang
                dir_pocket_x = dx_pocket / dist_pocket
                dir_pocket_y = dy_pocket / dist_pocket
                
                contact_x = ball.pos.x + dir_pocket_x * (BALL_RADIUS * 2)
                contact_y = ball.pos.y + dir_pocket_y * (BALL_RADIUS * 2)
                contact_pos = pygame.math.Vector2(contact_x, contact_y)
                
                dx_cue = contact_x - cue_ball.pos.x
                dy_cue = contact_y - cue_ball.pos.y
                dist_cue = math.hypot(dx_cue, dy_cue)
                if dist_cue == 0: continue
                
                dir_cue_x = dx_cue / dist_cue
                dir_cue_y = dy_cue / dist_cue
                dir_target_pocket_x = -dir_pocket_x
                dir_target_pocket_y = -dir_pocket_y
                
                # Sudut potong tembakan (cut angle alignment)
                dot = dir_cue_x * dir_target_pocket_x + dir_cue_y * dir_target_pocket_y
                
                # Abaikan tembakan yang terlalu tipis/tajam (kemungkinan masuk sangat kecil)
                if dot < 0.15:
                    continue
                    
                # Hitung skor heuristik: semakin lurus sudut potong (+) dan semakin dekat lubang (+), skor semakin besar
                score = dot * 130 - dist_pocket * 0.15 - dist_cue * 0.05
                
                # Cek halangan di antara bola putih dan titik kontak
                cue_to_contact_dir = contact_pos - cue_ball.pos
                blocked = False
                # Gunakan threshold 2.05 kali radius agar terhindar dari benturan samping bola lain
                clearance_threshold = BALL_RADIUS * 2.05
                
                for other in balls:
                    if other == cue_ball or other == ball or other.potted:
                        continue
                    to_other = other.pos - cue_ball.pos
                    proj = to_other.dot(cue_to_contact_dir.normalize())
                    if 0 < proj < dist_cue:
                        closest_point = cue_ball.pos + cue_to_contact_dir.normalize() * proj
                        if closest_point.distance_to(other.pos) < clearance_threshold:
                            blocked = True
                            break
                            
                # Cek halangan di antara bola sasaran dan lubang
                target_to_pocket_dir = pygame.math.Vector2(pocket[0] - ball.pos.x, pocket[1] - ball.pos.y)
                for other in balls:
                    if other == cue_ball or other == ball or other.potted:
                        continue
                    to_other = other.pos - ball.pos
                    proj = to_other.dot(target_to_pocket_dir.normalize())
                    if 0 < proj < dist_pocket:
                        closest_point = ball.pos + target_to_pocket_dir.normalize() * proj
                        if closest_point.distance_to(other.pos) < clearance_threshold:
                            blocked = True
                            break
                            
                if blocked:
                    score -= 100  # Penalti besar untuk lintasan terhalang
                    
                if score > best_score:
                    best_score = score
                    best_angle = math.atan2(dy_cue, dx_cue)
                    # Kalkulasi power optimal agar bola tidak meluncur terlalu kencang atau pelan
                    dist_total = dist_cue + dist_pocket
                    best_power = min(max(6 + (dist_total / 100.0) * 3.0, 7.5), 18.5)
                    
        # Fallback jika semua lubang terhalang / tidak ada sudut potong yang layak
        if best_score == -float('inf') and allowed_balls:
            allowed_balls.sort(key=lambda b: b.pos.distance_to(cue_ball.pos))
            target = allowed_balls[0]
            dx = target.pos.x - cue_ball.pos.x
            dy = target.pos.y - cue_ball.pos.y
            best_angle = math.atan2(dy, dx)
            best_power = 10.0
            
        # Tambahkan error acak berdasarkan difficulty
        err = self.error_ranges[self.difficulty]
        if err > 0:
            best_angle += random.uniform(-err, err)
            best_power = min(max(best_power + random.uniform(-err * 40, err * 40), 5.0), 20.0)
            
        return best_angle, best_power
