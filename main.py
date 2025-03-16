import pygame
import random
pygame.init()
pygame.mixer.init()

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

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")

background = pygame.transform.scale(pygame.image.load("galaxy.jpg"),
             (WIDTH, HEIGHT))

pygame.mixer.music.load("space.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()

clock = pygame.time.Clock()

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

    def fire(self):
        pass

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(self.rect.width, WIDTH - self.rect.width)

player = Player("rocket.png", (50, 70), (WIDTH // 2, HEIGHT // 2), 5)
enemy_test = Enemy("ufo.png", (70, 50), (random.randint(70, WIDTH - 70), 0), 8)

game = True
finish = False

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    if not finish:
        sc.blit(background, (0, 0))

        player.update()
        player.reset(sc)

        enemy_test.update()
        enemy_test.reset(sc)
    
    pygame.display.update()
    clock.tick(FPS)