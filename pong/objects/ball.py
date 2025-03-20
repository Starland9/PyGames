import random

import pygame

from objects.bar import Bar


class Ball(pygame.sprite.Sprite):
    def __init__(self, color=(255, 0,0), bars: [Bar]=None):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 300
        self.speed = 5
        self.dir_x = 1
        self.dir_y = 1
        self.bars = bars
        self.beep = pygame.mixer.Sound("assets/audio/ping_pong_8bit_beeep.ogg")
        self.long_beep = pygame.mixer.Sound("assets/audio/ping_pong_8bit_peeeeeep.ogg")

    def update(self, *args, **kwargs):
        self.move()
        self.bounce_on_screen()
        self.bounce_on_bar()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed


    def bounce_on_screen(self):
        if self.rect.x < 0:
            self.long_beep.play()
            self.reset()
            self.bars[1].score += 1

        if self.rect.x > 800:
            self.long_beep.play()
            self.reset()
            self.bars[0].score += 1

        if self.rect.y < 0:
            self.dir_y *= -1

        if self.rect.y > 600:
            self.dir_y *= -1

    def bounce_on_bar(self):
        if self.bars:
            for bar in self.bars:
                if self.rect.colliderect(bar.rect):
                    self.beep.play()
                    self.speed += 1

                    if self.rect.x < bar.rect.x:
                        self.dir_x *= -1
                    elif self.rect.x > bar.rect.x:
                        self.dir_x *= -1



    def reset(self):
        self.rect.x = 400
        self.rect.y = 300
        self.dir_x = random.choice([-1, 1])
        self.dir_y = random.choice([-1, 1])
        self.speed = 5
