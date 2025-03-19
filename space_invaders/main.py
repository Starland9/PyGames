import pygame
from pygame import mixer
import random


class Player:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("assets/images/player.png")
        self.x = screen.get_width() // 2 - self.image.get_width() // 2
        self.y = screen.get_height() - self.image.get_height() - 10
        self.speed = 5
        self.direction = 0

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.x += self.speed * self.direction
        if self.x < 0:
            self.x = 0
        if self.x > self.screen.get_width() - self.image.get_width():
            self.x = self.screen.get_width() - self.image.get_width()


class Enemy:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("assets/images/enemy.png")
        self.x = random.randint(0, screen.get_width() - self.image.get_width())
        self.y = random.randint(0, 100)
        self.speed = random.randint(1, 2)
        self.direction = random.choice([-1, 1])

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.x += self.speed * self.direction
        if self.x < 0 or self.x > self.screen.get_width() - self.image.get_width():
            self.direction *= -1
            self.y += random.randint(10, 20)
        if self.y > self.screen.get_height():
            self.x = random.randint(0, self.screen.get_width() - self.image.get_width())
            self.y = random.randint(0, 100)


class Bullet:
    def __init__(self, screen, player):
        self.screen = screen
        self.image = pygame.image.load("assets/images/bullet.png")
        self.x = player.x + player.image.get_width() // 2 - self.image.get_width() // 2
        self.y = player.y - self.image.get_height()
        self.speed = 10
        self.state = "ready"

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def update(self):
        if self.state == "fire":
            self.y -= self.speed
            if self.y < 0:
                self.state = "ready"


def has_bullet_collided_with_enemy(bullet, enemy):
    return (
        enemy.x <= bullet.x <= enemy.x + enemy.image.get_width()
        and enemy.y <= bullet.y <= enemy.y + enemy.image.get_height()
    )


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.icon = pygame.image.load("assets/images/ufo.png")
        pygame.display.set_icon(self.icon)
        self.background = pygame.image.load("assets/images/background.png")
        self.background = pygame.transform.scale(self.background, (800, 600))
        mixer.music.load("assets/audio/background.wav")
        mixer.music.play(-1)
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
        self.score = 0
        self.player = Player(self.screen)
        self.enemies = [Enemy(self.screen) for _ in range(60)]
        self.bullet = Bullet(self.screen, self.player)

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.direction = -1
                elif event.key == pygame.K_RIGHT:
                    self.player.direction = 1
                if event.key == pygame.K_SPACE:
                    if self.bullet.state == "ready":
                        self.bullet.state = "fire"
                        self.bullet.x = (
                            self.player.x
                            + self.player.image.get_width() // 2
                            - self.bullet.image.get_width() // 2
                        )
                        self.bullet.y = self.player.y - self.bullet.image.get_height()
                        bullet_sound = mixer.Sound("assets/audio/laser.wav")
                        bullet_sound.play()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player.direction = 0

    def update(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))

        self.player.update()
        self.player.draw()

        for enemy in self.enemies:
            enemy.update()
            enemy.draw()

        self.bullet.update()
        if self.bullet.state == "fire":
            self.bullet.draw()

        for enemy in self.enemies:
            if has_bullet_collided_with_enemy(self.bullet, enemy):
                explosion_sound = mixer.Sound("assets/audio/explosion.wav")
                explosion_sound.play()
                self.bullet.state = "ready"
                enemy.x = random.randint(
                    0, self.screen.get_width() - enemy.image.get_width()
                )
                enemy.y = random.randint(0, 100)
                self.score += 1

        self.draw_score()

        pygame.display.update()
        self.clock.tick(60)

    def run(self):
        while True:
            self.handle_events()
            self.update()


if __name__ == "__main__":
    game = Game()
    game.run()
