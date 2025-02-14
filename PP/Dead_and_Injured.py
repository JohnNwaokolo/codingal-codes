import pygame
import sys
import os
import socket
import threading
import time
import json

# ----------------------- Initialization -----------------------
pygame.init()
pygame.mixer.init()
pygame.font.init()

# ----------------------- Global Constants -----------------------
WIDTH, HEIGHT = 600, 500
FPS = 30
SERVER_PORT = 12345

# Colors
WHITE    = (255, 255, 255)
BLACK    = (0, 0, 0)
GRAY     = (200, 200, 200)
DARKGRAY = (50, 50, 50)
GREEN    = (0, 200, 0)
RED      = (255, 0, 0)
BLUE     = (0, 0, 255)

# ----------------------- Display Setup -----------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dead and Injured")
clock = pygame.time.Clock()

# ----------------------- Asset Loading -----------------------
def load_image(path, scale=None):
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    return None

background_image = load_image(os.path.join("assets", "background.png"), (WIDTH, HEIGHT))
font_path = os.path.join("assets", "custom_font.ttf")
if os.path.exists(font_path):
    FONT = pygame.font.Font(font_path, 36)
    SMALL_FONT = pygame.font.Font(font_path, 28)
    TITLE_FONT = pygame.font.Font(font_path, 64)
else:
    FONT = pygame.font.Font(None, 36)
    SMALL_FONT = pygame.font.Font(None, 28)
    TITLE_FONT = pygame.font.Font(None, 64)

def load_sound(sound_name):
    sound_path = os.path.join("assets", "sounds", sound_name)
    if os.path.exists(sound_path):
        try:
            return pygame.mixer.Sound(sound_path)
        except pygame.error:
            print(f"Could not load sound: {sound_name}")
    else:
        print(f"Sound file {sound_name} not found.")
    return None

bg_music = os.path.join("assets", "sounds", "bg_music.mp3")
if os.path.exists(bg_music):
    try:
        pygame.mixer.music.load(bg_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Background music failed to load.")
click_sound   = load_sound("click.wav")
correct_sound = load_sound("correct.wav")
win_sound     = load_sound("win.wav")
error_sound   = load_sound("error.wav")

def draw_background():
    if background_image:
        screen.blit(background_image, (0,0))
    else:
        screen.fill(WHITE)

def draw_text(surface, text, font, color, pos, center=False):
    text_surf = font.render(text, True, color)
    if center:
        text_rect = text_surf.get_rect(center=pos)
    else:
        text_rect = text_surf.get_rect(topleft=pos)
    surface.blit(text_surf, text_rect)

def fade_transition(duration=0.5):
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(BLACK)
    steps = int(FPS * duration)
    for alpha in range(0, 256, int(256/steps)):
        fade.set_alpha(alpha)
        draw_background()
        screen.blit(fade, (0,0))
        pygame.display.flip()
        clock.tick(FPS)
    for alpha in range(255, -1, -int(256/steps)):
        fade.set_alpha(alpha)
        draw_background()
        screen.blit(fade, (0,0))
        pygame.display.flip()
        clock.tick(FPS)

# ----------------------- Networking -----------------------
class NetworkHandler:
    def __init__(self, is_host, host_ip=None):
        self.is_host = is_host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.received_messages = []
        self.thread = None
        self.host_ip = host_ip

    def start(self):
        if self.is_host:
            try:
                self.sock.bind(('', SERVER_PORT))
                self.sock.listen(1)
                print("Waiting for client connection...")
                self.conn, addr = self.sock.accept()
                print("Connected to:", addr)
                self.connected = True
                self.thread = threading.Thread(target=self.receive_loop, daemon=True)
                self.thread.start()
            except Exception as e:
                print("Error starting host:", e)
        else:
            try:
                self.sock.connect((self.host_ip, SERVER_PORT))
                self.conn = self.sock
                self.connected = True
                print("Connected to host:", self.host_ip)
                self.thread = threading.Thread(target=self.receive_loop, daemon=True)
                self.thread.start()
            except Exception as e:
                print("Error connecting to host:", e)

    def send(self, message_dict):
        if self.connected:
            try:
                msg = json.dumps(message_dict) + "\n"
                self.conn.sendall(msg.encode('utf-8'))
            except Exception as e:
                print("Error sending message:", e)

    def receive_loop(self):
        buffer = ""
        while self.connected:
            try:
                data = self.conn.recv(1024)
                if not data:
                    self.connected = False
                    break
                buffer += data.decode('utf-8')
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    try:
                        msg = json.loads(line)
                        self.received_messages.append(msg)
                    except Exception as e:
                        print("Error decoding message:", e)
            except Exception as e:
                print("Error in receive loop:", e)
                self.connected = False

    def get_messages(self):
        msgs = self.received_messages[:]
        self.received_messages = []
        return msgs

    def close(self):
        self.connected = False
        self.sock.close()

# ----------------------- UI Elements -----------------------
class TextInputBox:
    def __init__(self, x, y, w, h, font, mask=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text = ""
        self.mask = mask
        self.active = False
        self.cursor_visible = True
        self.cursor_counter = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return "ENTER"
            else:
                if event.unicode.isdigit() and len(self.text) < 4:
                    self.text += event.unicode
        return None

    def update(self):
        self.cursor_counter += 1
        if self.cursor_counter >= FPS // 2:
            self.cursor_counter = 0
            self.cursor_visible = not self.cursor_visible

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        disp = self.text if not self.mask else "*" * len(self.text)
        txt_surface = self.font.render(disp, True, BLACK)
        surface.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + txt_surface.get_width() + 2
            cursor_y = self.rect.y + 5
            pygame.draw.line(surface, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + self.font.get_height()))

class Button:
    def __init__(self, rect, text, font, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if click_sound:
                click_sound.play()
            self.callback()

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        draw_text(surface, self.text, self.font, BLACK, self.rect.center, center=True)

# ----------------------- Game Class & States -----------------------
class Game:
    def __init__(self):
        # Game states: main_menu, local, online_host, online_join, enter_secret, switch_player, guessing, pause, game_over, info_terms, info_copyright, info_credits, leagues
        self.game_state = "main_menu"
        self.current_player = 1
        self.secrets = {1: None, 2: None}
        self.feedback = ""
        self.winner = None
        # Each player's guess history
        self.history = {1: [], 2: []}
        # Leaderboard (for wins) and league classification
        self.leaderboard = {}  # {player_name: wins}
        self.leagues = {}      # {league_name: [player_names]}
        # Networking
        self.online_mode = False
        self.is_host = False
        self.host_ip = ""
        self.network = None
        # Input box for secret entry and guesses
        self.input_box = TextInputBox(WIDTH // 2 - 50, 430, 100, 40, FONT, mask=False)
        self.input_box.active = True
        self.switch_message = ""
        self.menu_buttons = []
        self.create_menu_buttons()
        # Info text for T&C, Copyright, Credits, Leagues screens
        self.info_text = ""
    
    def create_menu_buttons(self):
        # Adjusted positions for multiple buttons in main menu
        self.menu_buttons = [
            Button((WIDTH // 2 - 100, 140, 200, 40), "Local Game", FONT, self.start_local_game),
            Button((WIDTH // 2 - 100, 190, 200, 40), "Online Host", FONT, self.start_online_host),
            Button((WIDTH // 2 - 100, 240, 200, 40), "Online Join", FONT, self.start_online_join),
            Button((WIDTH // 2 - 100, 290, 200, 40), "Leagues", FONT, self.show_leagues),
            Button((WIDTH // 2 - 100, 340, 200, 40), "Terms & Conditions", FONT, self.show_terms),
            Button((WIDTH // 2 - 100, 390, 200, 40), "Copyright", FONT, self.show_copyright),
            Button((WIDTH // 2 - 100, 440, 200, 40), "Credits", FONT, self.show_credits),
            Button((WIDTH // 2 - 100, 490, 200, 40), "Quit", FONT, self.quit_game)
        ]

    def start_local_game(self):
        self.online_mode = False
        self.start_secret_phase()

    def start_online_host(self):
        self.online_mode = True
        self.is_host = True
        self.network = NetworkHandler(is_host=True)
        self.network.start()
        self.start_secret_phase()

    def start_online_join(self):
        self.online_mode = True
        self.is_host = False
        self.host_ip = input("Enter host IP address: ")
        self.network = NetworkHandler(is_host=False, host_ip=self.host_ip)
        self.network.start()
        self.start_secret_phase()

    def start_secret_phase(self):
        self.secrets = {1: None, 2: None}
        self.history = {1: [], 2: []}
        self.feedback = ""
        self.input_box.text = ""
        self.input_box.mask = True
        self.input_box.active = True
        self.game_state = "enter_secret"

    def show_terms(self):
        self.info_text = "Terms & Conditions:\n\nBy playing this game, you agree to our terms. [Full T&C here]"
        self.game_state = "info_terms"

    def show_copyright(self):
        self.info_text = "Copyright Notice:\n\nAll game assets are properly licensed. [Details here]"
        self.game_state = "info_copyright"

    def show_credits(self):
        self.info_text = ("Credits & Attributions:\n\n"
                          "Background Music: bg_music.mp3 (CC BY-NC 4.0)\n"
                          "Click Sound: click.wav (CC BY-NC 4.0)\n"
                          "Correct Sound: correct.wav (CC BY-NC 4.0)\n"
                          "Win Sound: win.wav (CC BY-NC 4.0)\n"
                          "Error Sound: error.wav (CC BY-NC 4.0)\n"
                          "Background Image: background.png [Source/Attribution]\n"
                          "Custom Font: custom_font.ttf [Source/Attribution]")
        self.game_state = "info_credits"

    def show_leagues(self):
        self.game_state = "leagues"

    def quit_game(self):
        if self.network:
            self.network.close()
        pygame.quit()
        sys.exit()

    def classify_league(self, wins):
        if wins < 5:
            return "Bronze League"
        elif wins < 10:
            return "Silver League"
        else:
            return "Gold League"

    def update_leagues(self):
        # Update league classification based on leaderboard wins
        self.leagues = {"Bronze League": [], "Silver League": [], "Gold League": []}
        for name, wins in self.leaderboard.items():
            league = self.classify_league(wins)
            self.leagues[league].append((name, wins))
        # Sort each league by wins descending
        for league in self.leagues:
            self.leagues[league].sort(key=lambda x: x[1], reverse=True)

    def process_network_messages(self):
        if self.online_mode and self.network:
            msgs = self.network.get_messages()
            for msg in msgs:
                if msg["type"] == "SECRET":
                    opp = 2 if self.current_player == 1 else 1
                    self.secrets[opp] = msg["data"]
                    print(f"Received secret for player {opp}")
                elif msg["type"] == "GUESS":
                    opp = 2 if self.current_player == 1 else 1
                    guess = msg["data"]
                    dead, injured = evaluate_guess(self.secrets[self.current_player], guess)
                    self.feedback = f"Opponent guessed {guess}: {dead}D, {injured}I"
                    self.history[opp].append(f"{guess} → {dead}D, {injured}I")
                    self.game_state = "guessing"
                elif msg["type"] == "CHAT":
                    print("Chat:", msg["data"])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            if self.game_state.startswith("info_") or self.game_state == "leagues":
                if event.type == pygame.KEYDOWN:
                    self.game_state = "main_menu"
                continue

            if self.game_state == "main_menu":
                for btn in self.menu_buttons:
                    btn.handle_event(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.show_credits()

            elif self.game_state == "enter_secret":
                ret = self.input_box.handle_event(event)
                if ret == "ENTER":
                    if is_valid_number(self.input_box.text):
                        self.secrets[self.current_player] = self.input_box.text
                        if self.online_mode:
                            self.network.send({"type": "SECRET", "data": self.input_box.text})
                        self.input_box.text = ""
                        self.input_box.active = False
                        self.switch_message = (f"Player {self.current_player} secret recorded.\n"
                                               f"Pass the device to the other player.\n"
                                               "Press any key to continue.")
                        self.game_state = "switch_player"
                    else:
                        self.feedback = "Invalid number! Must be 4 unique digits."
                        if error_sound:
                            error_sound.play()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.quit_game()

            elif self.game_state == "switch_player":
                if event.type == pygame.KEYDOWN:
                    fade_transition()
                    if self.secrets[1] is None or self.secrets[2] is None:
                        self.current_player = 2 if self.current_player == 1 else 1
                        self.input_box.mask = True
                        self.input_box.text = ""
                        self.input_box.active = True
                        self.game_state = "enter_secret"
                    else:
                        self.input_box.mask = False
                        self.input_box.text = ""
                        self.input_box.active = True
                        self.feedback = ""
                        self.game_state = "guessing"

            elif self.game_state == "guessing":
                ret = self.input_box.handle_event(event)
                if ret == "ENTER":
                    guess = self.input_box.text
                    if is_valid_number(guess):
                        opponent = 2 if self.current_player == 1 else 1
                        dead, injured = evaluate_guess(self.secrets[opponent], guess)
                        self.feedback = f"Result: {dead}D, {injured}I"
                        if correct_sound:
                            correct_sound.play()
                        entry = f"{guess} → {dead}D, {injured}I"
                        self.history[self.current_player].append(entry)
                        if self.online_mode:
                            self.network.send({"type": "GUESS", "data": guess})
                        if dead == 4:
                            self.winner = self.current_player
                            self.game_state = "game_over"
                            if win_sound:
                                win_sound.play()
                            name = f"Player{self.current_player}"
                            self.leaderboard[name] = self.leaderboard.get(name, 0) + 1
                            self.update_leagues()
                        else:
                            self.switch_message = (f"Player {self.current_player}'s guess: {guess}\n"
                                                   f"Result: {dead}D, {injured}I\n"
                                                   f"Pass the device to Player {opponent} and press any key to continue.")
                            self.game_state = "switch_player"
                            self.current_player = opponent
                        self.input_box.text = ""
                        self.input_box.active = False
                    else:
                        self.feedback = "Invalid guess! Must be 4 unique digits."
                        if error_sound:
                            error_sound.play()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.quit_game()

            elif self.game_state == "pause":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    fade_transition()
                    self.game_state = "guessing"

            elif self.game_state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        fade_transition()
                        self.game_state = "main_menu"
                    elif event.key == pygame.K_q:
                        self.quit_game()

            # Process network messages in online mode
            if self.online_mode and self.network:
                self.process_network_messages()

    def update(self):
        if self.game_state in ["enter_secret", "guessing"]:
            self.input_box.update()

    def draw_history(self):
        max_entries = 8
        y_start = 110
        x1 = 20
        for i, entry in enumerate(self.history[1][-max_entries:]):
            draw_text(screen, entry, SMALL_FONT, BLACK, (x1, y_start + i * 25))
        x2 = WIDTH // 2 + 20
        for i, entry in enumerate(self.history[2][-max_entries:]):
            draw_text(screen, entry, SMALL_FONT, BLACK, (x2, y_start + i * 25))

    def draw_info(self):
        draw_background()
        y = 50
        for line in self.info_text.split("\n"):
            draw_text(screen, line, SMALL_FONT, BLACK, (20, y))
            y += 30
        draw_text(screen, "Press any key to return", SMALL_FONT, DARKGRAY, (WIDTH//2, HEIGHT-30), center=True)

    def draw_leagues(self):
        draw_background()
        draw_text(screen, "Leagues", TITLE_FONT, BLUE, (WIDTH//2, 30), center=True)
        y = 100
        for league, players in self.leagues.items():
            draw_text(screen, league, FONT, BLACK, (50, y))
            y += 40
            for name, wins in players:
                draw_text(screen, f"{name}: {wins} wins", SMALL_FONT, BLACK, (70, y))
                y += 30
            y += 20
        draw_text(screen, "Press any key to return", SMALL_FONT, DARKGRAY, (WIDTH//2, HEIGHT-30), center=True)

    def draw(self):
        if self.game_state in ["guessing", "game_over"]:
            draw_background()
            draw_text(screen, "Dead and Injured", TITLE_FONT, BLUE, (WIDTH//2, 30), center=True)
            pygame.draw.line(screen, BLACK, (50, 70), (WIDTH-50, 70), 2)
            pygame.draw.line(screen, BLACK, (WIDTH//2, 70), (WIDTH//2, 350), 2)
            draw_text(screen, "Player 1", FONT, BLACK, (WIDTH//4, 80), center=True)
            draw_text(screen, "Player 2", FONT, BLACK, (3*WIDTH//4, 80), center=True)
            self.draw_history()
            self.input_box.draw(screen)
            draw_text(screen, "Enter your guess:", SMALL_FONT, BLACK, (WIDTH//2 - 100, 370))
            if self.feedback:
                draw_text(screen, self.feedback, SMALL_FONT, RED, (WIDTH//2 - 100, 410))
            draw_text(screen, "Press P to pause, ESC to quit", SMALL_FONT, DARKGRAY, (WIDTH//2, 450), center=True)
            if self.game_state == "game_over":
                draw_text(screen, f"Game Over! Player {self.winner} wins!", TITLE_FONT, GREEN, (WIDTH//2, 30), center=True)
        elif self.game_state.startswith("info_"):
            self.draw_info()
        elif self.game_state == "leagues":
            self.draw_leagues()
        else:
            draw_background()
            if self.game_state == "main_menu":
                draw_text(screen, "Dead and Injured", TITLE_FONT, BLUE, (WIDTH//2, 100), center=True)
                draw_text(screen, "Press C for Credits", SMALL_FONT, DARKGRAY, (WIDTH//2, 150), center=True)
                for btn in self.menu_buttons:
                    btn.draw(screen)
            elif self.game_state == "enter_secret":
                draw_text(screen, f"Player {self.current_player}: Enter your secret 4-digit number", FONT, BLACK, (50, 150))
                draw_text(screen, "(Digits must be unique)", SMALL_FONT, DARKGRAY, (50, 200))
                self.input_box.draw(screen)
                if self.feedback:
                    draw_text(screen, self.feedback, SMALL_FONT, RED, (50, 320))
                draw_text(screen, "Press ESC to quit", SMALL_FONT, DARKGRAY, (50, 370))
            elif self.game_state == "switch_player":
                y = 150
                for line in self.switch_message.split("\n"):
                    draw_text(screen, line, FONT, BLACK, (50, y))
                    y += 40
                draw_text(screen, "Press any key to continue...", SMALL_FONT, DARKGRAY, (50, y+20))
            elif self.game_state == "pause":
                draw_text(screen, "Game Paused", TITLE_FONT, BLUE, (WIDTH//2, HEIGHT//2 - 50), center=True)
                draw_text(screen, "Press P to resume", FONT, BLACK, (WIDTH//2, HEIGHT//2 + 20), center=True)

    def run(self):
        running = True
        while running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(FPS)

# ----------------------- Utility -----------------------
def is_valid_number(num_str):
    return len(num_str) == 4 and num_str.isdigit() and len(set(num_str)) == 4

def evaluate_guess(secret, guess):
    dead = sum(1 for i in range(4) if guess[i] == secret[i])
    matching = sum(1 for digit in guess if digit in secret)
    return dead, matching - dead

# ----------------------- Main -----------------------
def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
