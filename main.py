import pygame # type: ignore
import sys
import array
import math
import random
import os
from config import *
from ball import CueBall, ObjectBall
from table import Table
from cue import Cue
from physics import PhysicsEngine
from leaderboard import Leaderboard

class SoundGenerator:
    """Class untuk menghasilkan efek suara sintetis billiard yang realistis tanpa file eksternal"""
    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            self.sounds = {}
            self._generate_all_sounds()
            self.has_mixer = True
        except Exception:
            self.has_mixer = False

    def _generate_all_sounds(self):
        self.sounds['hit'] = self._generate_ball_hit()
        self.sounds['cue_hit'] = self._generate_cue_hit()
        self.sounds['wall'] = self._generate_wall_hit()
        self.sounds['pocket'] = self._generate_pocket()

    def _generate_ball_hit(self):
        sample_rate = 44100
        duration = 0.05
        n_samples = int(sample_rate * duration)
        buffer = array.array('h', [0] * n_samples)
        
        for i in range(n_samples):
            t = i / sample_rate
            # Extremely fast decay for high-pitched acrylic clack
            decay = math.exp(-t / 0.0035)
            
            # Harmonics of a solid acrylic sphere collision
            val = (0.5 * math.sin(2 * math.pi * 1400 * t) +
                   0.3 * math.sin(2 * math.pi * 2100 * t) +
                   0.15 * math.sin(2 * math.pi * 3200 * t) +
                   0.05 * math.sin(2 * math.pi * 4500 * t))
            
            # Initial sharp contact click noise
            if t < 0.0012:
                val += 0.4 * random.uniform(-1, 1)
                
            sample_val = int(val * decay * 16000)
            buffer[i] = max(-32768, min(32767, sample_val))
            
        return pygame.mixer.Sound(buffer)

    def _generate_cue_hit(self):
        sample_rate = 44100
        duration = 0.08
        n_samples = int(sample_rate * duration)
        buffer = array.array('h', [0] * n_samples)
        
        for i in range(n_samples):
            t = i / sample_rate
            # Slightly longer decay than ball-to-ball clack
            decay = math.exp(-t / 0.009)
            
            # Lower frequencies representing leather tip / wood cue contact
            val = (0.65 * math.sin(2 * math.pi * 320 * t) +
                   0.25 * math.sin(2 * math.pi * 650 * t) +
                   0.1 * math.sin(2 * math.pi * 1100 * t))
            
            # Leather friction noise at the instant of impact
            if t < 0.003:
                val += 0.25 * random.uniform(-1, 1)
                
            sample_val = int(val * decay * 15000)
            buffer[i] = max(-32768, min(32767, sample_val))
            
        return pygame.mixer.Sound(buffer)

    def _generate_wall_hit(self):
        sample_rate = 44100
        duration = 0.12
        n_samples = int(sample_rate * duration)
        buffer = array.array('h', [0] * n_samples)
        
        for i in range(n_samples):
            t = i / sample_rate
            # Rubbery wall absorbs high frequency, decays slower
            decay = math.exp(-t / 0.02)
            
            # Muffled low frequency thud
            val = (0.75 * math.sin(2 * math.pi * 130 * t) +
                   0.25 * math.sin(2 * math.pi * 260 * t))
            
            sample_val = int(val * decay * 14000)
            buffer[i] = max(-32768, min(32767, sample_val))
            
        return pygame.mixer.Sound(buffer)

    def _generate_pocket(self):
        sample_rate = 44100
        duration = 0.25
        n_samples = int(sample_rate * duration)
        buffer = array.array('h', [0] * n_samples)
        
        for i in range(n_samples):
            t = i / sample_rate
            # Heavy low thud as ball drops into pocket
            decay_thud = math.exp(-t / 0.065)
            val_thud = 0.65 * math.sin(2 * math.pi * 170 * t) * decay_thud
            
            # Rattle sound as ball clicks on pocket liner edges
            decay_rattle = math.exp(-t / 0.022)
            val_rattle = 0.35 * random.uniform(-1, 1) * decay_rattle
            
            val = val_thud + val_rattle
            sample_val = int(val * 16000)
            buffer[i] = max(-32768, min(32767, sample_val))
            
        return pygame.mixer.Sound(buffer)

    def play(self, name, volume=1.0):
        if self.enabled and self.has_mixer and name in self.sounds:
            self.sounds[name].set_volume(volume)
            self.sounds[name].play()

class Button:
    def __init__(self, x, y, w, h, text, color=ACCENT_COLOR):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = BUTTON_HOVER
        self.is_hovered = False
        self.font = pygame.font.SysFont('Arial', 20, bold=True)

    def draw(self, surface):
        color = self.color if not self.is_hovered else self.hover_color
        pygame.draw.rect(surface, (10, 10, 10), (self.rect.x + 2, self.rect.y + 2, self.rect.w, self.rect.h), border_radius=8)
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)
        
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered
        return False

class TextInput:
    """Class sederhana untuk input teks dengan autocomplete/dropdown saran nama"""
    def __init__(self, x, y, w, h, placeholder="Enter Name"):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.color_inactive = GREY
        self.color_active = ACCENT_COLOR
        self.font = pygame.font.SysFont('Arial', 22)
        self.suggestions = []

    def update_suggestions(self, all_names):
        if not self.active or not self.text.strip():
            self.suggestions = []
            return
        
        prefix = self.text.strip().lower()
        matches = []
        for name in all_names:
            if name.lower().startswith(prefix) and name.lower() != prefix:
                matches.append(name)
        self.suggestions = sorted(list(set(matches)))[:3]

    def handle_event(self, event, all_names=None):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.active and self.suggestions:
                for i, name in enumerate(self.suggestions):
                    s_rect = pygame.Rect(self.rect.x, self.rect.bottom + i * 35, self.rect.w, 35)
                    if s_rect.collidepoint(event.pos):
                        self.text = name
                        self.suggestions = []
                        self.active = False
                        return True
            
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
                self.suggestions = []
                
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.suggestions = []
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                if all_names:
                    self.update_suggestions(all_names)
            elif event.key == pygame.K_TAB:
                pass
            else:
                if len(self.text) < 12 and event.unicode.isprintable() and len(event.unicode) > 0:
                    self.text += event.unicode
                    if all_names:
                        self.update_suggestions(all_names)
        return False

    def draw_box(self, surface):
        color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(surface, BLACK, self.rect, border_radius=5)
        pygame.draw.rect(surface, color, self.rect, 2, border_radius=5)

        display_text = self.text if self.text else self.placeholder
        color_text = WHITE if self.text else GREY
        
        txt_surface = self.font.render(display_text, True, color_text)
        surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + (self.rect.h - txt_surface.get_height()) // 2))

    def draw_suggestions(self, surface, mouse_pos):
        if not self.active or not self.suggestions:
            return
        
        for i, name in enumerate(self.suggestions):
            s_rect = pygame.Rect(self.rect.x, self.rect.bottom + i * 35, self.rect.w, 35)
            is_hover = s_rect.collidepoint(mouse_pos)
            bg_col = (45, 50, 60) if is_hover else (25, 30, 40)
            
            pygame.draw.rect(surface, bg_col, s_rect, border_radius=4)
            pygame.draw.rect(surface, GREY, s_rect, 1, border_radius=4)
            
            txt_surf = self.font.render(name, True, YELLOW if is_hover else WHITE)
            surface.blit(txt_surf, (s_rect.x + 10, s_rect.y + (s_rect.h - txt_surf.get_height()) // 2))

    def draw(self, surface):
        self.draw_box(surface)

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Billiard 8-Ball Master - Final Project")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont('Arial', 18)
        self.debug_font = pygame.font.SysFont('Consolas', 14)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.header_font = pygame.font.SysFont('Arial', 28, bold=True)
        self.ball_font = pygame.font.SysFont('Arial', 10, bold=True)
        self.ui_ball_font = pygame.font.SysFont('Arial', 12, bold=True)
        
        self.state = STATE_MENU
        self.sound_manager = SoundGenerator()
        self.leaderboard = Leaderboard()

        self.ball_colors = {
            1: YELLOW, 2: BLUE, 3: RED, 4: PURPLE, 5: ORANGE, 6: GREEN, 7: MAROON,
            9: YELLOW, 10: BLUE, 11: RED, 12: PURPLE, 13: ORANGE, 14: GREEN, 15: MAROON,
            8: BLACK
        }

        self.sens_values = SENS_VALUES
        self.sens_names = SENS_NAMES
        self.current_sens_idx = 2  # Default to level 3 (Normal)

        self.p1_name = "Player 1"
        self.p2_name = "Player 2"
        self.winner_name = ""

        self.vs_computer = False
        self.settings_back_state = STATE_MENU
        self.ai_state = None
        self.ai_timer = 0
        self.ai_target_angle = 0
        self.ai_target_power = 0
        self.player_history = self.load_player_history()

        self.init_ui()
        self.init_input_ui()
        self.reset_game_objects()

    def load_player_history(self):
        import json
        if not os.path.exists("player_history.json"):
            return []
        try:
            with open("player_history.json", "r") as f:
                return json.load(f)
        except Exception:
            return []

    def save_player_history(self, name):
        import json
        name = name.strip()
        if not name or name.lower() == "computer":
            return
        history = self.load_player_history()
        if not any(h.lower() == name.lower() for h in history):
            history.append(name)
            try:
                with open("player_history.json", "w") as f:
                    json.dump(history, f, indent=4)
            except Exception:
                pass
        self.player_history = history

    def init_ui(self):
        cx = SCREEN_WIDTH // 2
        start_y = 250
        gap = 55
        
        self.btn_start = Button(cx - 100, start_y, 200, 45, "PLAY GAME")
        self.btn_leaderboard = Button(cx - 100, start_y + gap, 200, 45, "LEADERBOARD")
        self.btn_tutorial = Button(cx - 100, start_y + gap * 2, 200, 45, "TUTORIAL")
        self.btn_team = Button(cx - 100, start_y + gap * 3, 200, 45, "OUR TEAM")
        self.btn_settings = Button(cx - 100, start_y + gap * 4, 200, 45, "SETTINGS")
        self.btn_quit = Button(cx - 100, start_y + gap * 5, 200, 45, "QUIT")
        
        self.btn_back_panel = Button(cx - 100, 580, 200, 40, "BACK", GREY)
        
        self.btn_toggle_sound = Button(cx - 100, 300, 200, 50, "SOUND: [ ON ]")
        self.btn_sensitivity = Button(cx - 100, 370, 200, 50, f"SENSITIVITY: < {self.sens_names[self.current_sens_idx]} >")
        
        self.btn_pause_game = Button(SCREEN_WIDTH - 120, 20, 100, 40, "MENU", GREY)
        
        self.btn_resume = Button(cx - 100, SCREEN_HEIGHT//2 - 60, 200, 50, "RESUME", ACCENT_COLOR)
        self.btn_restart = Button(cx - 100, SCREEN_HEIGHT//2 + 10, 200, 50, "RESTART MATCH", RED)
        self.btn_settings_paused = Button(cx - 100, SCREEN_HEIGHT//2 + 80, 200, 50, "SETTINGS", ACCENT_COLOR)
        self.btn_exit_to_menu = Button(cx - 100, SCREEN_HEIGHT//2 + 150, 200, 50, "MAIN MENU", GREY)
        
        self.btn_play_again = Button(cx - 100, 380, 200, 50, "PLAY AGAIN", ACCENT_COLOR)
        self.btn_main_menu = Button(cx - 100, 450, 200, 50, "MAIN MENU", GREY)

    def init_input_ui(self):
        cx = SCREEN_WIDTH // 2
        self.btn_mode_toggle = Button(cx - 150, 205, 300, 45, "MODE: 2 PLAYERS", ACCENT_COLOR)
        self.input_p1 = TextInput(cx - 150, 270, 300, 45, "Player 1 Name")
        self.input_p2 = TextInput(cx - 150, 335, 300, 45, "Player 2 Name")
        self.btn_start_match = Button(cx - 100, 410, 200, 45, "START MATCH", GREEN)

    def reset_game_objects(self):
        self.table = Table()
        self.cue_ball = CueBall(TABLE_X + 200, TABLE_Y + PLAY_HEIGHT // 2)
        self.balls = [self.cue_ball]
        
        self.cue = Cue(self.cue_ball)
        self.cue.sensitivity = self.sens_values[self.current_sens_idx]
        
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
        
        self.turn = 1
        self.player_assignments = {1: None, 2: None}
        self.scores = {1: [], 2: []}
        self.is_moving = False
        self.ball_potted_this_turn = False
        self.message = "Break Shot!"
        self.message_timer = 120
        self.winner_text = ""
        self.winner_name = ""

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.state == STATE_MENU:
                    if self.btn_start.is_clicked(event): 
                        self.state = STATE_INPUT_NAMES
                        self.input_p1.text = ""
                        self.input_p2.text = ""
                        self.input_p1.active = True
                        if self.vs_computer:
                            self.input_p2.text = "Computer"
                    if self.btn_leaderboard.is_clicked(event): self.state = STATE_LEADERBOARD
                    if self.btn_tutorial.is_clicked(event): self.state = STATE_TUTORIAL
                    if self.btn_team.is_clicked(event): self.state = STATE_TEAM
                    if self.btn_settings.is_clicked(event):
                        self.settings_back_state = STATE_MENU
                        self.state = STATE_SETTINGS
                    if self.btn_quit.is_clicked(event): pygame.quit(); sys.exit()

                elif self.state == STATE_INPUT_NAMES:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                        if self.input_p1.active:
                            self.input_p1.active = False
                            self.input_p1.suggestions = []
                            if not self.vs_computer:
                                self.input_p2.active = True
                                self.input_p2.update_suggestions(self.player_history)
                        elif self.input_p2.active:
                            self.input_p2.active = False
                            self.input_p2.suggestions = []
                            self.input_p1.active = True
                            self.input_p1.update_suggestions(self.player_history)
                    else:
                        if self.btn_mode_toggle.is_clicked(event):
                            self.vs_computer = not self.vs_computer
                            if self.vs_computer:
                                self.btn_mode_toggle.text = "MODE: VS COMPUTER"
                                self.input_p2.text = "Computer"
                                self.input_p2.active = False
                                self.input_p2.suggestions = []
                            else:
                                self.btn_mode_toggle.text = "MODE: 2 PLAYERS"
                                if self.input_p2.text == "Computer":
                                    self.input_p2.text = ""
                        
                        self.input_p1.handle_event(event, self.player_history)
                        if not self.vs_computer:
                            self.input_p2.handle_event(event, self.player_history)
                            
                        if self.btn_start_match.is_clicked(event):
                            self.p1_name = self.input_p1.text.strip() if self.input_p1.text.strip() else "Player 1"
                            self.p2_name = self.input_p2.text.strip() if self.input_p2.text.strip() else "Player 2"
                            if self.vs_computer:
                                self.p2_name = "Computer"
                            self.save_player_history(self.p1_name)
                            if not self.vs_computer:
                                self.save_player_history(self.p2_name)
                            self.reset_game_objects()
                            self.state = STATE_PLAYING
                            
                    if self.btn_back_panel.is_clicked(event): self.state = STATE_MENU

                elif self.state == STATE_PLAYING:
                    if self.btn_pause_game.is_clicked(event): 
                        self.state = STATE_PAUSED
                    if not self.btn_pause_game.is_hovered:
                        if not (self.vs_computer and self.turn == 2):
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                if not self.is_moving:
                                    shot_power = self.cue.power
                                    if self.cue.handle_click():
                                        self.is_moving = True
                                        vol = min(1.0, shot_power / self.cue.max_power) if shot_power > 0 else 0.5
                                        self.sound_manager.play('cue_hit', volume=vol)
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                                self.cue.cancel_shot()

                elif self.state == STATE_GAME_OVER:
                    if self.btn_play_again.is_clicked(event):
                        self.reset_game_objects()
                        self.state = STATE_PLAYING
                    if self.btn_main_menu.is_clicked(event):
                        self.reset_game_objects()
                        self.state = STATE_MENU
                
                elif self.state in [STATE_SETTINGS, STATE_TUTORIAL, STATE_TEAM, STATE_LEADERBOARD]:
                    if self.btn_back_panel.is_clicked(event): 
                        self.state = self.settings_back_state
                    
                    if self.state == STATE_SETTINGS:
                        if self.btn_toggle_sound.is_clicked(event):
                            self.sound_manager.enabled = not self.sound_manager.enabled
                            self.btn_toggle_sound.text = f"SOUND: [ {'ON' if self.sound_manager.enabled else 'OFF'} ]"
                        if self.btn_sensitivity.is_clicked(event):
                            self.current_sens_idx = (self.current_sens_idx + 1) % 5
                            self.btn_sensitivity.text = f"SENSITIVITY: < {self.sens_names[self.current_sens_idx]} >"
                            if self.cue: self.cue.sensitivity = self.sens_values[self.current_sens_idx]
                        if event.type == pygame.KEYDOWN:
                            if self.btn_sensitivity.is_hovered:
                                if event.key == pygame.K_LEFT:
                                    self.current_sens_idx = max(0, self.current_sens_idx - 1)
                                    self.btn_sensitivity.text = f"SENSITIVITY: < {self.sens_names[self.current_sens_idx]} >"
                                    if self.cue: self.cue.sensitivity = self.sens_values[self.current_sens_idx]
                                elif event.key == pygame.K_RIGHT:
                                    self.current_sens_idx = min(4, self.current_sens_idx + 1)
                                    self.btn_sensitivity.text = f"SENSITIVITY: < {self.sens_names[self.current_sens_idx]} >"
                                    if self.cue: self.cue.sensitivity = self.sens_values[self.current_sens_idx]

                elif self.state == STATE_PAUSED:
                    if self.btn_resume.is_clicked(event): self.state = STATE_PLAYING
                    if self.btn_restart.is_clicked(event):
                        self.reset_game_objects()
                        self.state = STATE_PLAYING
                    if self.btn_settings_paused.is_clicked(event):
                        self.settings_back_state = STATE_PAUSED
                        self.state = STATE_SETTINGS
                    if self.btn_exit_to_menu.is_clicked(event):
                        self.reset_game_objects()
                        self.state = STATE_MENU

            self.screen.fill(UI_BG)
            
            if self.state == STATE_MENU:
                self.draw_menu(mouse_pos)
            elif self.state == STATE_INPUT_NAMES:
                self.draw_input_names(mouse_pos)
            elif self.state == STATE_PLAYING:
                self.update_game_logic(mouse_pos)
                self.draw_game(mouse_pos)
            elif self.state == STATE_PAUSED:
                self.update_game_logic(mouse_pos)
                self.draw_game(mouse_pos)
                self.draw_paused(mouse_pos)
            elif self.state == STATE_GAME_OVER:
                self.draw_game_over(mouse_pos)
            elif self.state == STATE_TUTORIAL:
                self.draw_tutorial(mouse_pos)
            elif self.state == STATE_TEAM:
                self.draw_team(mouse_pos)
            elif self.state == STATE_SETTINGS:
                self.draw_settings(mouse_pos)
            elif self.state == STATE_LEADERBOARD:
                self.draw_leaderboard(mouse_pos)

            if DEBUG_MODE: self.draw_debug_info()
            
            self.clock.tick(FPS)
            pygame.display.flip()

    def update_game_logic(self, mouse_pos):
        if self.state == STATE_PAUSED: return

        if not self.is_moving:
            if self.vs_computer and self.turn == 2:
                self.update_ai_logic()
            else:
                self.cue.update(mouse_pos)
        
        physics_steps = 10 
        for _ in range(physics_steps):
            for ball in self.balls:
                if ball.potted: continue
                ball.pos += ball.velocity / physics_steps
                if ball.check_wall_collision(self.table.rect):
                    impact = ball.velocity.length()
                    if impact > 0.5:
                        vol = min(1.0, impact / 10.0)
                        self.sound_manager.play('wall', volume=vol)
                if ball.check_pocket_collision(self.table.pockets):
                    self.sound_manager.play('pocket')
                    self.handle_pot(ball)
            
            for i in range(len(self.balls)):
                for j in range(i + 1, len(self.balls)):
                    b1 = self.balls[i]
                    b2 = self.balls[j]
                    if PhysicsEngine.resolve_collision(b1, b2):
                        impact = (b1.velocity - b2.velocity).length()
                        if impact > 0.5:
                            vol = min(1.0, impact / 12.0)
                            self.sound_manager.play('hit', volume=vol)

        moving_count = 0
        for ball in self.balls:
            if ball.potted: continue
            if ball.velocity.length() > 0.05:
                ball.velocity *= ball.friction
                moving_count += 1
            else:
                ball.velocity = pygame.math.Vector2(0, 0)

        if self.is_moving and moving_count == 0:
            self.is_moving = False
            self.cue.state = 0
            if self.state != STATE_GAME_OVER:
                self.switch_turn()
            
        if self.message_timer > 0: self.message_timer -= 1

    def handle_pot(self, ball):
        if ball.type == "cue":
            self.ball_potted_this_turn = False
            self.message = "FOUL! Cue Ball Potted"
            ball.reset()
        elif ball.type == "eight":
            current_player = self.turn
            p_type = self.player_assignments[current_player]
            has_won = False
            
            if p_type:
                target_nums = list(range(1, 8)) if p_type == 'solid' else list(range(9, 16))
                remaining = [b for b in self.balls if b.number in target_nums and not b.potted]
                if not remaining: has_won = True
                else: has_won = False
            else:
                has_won = False
            
            if has_won:
                winner_id = current_player
                self.winner_name = self.p1_name if winner_id == 1 else self.p2_name
                self.winner_text = f"VICTORY! {self.winner_name.upper()} WINS!"
                self.leaderboard.add_win(self.winner_name)
            else:
                winner_id = 2 if current_player == 1 else 1
                self.winner_name = self.p1_name if winner_id == 1 else self.p2_name
                self.winner_text = f"GAME OVER! {self.winner_name.upper()} WINS!"
                self.leaderboard.add_win(self.winner_name)
                
            self.state = STATE_GAME_OVER
        else:
            if self.player_assignments[1] is None:
                if self.turn == 1:
                    self.player_assignments[1] = ball.type
                    self.player_assignments[2] = "stripe" if ball.type == "solid" else "solid"
                else:
                    self.player_assignments[2] = ball.type
                    self.player_assignments[1] = "stripe" if ball.type == "solid" else "solid"
            
            if self.player_assignments[self.turn] == ball.type or self.player_assignments[self.turn] is None:
                self.scores[self.turn].append(ball)
                self.ball_potted_this_turn = True
            else:
                opponent = 2 if self.turn == 1 else 1
                self.scores[opponent].append(ball)
                self.ball_potted_this_turn = False

    def switch_turn(self):
        player_name = self.p1_name if self.turn == 2 else self.p2_name
        if not self.ball_potted_this_turn:
            self.turn = 2 if self.turn == 1 else 1
            next_name = self.p1_name if self.turn == 1 else self.p2_name
            self.message = f"Turn: {next_name}"
        else:
            current_name = self.p1_name if self.turn == 1 else self.p2_name
            self.message = f"Continue: {current_name}"
        self.message_timer = 60
        self.ball_potted_this_turn = False

    def draw_menu(self, mouse_pos):
        title = self.title_font.render("BILLIARD MASTER", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        for btn in [self.btn_start, self.btn_leaderboard, self.btn_tutorial, self.btn_team, self.btn_settings, self.btn_quit]:
            btn.check_hover(mouse_pos)
            btn.draw(self.screen)

    def draw_input_names(self, mouse_pos):
        self.draw_panel("ENTER PLAYER NAMES", height=480)
        
        self.btn_mode_toggle.check_hover(mouse_pos)
        self.btn_mode_toggle.draw(self.screen)
        
        self.input_p1.draw_box(self.screen)
        self.input_p2.draw_box(self.screen)
        
        self.btn_start_match.check_hover(mouse_pos)
        self.btn_start_match.draw(self.screen)
        
        self.btn_back_panel.check_hover(mouse_pos)
        self.btn_back_panel.draw(self.screen)
        
        # Draw suggestions on top of everything
        self.input_p1.draw_suggestions(self.screen, mouse_pos)
        self.input_p2.draw_suggestions(self.screen, mouse_pos)

    def draw_leaderboard(self, mouse_pos):
        x, y, w, h = self.draw_panel("TOP PLAYERS", height=500)
        
        top_players = self.leaderboard.get_top_players(5)
        
        start_y = y + 100
        headers = ["Rank", "Name", "Wins"]
        gx = [x + 50, x + 150, x + 450]
        for i, h_text in enumerate(headers):
            surf = self.font.render(h_text, True, ACCENT_COLOR)
            self.screen.blit(surf, (gx[i], start_y))
            
        start_y += 30
        pygame.draw.line(self.screen, GREY, (x + 30, start_y), (x + w - 30, start_y), 1)
        start_y += 10
        
        if not top_players:
            txt = self.font.render("No records yet.", True, GREY)
            self.screen.blit(txt, (x + w//2 - txt.get_width()//2, start_y + 20))
        else:
            for i, player in enumerate(top_players):
                col = YELLOW if i == 0 else WHITE
                
                rank_txt = self.font.render(f"#{i+1}", True, col)
                name_txt = self.font.render(player['name'], True, col)
                wins_txt = self.font.render(str(player['wins']), True, col)
                
                self.screen.blit(rank_txt, (gx[0], start_y))
                self.screen.blit(name_txt, (gx[1], start_y))
                self.screen.blit(wins_txt, (gx[2], start_y))
                
                start_y += 40

        self.btn_back_panel.check_hover(mouse_pos)
        self.btn_back_panel.draw(self.screen)

    def draw_panel(self, title, height=450):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0,0))
        
        panel_w, panel_h = 600, height
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = (SCREEN_HEIGHT - panel_h) // 2
        
        pygame.draw.rect(self.screen, (10, 10, 10), (panel_x + 5, panel_y + 5, panel_w, panel_h), border_radius=15)
        pygame.draw.rect(self.screen, DARK_GREY, (panel_x, panel_y, panel_w, panel_h), border_radius=15)
        pygame.draw.rect(self.screen, ACCENT_COLOR, (panel_x, panel_y, panel_w, panel_h), 2, border_radius=15)
        
        title_surf = self.header_font.render(title, True, ACCENT_COLOR)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, panel_y + 40))
        self.screen.blit(title_surf, title_rect)
        
        pygame.draw.line(self.screen, GREY, (panel_x + 50, panel_y + 70), (panel_x + panel_w - 50, panel_y + 70), 2)
        return panel_x, panel_y, panel_w, panel_h

    def draw_settings(self, mouse_pos):
        self.draw_panel("SETTINGS")
        self.btn_toggle_sound.check_hover(mouse_pos)
        self.btn_toggle_sound.draw(self.screen)
        self.btn_sensitivity.check_hover(mouse_pos)
        self.btn_sensitivity.draw(self.screen)
        
        # Draw instruction text
        help_text = self.font.render("(Use Left/Right arrow keys to adjust)", True, GREY)
        self.screen.blit(help_text, (SCREEN_WIDTH//2 - help_text.get_width()//2, 430))
        
        self.btn_back_panel.check_hover(mouse_pos)
        self.btn_back_panel.draw(self.screen)

    def draw_tutorial(self, mouse_pos):
        panel_x, panel_y, _, _ = self.draw_panel("HOW TO PLAY")
        lines = [
            ("Arahkan Mouse", "Untuk membidik bola sasaran."),
            ("Klik Kiri (1x)", "Mengunci arah (Aim Lock)."),
            ("Tarik Mouse", "Mengatur kekuatan (Power)."),
            ("Klik Kiri (2x)", "Melepaskan tembakan."),
            ("Klik Kanan", "Membatalkan tembakan/kunci."),
        ]
        start_y_text = panel_y + 100
        for action, desc in lines:
            act_surf = self.font.render(action, True, ACCENT_COLOR)
            self.screen.blit(act_surf, (panel_x + 50, start_y_text))
            desc_surf = self.font.render(f":  {desc}", True, WHITE)
            self.screen.blit(desc_surf, (panel_x + 200, start_y_text))
            start_y_text += 40
        self.btn_back_panel.check_hover(mouse_pos)
        self.btn_back_panel.draw(self.screen)

    def draw_team(self, mouse_pos):
        _, panel_y, _, _ = self.draw_panel("OUR TEAM")
        team_members = [
            "Fujiono Nur Ikhsan (1313624008)",
            "Muhammad Daffa Ramdhani (1313624025)",
            "Leonard Dwi Chrisdiasa (1313624031)",
        ]
        start_y_text = panel_y + 120
        for member in team_members:
            txt_surf = self.font.render(member, True, WHITE)
            txt_rect = txt_surf.get_rect(center=(SCREEN_WIDTH//2, start_y_text))
            self.screen.blit(txt_surf, txt_rect)
            start_y_text += 45
        self.btn_back_panel.check_hover(mouse_pos)
        self.btn_back_panel.draw(self.screen)

    def draw_game(self, mouse_pos):
        pygame.draw.rect(self.screen, DARK_GREY, (0, 0, SCREEN_WIDTH, 80))
        
        p1_type = self.player_assignments[1] if self.player_assignments[1] else "OPEN"
        p1_col = ACCENT_COLOR if self.turn == 1 else GREY
        p1_txt = self.font.render(f"{self.p1_name} ({p1_type.upper()})", True, p1_col)
        self.screen.blit(p1_txt, (50, 20))
        if self.turn == 1: pygame.draw.circle(self.screen, ACCENT_COLOR, (30, 30), 5)
        self.draw_remaining_balls(1, 50, 55, align_left=True)
            
        p2_type = self.player_assignments[2] if self.player_assignments[2] else "OPEN"
        p2_col = ACCENT_COLOR if self.turn == 2 else GREY
        p2_txt = self.font.render(f"{self.p2_name} ({p2_type.upper()})", True, p2_col)
        p2_rect = p2_txt.get_rect(topright=(SCREEN_WIDTH - 150, 20))
        self.screen.blit(p2_txt, p2_rect)
        if self.turn == 2: pygame.draw.circle(self.screen, ACCENT_COLOR, (SCREEN_WIDTH - 30, 30), 5)
        self.draw_remaining_balls(2, SCREEN_WIDTH - 150, 55, align_left=False)

        bar_x, bar_y = SCREEN_WIDTH // 2 - 100, 25
        bar_w, bar_h = 200, 30
        pygame.draw.rect(self.screen, BLACK, (bar_x, bar_y, bar_w, bar_h), border_radius=5)
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=5)
        ratio = self.cue.power / self.cue.max_power
        if ratio > 0:
            fill_w = int((bar_w - 4) * ratio)
            fill_color = (255, int(255 * (1 - ratio)), 0) 
            pygame.draw.rect(self.screen, fill_color, (bar_x + 2, bar_y + 2, fill_w, bar_h - 4), border_radius=3)
        pow_txt = self.ball_font.render("POWER", True, WHITE)
        self.screen.blit(pow_txt, (bar_x + bar_w // 2 - pow_txt.get_width() // 2, bar_y + 8))

        self.table.draw(self.screen)
        for ball in self.balls: ball.draw(self.screen, self.ball_font)
        if not self.is_moving and self.state != STATE_PAUSED:
            self.cue.draw(self.screen, self.balls, self.table.rect)
            
        if self.message_timer > 0:
            msg_surf = self.title_font.render(self.message, True, WHITE)
            msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            bg_rect = msg_rect.inflate(40, 20)
            pygame.draw.rect(self.screen, (0,0,0,180), bg_rect, border_radius=10)
            self.screen.blit(msg_surf, msg_rect)
            
        self.btn_pause_game.check_hover(mouse_pos)
        self.btn_pause_game.draw(self.screen)

    def draw_remaining_balls(self, player_num, start_x, start_y, align_left=True):
        p_type = self.player_assignments[player_num]
        if p_type is None:
            target_nums = list(range(1, 8)) if player_num == 1 else list(range(9, 16))
        else:
            target_nums = list(range(1, 8)) if p_type == 'solid' else list(range(9, 16))
        balls_to_draw = [num for num in target_nums if next((b for b in self.balls if b.number == num and not b.potted), None)]
        
        spacing = 25
        for i, num in enumerate(balls_to_draw):
            color = self.ball_colors.get(num, WHITE)
            pos_x = start_x + (i * spacing) if align_left else start_x - (i * spacing)
            pygame.draw.circle(self.screen, color, (pos_x, start_y), 10)
            if num > 8:
                pygame.draw.circle(self.screen, WHITE, (pos_x, start_y), 7)
                pygame.draw.rect(self.screen, color, (pos_x - 8, start_y - 3, 16, 6))
            txt = self.ui_ball_font.render(str(num), True, BLACK)
            txt_rect = txt.get_rect(center=(pos_x, start_y))
            self.screen.blit(txt, txt_rect)

    def draw_paused(self, mouse_pos):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0,0))
        text = self.title_font.render("GAME PAUSED", True, WHITE)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 120))
        self.screen.blit(text, rect)
        
        for btn in [self.btn_resume, self.btn_restart, self.btn_settings_paused, self.btn_exit_to_menu]:
            btn.check_hover(mouse_pos)
            btn.draw(self.screen)

    def update_ai_logic(self):
        if self.ai_state is None:
            self.ai_state = 'thinking'
            self.ai_timer = 45  # 0.75s thinking delay
            
        elif self.ai_state == 'thinking':
            self.ai_timer -= 1
            if self.ai_timer <= 0:
                self.calculate_ai_shot()
                self.ai_state = 'aiming'
                self.cue.state = 0
                
        elif self.ai_state == 'aiming':
            diff = (self.ai_target_angle - self.cue.angle + math.pi) % (2 * math.pi) - math.pi
            step = 0.04
            if abs(diff) < step:
                self.cue.angle = self.ai_target_angle
                self.ai_state = 'powering'
                self.cue.state = 1
            else:
                self.cue.angle += math.copysign(step, diff)
                
        elif self.ai_state == 'powering':
            step = 0.4
            if self.cue.power >= self.ai_target_power:
                self.cue.power = self.ai_target_power
                self.ai_state = 'shooting'
                self.ai_timer = 15  # brief pause before shooting
            else:
                self.cue.power += step
                
        elif self.ai_state == 'shooting':
            self.ai_timer -= 1
            if self.ai_timer <= 0:
                vol = min(1.0, self.ai_target_power / self.cue.max_power) if self.ai_target_power > 0 else 0.5
                self.cue.shoot()
                self.sound_manager.play('cue_hit', volume=vol)
                self.is_moving = True
                self.ai_state = None

    def calculate_ai_shot(self):
        p_type = self.player_assignments[2]
        
        if p_type is None:
            allowed_nums = [b.number for b in self.balls if b.number != 0 and b.number != 8 and not b.potted]
            if not allowed_nums:
                allowed_nums = [8]
        else:
            if p_type == 'solid':
                allowed_nums = [num for num in range(1, 8) if next((b for b in self.balls if b.number == num and not b.potted), None)]
            else:
                allowed_nums = [num for num in range(9, 16) if next((b for b in self.balls if b.number == num and not b.potted), None)]
            
            if not allowed_nums:
                allowed_nums = [8]
                
        allowed_balls = [b for b in self.balls if b.number in allowed_nums and not b.potted]
        
        best_score = -float('inf')
        best_angle = 0
        best_power = 12
        
        pockets = self.table.pockets
        cue_ball = self.cue_ball
        
        for ball in allowed_balls:
            for pocket in pockets:
                dx_pocket = ball.pos.x - pocket[0]
                dy_pocket = ball.pos.y - pocket[1]
                dist_pocket = math.hypot(dx_pocket, dy_pocket)
                if dist_pocket == 0: continue
                
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
                
                dot = dir_cue_x * dir_target_pocket_x + dir_cue_y * dir_target_pocket_y
                
                if dot < 0.15:
                    continue
                    
                score = dot * 120 - dist_pocket * 0.15 - dist_cue * 0.05
                
                cue_to_contact_dir = contact_pos - cue_ball.pos
                blocked = False
                for other in self.balls:
                    if other == cue_ball or other == ball or other.potted:
                        continue
                    to_other = other.pos - cue_ball.pos
                    proj = to_other.dot(cue_to_contact_dir.normalize())
                    if 0 < proj < dist_cue:
                        closest_point = cue_ball.pos + cue_to_contact_dir.normalize() * proj
                        if closest_point.distance_to(other.pos) < BALL_RADIUS * 1.9:
                            blocked = True
                            break
                            
                target_to_pocket_dir = pygame.math.Vector2(pocket[0] - ball.pos.x, pocket[1] - ball.pos.y)
                for other in self.balls:
                    if other == cue_ball or other == ball or other.potted:
                        continue
                    to_other = other.pos - ball.pos
                    proj = to_other.dot(target_to_pocket_dir.normalize())
                    if 0 < proj < dist_pocket:
                        closest_point = ball.pos + target_to_pocket_dir.normalize() * proj
                        if closest_point.distance_to(other.pos) < BALL_RADIUS * 1.9:
                            blocked = True
                            break
                            
                if blocked:
                    score -= 80
                    
                if score > best_score:
                    best_score = score
                    best_angle = math.atan2(dy_cue, dx_cue)
                    dist_total = dist_cue + dist_pocket
                    best_power = min(max(5 + (dist_total / 90.0) * 2.5, 7), 18)
                    
        if best_score == -float('inf') and allowed_balls:
            allowed_balls.sort(key=lambda b: b.pos.distance_to(cue_ball.pos))
            target = allowed_balls[0]
            dx = target.pos.x - cue_ball.pos.x
            dy = target.pos.y - cue_ball.pos.y
            best_angle = math.atan2(dy, dx)
            best_power = 10
            
        best_angle += random.uniform(-0.03, 0.03)
        best_power = min(max(best_power + random.uniform(-1.0, 1.0), 4.0), 20.0)
        
        self.ai_target_angle = best_angle
        self.ai_target_power = best_power

    def draw_game_over(self, mouse_pos):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0,0))
        
        color = GREEN if "VICTORY" in self.winner_text else RED
        text = self.title_font.render(self.winner_text, True, color)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(text, rect)
        
        for btn in [self.btn_play_again, self.btn_main_menu]:
            btn.check_hover(mouse_pos)
            btn.draw(self.screen)

    def draw_debug_info(self):
        fps = int(self.clock.get_fps())
        fps_text = self.debug_font.render(f"FPS: {fps}", True, GREEN)
        self.screen.blit(fps_text, (10, SCREEN_HEIGHT - 30))

if __name__ == "__main__":
    game = GameManager()
    game.run()