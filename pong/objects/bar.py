import pygame


class Bar(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, ball=None, score_pos=(0, 0), score=0):
        super().__init__()
        self.score_pos = score_pos
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 10
        self.ball = ball
        self.font = pygame.font.Font(None, 36)
        self.score = score

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, self.color, self.rect, 2)
        self.draw_score(surface)

    def update(self):
        if self.ball:
            self.follow_ball()

    def set_color(self, color):
        self.color = color

    def move(self, dx, dy):
        """Move the bar by (dx, dy) at a speed of speed."""
        vel_x = dx * self.speed
        vel_y = dy * self.speed
        self.hold_in_bounds(vel_x, vel_y)
        self.rect.x += vel_x
        self.rect.y += vel_y

    def follow_ball(self):
        self.rect.y = self.ball.rect.y - self.height // 2

    def hold_in_bounds(self, vel_x, vel_y):
        if self.rect.x + vel_x < 0:
            self.rect.x = 0
        elif self.rect.x + vel_x > 800 - self.width:
            self.rect.x = 800 - self.width

        if self.rect.y + vel_y < 0:
            self.rect.y = 0
        elif self.rect.y + vel_y > 600 - self.height:
            self.rect.y = 600 - self.height

    def draw_score(self, surface):
        text = self.font.render(str(self.score), True, (0,255,0))
        surface.blit(text, self.score_pos)
