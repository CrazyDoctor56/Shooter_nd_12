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

# GLOBAL
score = 0
lost = 0
level = 1
level_threshold = 10

ammo = 10
max_ammo = 10
reloading = False
reload_time = 2000
reload_start_time = 0

medium_font = pygame.font.SysFont("Arial", 20)

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")

background = pygame.transform.scale(pygame.image.load("galaxy.jpg"), (WIDTH, HEIGHT))

pygame.mixer.music.load("space.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()

clock = pygame.time.Clock()

bullets = pygame.sprite.Group()
steroids = pygame.sprite.Group()

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
        global ammo, reloading, reload_start_time
        if not reloading and ammo > 0:
            new_bullet = Bullet("bullet.png", (15, 20), (self.rect.centerx, self.rect.top), 9)
            bullets.add(new_bullet)
            pygame.mixer.Sound("fire.ogg").play()
            ammo -= 1
            if ammo == 0:
                reloading = True
                reload_start_time = pygame.time.get_ticks()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(self.rect.width, WIDTH - self.rect.width)
            global lost
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Steroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

def create_enemies(count, level):
    group = pygame.sprite.Group()
    for _ in range(count):
        new_enemy = Enemy("ufo.png", (70, 50),
                (random.randint(50, WIDTH - 50), 0),
                random.randint(3, 5 + level))
        group.add(new_enemy)
    return group

def reset_game():
    global score, lost, level, enemies, ammo, reloading
    score = 0
    lost = 0
    level = 1
    ammo = max_ammo
    reloading = False
    player.rect.center = (WIDTH // 2, HEIGHT // 2)
    bullets.empty()
    steroids.empty()
    enemies.empty()
    enemies.add(create_enemies(4, level))

player = Player("rocket.png", (50, 70), (WIDTH // 2, HEIGHT // 2), 5)
enemies = create_enemies(4, level)

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
        score_text = medium_font.render(f"Score: {score}", True, WHITE)
        level_text = medium_font.render(f"Level: {level}", True, WHITE)

        sc.blit(lost_text, (10, 10))
        sc.blit(score_text, (WIDTH - 180, 10))
        sc.blit(level_text, (WIDTH // 2 - 50, 10))

        if reloading:
            current_time = pygame.time.get_ticks()
            if current_time - reload_start_time >= reload_time:
                reloading = False
                ammo = max_ammo

        player.update()
        player.reset(sc)

        enemies.update()
        enemies.draw(sc)

        bullets.update()
        bullets.draw(sc)

        steroids.update()
        steroids.draw(sc)

        if reloading:
            ammo_text = medium_font.render("Reloading...", True, WHITE)
        else:
            ammo_text = medium_font.render(f"Ammo: {ammo}", True, WHITE)
        sc.blit(ammo_text, (player.rect.centerx - ammo_text.get_width() // 2, player.rect.bottom + 10))

        collide = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for enemy in collide:
            score += 1
            if score % level_threshold == 0:
                level += 1
                enemies.add(create_enemies(1, level))

            new_enemy = Enemy("ufo.png", (70, 50),
                (random.randint(50, WIDTH - 50), 0),
                random.randint(3, 5 + level))
            enemies.add(new_enemy)

        if random.randint(1, 500) == 1:
            new_steroid = Steroid("asteroid.png", (40, 40),
                (random.randint(50, WIDTH - 50), 0), 3)
            steroids.add(new_steroid)

        hits = pygame.sprite.spritecollide(player, steroids, True)
        for steroid in hits:
            player.speed += 1

        if score >= 30:
            finish = True
            sc.fill(BLACK)
            text = medium_font.render("YOU WIN - Press R to Restart", True, WHITE)
            sc.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        if lost >= 30:
            finish = True
            sc.fill(BLACK)
            text = medium_font.render("YOU LOSE - Press R to Restart", True, WHITE)
            sc.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            finish = False
            reset_game()

    pygame.display.update()
    clock.tick(FPS)