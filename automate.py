import pygame
import random
import sys


pygame.init()


WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sid Runner")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


clock = pygame.time.Clock()


font = pygame.font.SysFont(None, 36)


dino_img = pygame.image.load("sidd.png")
dino_img = pygame.transform.scale(dino_img, (100, 100))


class Dino:
    def __init__(self):
        self.image = dino_img
        self.x = 50
        self.y = HEIGHT - 100
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.is_jumping = False
        self.jump_speed = 15
        self.gravity = 1
        self.velocity = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = -self.jump_speed

    def update(self):
        if self.is_jumping:
            self.y += self.velocity
            self.velocity += self.gravity
            if self.y >= HEIGHT - self.height - 60:
                self.y = HEIGHT - self.height - 60
                self.is_jumping = False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self):
        self.width = 30
        self.height = random.choice([30, 50])
        self.x = WIDTH
        self.y = HEIGHT - self.height - 60
        self.speed = 8

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))


def game():
    dino = Dino()
    obstacles = []
    score = 0
    running = True

    while running:
        clock.tick(60)
        screen.fill(WHITE)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()


        dino.update()

        if random.randint(1, 90) == 1:
            obstacles.append(Obstacle())

        for obstacle in list(obstacles):
            obstacle.update()
            if obstacle.x + obstacle.width < 0:
                obstacles.remove(obstacle)
                score += 1


            if (dino.x < obstacle.x + obstacle.width and
                dino.x + dino.width > obstacle.x and
                dino.y < obstacle.y + obstacle.height and
                dino.y + dino.height > obstacle.y):
                running = False


        dino.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)


        pygame.draw.line(screen, BLACK, (0, HEIGHT - 60), (WIDTH, HEIGHT - 60), 2)


        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()


    screen.fill(WHITE)
    msg = font.render(f"Game Over! Final Score: {score}", True, BLACK)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(3000)


if __name__ == "__main__":
    game()
