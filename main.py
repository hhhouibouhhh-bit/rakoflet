# snake_mobile_french.py - لعبة ثعبان للهاتف (أزرار لمس)
import pygame
import random
import sys
import base64
from io import BytesIO

# --- تهيئة pygame ---
pygame.init()

# --- إعدادات الشاشة (مثالية للهاتف) ---
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
CELL_SIZE = 25
CELL_NUMBER_X = SCREEN_WIDTH // CELL_SIZE
CELL_NUMBER_Y = (SCREEN_HEIGHT - 200) // CELL_SIZE  # ترك مساحة للأزرار

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake - Tête de Lion")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

# --- رأس الأسد (Base64) ---
LION_HEAD_BASE64 = """
iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAYAAADE6YVjAAAACXBIWXMAAAsTAAALEwEAmpwYAAAF
KGlDQ1BQaG90b3Nob3AgSUNDIHByb2ZpbGUAAHjarZG9SgNBEMZfMUQUpLFFsDCZCLSxjYVYCGJh
EQk28gObLCF3c5IcPLk45wRC4Q/wBl6B2ngD72LhD3gDgYCXiJid3G1MlAiGnd35vZmdD4Zoq6r7
YhHlZS2xJ6JYtKuK2m21Ig88I0DAmKZq1tXu2Z17dOJXvM84z2cRJ2VZ03Q8x1O8wBtcYI45Zphh
hrOY4QxTnOEYx5jiAKc4wT5mOMUZzjDDGc5xgQv0cI4LXKCHc1zgEj1c4Ao9XKGPc1zjBj1c4hJ9
XKOPK1zjFje4xR0GuMc9BnjAAx7xiD4e8IAHPKCPBzzhEU94xjOe0McTnvGMFzzjBa94wzve8I4P
fOATX/jEF77xg1/8AUDrRz4KZW5kc3RyZWFtCmVuZG9iagoyNCAwIG9iago8PC9MZW5ndGggMTYx
L0ZpbHRlci9GbGF0ZURlY29kZT4+c3RyZWFtCnjaPcuxCoAgFIXhVwhz6RAyXaIu0aZB0KZDp07R
r0On/k+nQxDvcDgcDi4551xyySnlnFLOKaecUs455ZxTzjnlnFPOOeWcU8455ZxTzjnl/FfOu8fe
3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e
3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e
3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e
3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e
3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e
3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e
3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e
3t7e3t7e3t7e3t......
"""

# --- تحويل Base64 إلى صورة ---
def create_lion_head():
    try:
        image_data = base64.b64decode(LION_HEAD_BASE64)
        image_stream = BytesIO(image_data)
        lion = pygame.image.load(image_stream)
        return pygame.transform.scale(lion, (CELL_SIZE, CELL_SIZE))
    except:
        lion = pygame.Surface((CELL_SIZE, CELL_SIZE))
        lion.fill((200, 100, 0))
        pygame.draw.circle(lion, (255, 200, 0), (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//2)
        pygame.draw.circle(lion, (0, 0, 0), (CELL_SIZE//2 - 5, CELL_SIZE//2 - 3), 3)
        pygame.draw.circle(lion, (0, 0, 0), (CELL_SIZE//2 + 5, CELL_SIZE//2 - 3), 3)
        pygame.draw.rect(lion, (0, 0, 0), (CELL_SIZE//2 - 3, CELL_SIZE//2 + 2, 6, 2))
        return lion

lion_head_img = create_lion_head()

# --- الألوان ---
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
TRANSPARENT_GRAY = (100, 100, 100, 100)  # شبه شفاف
BUTTON_COLOR = (70, 130, 180, 180)        # أزرار شبه شفافة
BUTTON_HOVER = (100, 160, 200, 200)

# --- التفاحة ---
apple_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
apple_img.fill(RED)
pygame.draw.circle(apple_img, RED, (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//2 - 2)
pygame.draw.line(apple_img, (0, 0, 0), (CELL_SIZE//2, 2), (CELL_SIZE//2, 6), 2)

# --- ثعبان ---
class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [[10, 10], [9, 10], [8, 10]]
        self.direction = "RIGHT"
        self.new_direction = "RIGHT"
        self.growing = False

    def move(self):
        self.direction = self.new_direction
        head = self.body[0][:]
        if self.direction == "RIGHT": head[0] += 1
        if self.direction == "LEFT": head[0] -= 1
        if self.direction == "UP": head[1] -= 1
        if self.direction == "DOWN": head[1] += 1
        self.body.insert(0, head)
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def change_direction(self, direction):
        if direction == "RIGHT" and self.direction != "LEFT":
            self.new_direction = "RIGHT"
        if direction == "LEFT" and self.direction != "RIGHT":
            self.new_direction = "LEFT"
        if direction == "UP" and self.direction != "DOWN":
            self.new_direction = "UP"
        if direction == "DOWN" and self.direction != "UP":
            self.new_direction = "DOWN"

    def draw(self, surface):
        head_x, head_y = self.body[0]
        surface.blit(lion_head_img, (head_x * CELL_SIZE, head_y * CELL_SIZE))
        for segment in self.body[1:]:
            x, y = segment[0] * CELL_SIZE, segment[1] * CELL_SIZE
            pygame.draw.rect(surface, DARK_GREEN, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, GREEN, (x+2, y+2, CELL_SIZE-4, CELL_SIZE-4))

# --- التفاحة ---
class Apple:
    def __init__(self):
        self.position = [0, 0]
        self.randomize()

    def randomize(self):
        self.position = [
            random.randint(0, CELL_NUMBER_X - 1),
            random.randint(0, CELL_NUMBER_Y - 1)
        ]

    def draw(self, surface):
        x = self.position[0] * CELL_SIZE
        y = self.position[1] * CELL_SIZE
        surface.blit(apple_img, (x, y))

# --- زر شبه شفاف ---
class Button:
    def __init__(self, text, x, y, w, h, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.hover_color = hover_color
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)  # دعم الشفافية

    def draw(self, screen_surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        # رسم الزر شبه الشفاف
        btn_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(btn_surface, color, (0, 0, self.rect.width, self.rect.height), border_radius=15)
        pygame.draw.rect(btn_surface, WHITE + (180,), (0, 0, self.rect.width, self.rect.height), 2, border_radius=15)
        text_surf = small_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=(self.rect.width//2, self.rect.height//2))
        btn_surface.blit(text_surf, text_rect)
        screen_surface.blit(btn_surface, self.rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# --- زر إعادة التشغيل (في شاشة النهاية) ---
def show_game_over(score):
    screen.fill(BLACK)
    game_over = font.render("Jeu Terminé !", True, RED)
    score_text = font.render(f"Score : {score}", True, WHITE)
    screen.blit(game_over, (SCREEN_WIDTH//2 - game_over.get_width()//2, 200))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 280))

    restart_btn = Button("Rejouer", SCREEN_WIDTH//2 - 100, 380, 90, 50, (70, 130, 180, 180), (100, 160, 200, 200))
    quit_btn = Button("Quitter", SCREEN_WIDTH//2 + 10, 380, 90, 50, (200, 50, 50, 180), (220, 80, 80, 200))
    restart_btn.draw(screen)
    quit_btn.draw(screen)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if restart_btn.is_clicked(event):
                return True
            if quit_btn.is_clicked(event):
                pygame.quit()
                sys.exit()

# --- شاشة البداية ---
def show_start_screen():
    screen.fill(BLACK)
    title = font.render("Snake", True, GREEN)
    subtitle = font.render("Tête de Lion", True, (255, 200, 0))
    instruction = small_font.render("Touchez pour commencer", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 200))
    screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 260))
    screen.blit(instruction, (SCREEN_WIDTH//2 - instruction.get_width()//2, 340))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# --- الدالة الرئيسية ---
def main():
    snake = Snake()
    apple = Apple()
    score = 0
    game_over = False

    show_start_screen()

    # --- إنشاء أزرار التحكم ---
    btn_size = 100
    padding = 20
    center_x = SCREEN_WIDTH // 2

    up_btn = Button("↑", center_x - btn_size//2, SCREEN_HEIGHT - 150, btn_size, btn_size, (100, 100, 100, 160), (140, 140, 140, 200))
    left_btn = Button("←", padding, SCREEN_HEIGHT - 80, btn_size, btn_size, (100, 100, 100, 160), (140, 140, 140, 200))
    right_btn = Button("→", SCREEN_WIDTH - btn_size - padding, SCREEN_HEIGHT - 80, btn_size, btn_size, (100, 100, 100, 160), (140, 140, 140, 200))
    down_btn = Button("↓", center_x - btn_size//2, SCREEN_HEIGHT - 80, btn_size, btn_size, (100, 100, 100, 160), (140, 140, 140, 200))

    while True:
        if game_over:
            if show_game_over(score):
                snake.reset()
                apple.randomize()
                score = 0
                game_over = False
            continue

        screen.fill(BLACK)

        # --- معالجة الأحداث ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if up_btn.is_clicked(event): snake.change_direction("UP")
                if down_btn.is_clicked(event): snake.change_direction("DOWN")
                if left_btn.is_clicked(event): snake.change_direction("LEFT")
                if right_btn.is_clicked(event): snake.change_direction("RIGHT")

        # --- التحرك ---
        snake.move()

        # --- أكل التفاحة ---
        if snake.body[0] == apple.position:
            snake.growing = True
            apple.randomize()
            score += 10
            while apple.position in snake.body:
                apple.randomize()

        # --- التصادم ---
        head = snake.body[0]
        if (head[0] < 0 or head[0] >= CELL_NUMBER_X or
            head[1] < 0 or head[1] >= CELL_NUMBER_Y or
            head in snake.body[1:]):
            game_over = True

        # --- الرسم ---
        snake.draw(screen)
        apple.draw(screen)

        # --- عرض النقاط ---
        score_text = small_font.render(f"Score : {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # --- رسم الأزرار ---
        up_btn.draw(screen)
        left_btn.draw(screen)
        right_btn.draw(screen)
        down_btn.draw(screen)

        pygame.display.update()
        clock.tick(10)

# --- تشغيل اللعبة ---
if __name__ == "__main__":
    main()
