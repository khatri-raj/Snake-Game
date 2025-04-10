import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modern Snake Game")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.color = GREEN
        self.score = 0
        self.speed = 10

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        if new in self.positions[3:]:
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0
        self.speed = 10

    def render(self, surface):
        for i, p in enumerate(self.positions):
            color = [max(0, self.color[0] - i * 2),
                    max(0, self.color[1] - i * 2),
                    max(0, self.color[2] - i * 2)]
            r = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE),
                          (GRID_SIZE - 2, GRID_SIZE - 2))
            pygame.draw.rect(surface, color, r)
            pygame.draw.rect(surface, BLACK, r, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1),
                        random.randint(0, GRID_HEIGHT - 1))

    def render(self, surface):
        r = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
                       (GRID_SIZE - 2, GRID_SIZE - 2))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, BLACK, r, 1)

class PowerUp:
    def __init__(self):
        self.position = (0, 0)
        self.color = YELLOW
        self.active = False
        self.timer = 0

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1),
                        random.randint(0, GRID_HEIGHT - 1))
        self.active = True
        self.timer = 150  # Power-up will disappear after 150 frames

    def render(self, surface):
        if self.active:
            r = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
                           (GRID_SIZE - 2, GRID_SIZE - 2))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)

def main():
    snake = Snake()
    food = Food()
    power_up = PowerUp()
    font = pygame.font.Font(None, 36)
    game_over_font = pygame.font.Font(None, 72)

    running = True
    game_over = False
    power_up_active = False
    power_up_timer = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        game_over = False
                        power_up_active = False
                else:
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)

        if not game_over:
            # Update game state
            if not snake.update():
                game_over = True

            # Check for food collision
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 10
                food.randomize_position()
                if random.random() < 0.3 and not power_up.active:  # 30% chance to spawn power-up
                    power_up.randomize_position()

            # Check for power-up collision
            if power_up.active:
                if snake.get_head_position() == power_up.position:
                    power_up_active = True
                    power_up_timer = 300  # Power-up effect lasts 300 frames
                    power_up.active = False
                    snake.speed += 5
                power_up.timer -= 1
                if power_up.timer <= 0:
                    power_up.active = False

            # Update power-up effect
            if power_up_active:
                power_up_timer -= 1
                if power_up_timer <= 0:
                    power_up_active = False
                    snake.speed = max(10, snake.speed - 5)

        # Render
        screen.fill(BLACK)
        
        # Draw grid
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

        snake.render(screen)
        food.render(screen)
        if power_up.active:
            power_up.render(screen)

        # Draw score
        score_text = font.render(f"Score: {snake.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw speed
        speed_text = font.render(f"Speed: {snake.speed}", True, WHITE)
        screen.blit(speed_text, (10, 50))

        if game_over:
            game_over_text = game_over_font.render("GAME OVER!", True, RED)
            restart_text = font.render("Press SPACE to restart", True, WHITE)
            screen.blit(game_over_text, 
                       (WIDTH // 2 - game_over_text.get_width() // 2, 
                        HEIGHT // 2 - game_over_text.get_height() // 2))
            screen.blit(restart_text, 
                       (WIDTH // 2 - restart_text.get_width() // 2, 
                        HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(snake.speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
