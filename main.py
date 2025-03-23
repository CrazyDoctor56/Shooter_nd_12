import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.font.init()

# SETTING
HEIGHT = 700
WIDTH = 1200
FPS = 60

# COLOR
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# GLOBAL
score = 0
lost = 0

medium_font = pygame.font.SysFont("Arial", 36)

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")

background = pygame.transform.scale(pygame.image.load("galaxy.jpg"),
             (WIDTH, HEIGHT))

pygame.mixer.music.load("space.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()

clock = pygame.time.Clock()

bullets = pygame.sprite.Group()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename: str, size: tuple[int, int], coords: tuple[int, int], speed: int):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(filename), size)
        self.rect = self.image.get_rect(center=coords)
        self.speed = speed

    def reset(self, sc: pygame.Surface):
        sc.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

        if keys[pygame.K_x]:
            self.fire()

    def fire(self):
        new_bullet = bullet("bullet.png", (15, 20), (self.rect.centerx, self.rect.top), 9)
        bullets.add(new_bullet)
        pygame.mixer.Sound("fire.ogg").play()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(self.rect.width, WIDTH - self.rect.width)

            global lost
            lost += 1

class bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

player = Player("rocket.png", (50, 70), (WIDTH // 2, HEIGHT // 2), 5)

enemies = pygame.sprite.Group()
enemies_num = 4
for i in range(enemies_num):
    new_enemy = Enemy("ufo.png", (70, 50),
                (random.randint(50, WIDTH - 50),
                0),
                random.randint(5, 8))
    
    enemies.add(new_enemy)


game = True
finish = False

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            player.fire()

    if not finish:
        sc.blit(background, (0, 0))
        lost_text = medium_font.render(f"Lost: {lost}", True, WHITE)
        sc.blit(lost_text, (10, 10))
        score_text = medium_font.render(f"Score: {score}", True, WHITE)
        sc.blit(score_text, (WIDTH - 150, 10))

        player.update()
        player.reset(sc)

        enemies.update()
        enemies.draw(sc)

        bullets.update()
        bullets.draw(sc)
    
    pygame.display.update()
    clock.tick(FPS)