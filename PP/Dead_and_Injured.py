import pygame
import sys
import os

# ----------------------- Initialization -----------------------
pygame.init()
pygame.mixer.init()
pygame.font.init()

# ----------------------- Global Constants -----------------------
WIDTH, HEIGHT = 600, 500
FPS = 30

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

# ----------------------- Load Background -----------------------
def load_background():
    bg_path = os.path.join("assets", "background.png")
    if os.path.exists(bg_path):
        bg = pygame.image.load(bg_path).convert()
        return pygame.transform.scale(bg, (WIDTH, HEIGHT))
    return None

background_image = load_background()

def draw_background():
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(WHITE)

# ----------------------- Load Fonts -----------------------
font_path = os.path.join("assets", "custom_font.ttf")
if os.path.exists(font_path):
    FONT = pygame.font.Font(font_path, 36)
    SMALL_FONT = pygame.font.Font(font_path, 28)
    TITLE_FONT = pygame.font.Font(font_path, 64)
else:
    FONT = pygame.font.Font(None, 36)
    SMALL_FONT = pygame.font.Font(None, 28)
    TITLE_FONT = pygame.font.Font(None, 64)

# ----------------------- Sound Setup -----------------------
sound_files = {
    "bg_music": {"file": os.path.join("assets", "sounds", "bg_music.mp3"), "desc": "Background music (loops continuously)"},
    "click":    {"file": os.path.join("assets", "sounds", "click.wav"),      "desc": "Button click sound"},
    "correct":  {"file": os.path.join("assets", "sounds", "correct.wav"),    "desc": "Sound for a correct guess"},
    "win":      {"file": os.path.join("assets", "sounds", "win.wav"),        "desc": "Sound played when a player wins"},
    "error":    {"file": os.path.join("assets", "sounds", "error.wav"),      "desc": "Sound played on invalid input"}
}

def load_sound(sound_key):
    try:
        sound_path = sound_files[sound_key]["file"]
        if os.path.exists(sound_path):
            return pygame.mixer.Sound(sound_path)
        else:
            print(f"Warning: '{sound_key}' sound file not found at {sound_path}.")
            return None
    except Exception as e:
        print(f"Error loading sound '{sound_key}': {e}")
        return None

# Load background music (using pygame.mixer.music)
bg_music_path = sound_files["bg_music"]["file"]
if os.path.exists(bg_music_path):
    try:
        pygame.mixer.music.load(bg_music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Warning: Could not load background music.")
else:
    print("Warning: Background music file not found.")

click_sound   = load_sound("click")
correct_sound = load_sound("correct")
win_sound     = load_sound("win")
error_sound   = load_sound("error")

# ----------------------- Helper Functions -----------------------
def draw_text(surface, text, font, color, pos, center=False):
    text_surf = font.render(text, True, color)
    if center:
        text_rect = text_surf.get_rect(center=pos)
    else:
        text_rect = text_surf.get_rect(topleft=pos)
    surface.blit(text_surf, text_rect)

def is_valid_number(num_str):
    """Return True if num_str is a 4-digit number with all unique digits."""
    return len(num_str) == 4 and num_str.isdigit() and len(set(num_str)) == 4

def evaluate_guess(secret, guess):
    """Return a tuple (dead, injured) comparing guess to secret."""
    dead = sum(1 for i in range(4) if guess[i] == secret[i])
    matching = sum(1 for digit in guess if digit in secret)
    return dead, matching - dead

def fade_transition(duration=0.5):
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(BLACK)
    steps = int(FPS * duration)
    # Fade out
    for alpha in range(0, 256, int(256/steps)):
        fade.set_alpha(alpha)
        draw_background()
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)
    # Fade in
    for alpha in range(255, -1, -int(256/steps)):
        fade.set_alpha(alpha)
        draw_background()
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

# ----------------------- UI Classes -----------------------
class TextInputBox:
    def __init__(self, x, y, w, h, font, mask=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = ""
        self.font = font
        self.active = False
        self.mask = mask  # If True, display asterisks instead of actual text.
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
        pygame.draw.rect(surface, self.color, self.rect, 2)
        display_text = self.text if not self.mask else "*" * len(self.text)
        txt_surface = self.font.render(display_text, True, BLACK)
        surface.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + txt_surface.get_width() + 2
            cursor_y = self.rect.y + 5
            pygame.draw.line(surface, BLACK, (cursor_x, cursor_y),
                             (cursor_x, cursor_y + self.font.get_height()))

class Button:
    def __init__(self, rect, text, font, callback, bg_color=GRAY, text_color=BLACK):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.bg_color = bg_color
        self.text_color = text_color

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if click_sound:
                click_sound.play()
            self.callback()

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        draw_text(surface, self.text, self.font, self.text_color, self.rect.center, center=True)

# ----------------------- Game Class & States -----------------------
class Game:
    def __init__(self):
        # Game states: main_menu, enter_secret, switch_player, guessing, pause, game_over
        self.game_state = "main_menu"
        self.current_player = 1
        self.secrets = {1: None, 2: None}
        self.feedback = ""
        self.winner = None
        # Separate history for each player's guesses
        self.history = {1: [], 2: []}
        # Input box positioned near the bottom center for guesses
        self.input_box = TextInputBox(WIDTH // 2 - 50, 430, 100, 40, FONT, mask=False)
        self.input_box.active = True
        self.switch_message = ""
        self.menu_buttons = []
        self.create_menu_buttons()

    def create_menu_buttons(self):
        self.menu_buttons = [
            Button((WIDTH // 2 - 100, 250, 200, 50), "Start Game", FONT, self.start_game),
            Button((WIDTH // 2 - 100, 320, 200, 50), "Quit", FONT, self.quit_game)
        ]

    def start_game(self):
        self.secrets = {1: None, 2: None}
        self.current_player = 1
        self.feedback = ""
        self.history = {1: [], 2: []}  # Reset histories
        self.input_box.text = ""
        self.input_box.mask = True  # For secret entry
        self.input_box.active = True
        self.game_state = "enter_secret"

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            # Global pause during guessing state
            if event.type == pygame.KEYDOWN and self.game_state == "guessing" and event.key == pygame.K_p:
                self.game_state = "pause"

            if self.game_state == "main_menu":
                for btn in self.menu_buttons:
                    btn.handle_event(event)

            elif self.game_state == "enter_secret":
                ret = self.input_box.handle_event(event)
                if ret == "ENTER":
                    if is_valid_number(self.input_box.text):
                        self.secrets[self.current_player] = self.input_box.text
                        self.input_box.text = ""
                        self.input_box.active = False
                        self.switch_message = (f"Player {self.current_player} secret recorded.\n"
                                               f"Pass the device to Player {2 if self.current_player == 1 else 1}.\n"
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
                        # Do NOT reset current_player here.
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
                        # Log guess and feedback in the current player's history
                        entry = f"{guess} → {dead}D, {injured}I"
                        self.history[self.current_player].append(entry)
                        if dead == 4:
                            self.winner = self.current_player
                            self.game_state = "game_over"
                            if win_sound:
                                win_sound.play()
                        else:
                            self.switch_message = (f"Player {self.current_player}'s guess: {guess}\n"
                                                   f"Result: {dead}D, {injured}I\n"
                                                   f"Pass the device to Player {opponent} and press any key to continue.")
                            self.game_state = "switch_player"
                            self.current_player = opponent  # Switch player after a guess
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

    def update(self):
        if self.game_state in ["enter_secret", "guessing"]:
            self.input_box.update()

    def draw_history(self):
        # Draw each player's guess history in their respective column.
        max_entries = 8  # Show up to 8 recent guesses
        y_start = 110
        # Left column for Player 1
        x1 = 20
        for i, entry in enumerate(self.history[1][-max_entries:]):
            draw_text(screen, entry, SMALL_FONT, BLACK, (x1, y_start + i * 25))
        # Right column for Player 2
        x2 = WIDTH // 2 + 20
        for i, entry in enumerate(self.history[2][-max_entries:]):
            draw_text(screen, entry, SMALL_FONT, BLACK, (x2, y_start + i * 25))

    def draw(self):
        if self.game_state in ["guessing", "game_over"]:
            # Notebook-style interface
            draw_background()
            # Title at the top
            draw_text(screen, "Dead and Injured", TITLE_FONT, BLUE, (WIDTH // 2, 30), center=True)
            # Horizontal line below title
            pygame.draw.line(screen, BLACK, (50, 70), (WIDTH - 50, 70), 2)
            # Vertical divider for two columns
            pygame.draw.line(screen, BLACK, (WIDTH // 2, 70), (WIDTH // 2, 350), 2)
            # Column labels
            draw_text(screen, "Player 1", FONT, BLACK, (WIDTH // 4, 80), center=True)
            draw_text(screen, "Player 2", FONT, BLACK, (3 * WIDTH // 4, 80), center=True)
            # Draw guess histories for each player
            self.draw_history()
            # Draw input box and instructions at the bottom
            self.input_box.draw(screen)
            draw_text(screen, "Enter your guess:", SMALL_FONT, BLACK, (WIDTH // 2 - 100, 370))
            if self.feedback:
                draw_text(screen, self.feedback, SMALL_FONT, RED, (WIDTH // 2 - 100, 410))
            draw_text(screen, "Press P to pause, ESC to quit", SMALL_FONT, DARKGRAY, (WIDTH // 2, 450), center=True)
        else:
            # Other states use simpler interfaces
            draw_background()
            if self.game_state == "main_menu":
                draw_text(screen, "Dead and Injured", TITLE_FONT, BLUE, (WIDTH // 2, 100), center=True)
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
                draw_text(screen, "Press any key to continue...", SMALL_FONT, DARKGRAY, (50, y + 20))
            elif self.game_state == "pause":
                draw_text(screen, "Game Paused", TITLE_FONT, BLUE, (WIDTH // 2, HEIGHT // 2 - 50), center=True)
                draw_text(screen, "Press P to resume", FONT, BLACK, (WIDTH // 2, HEIGHT // 2 + 20), center=True)
        # In game_over, we use the notebook layout (with history shown)
        if self.game_state == "game_over":
            draw_text(screen, f"Game Over! Player {self.winner} wins!", TITLE_FONT, GREEN, (WIDTH // 2, 30), center=True)

    def run(self):
        running = True
        while running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(FPS)

# ----------------------- Main -----------------------
def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
