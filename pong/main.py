import os
import pathlib

import pygame

from objects.ball import Ball
from objects.bar import Bar


def load_score():
    if not pathlib.Path("score.txt").exists():
        return 0, 0

    with open("score.txt", "r") as f:
        scores = f.read().split("\n")
        score_1 = int(scores[0])
        score_2 = int(scores[1])

    return score_1, score_2


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pong")
        pygame.key.set_repeat(10, 10)
        scores = load_score()

        self.bar_1 = Bar(0, 0, 30, 100, (0, 0, 0), score_pos=(10, 10), score=scores[0])
        self.bar_2 = Bar(770, 0, 30, 100, (0, 0, 0), score_pos=(780, 10), score=scores[1])

        self.ball = Ball((0, 0, 0), [self.bar_1, self.bar_2])

    def update(self):
        pygame.time.Clock().tick(60)
        pygame.display.update()
        self.bar_1.update()
        self.bar_2.update()
        self.ball.update()
        self.bar_2_follow_ball()
        self.ball_1_follow_ball()


    def draw(self):
        self.bar_1.draw(self.screen)
        self.bar_2.draw(self.screen)
        self.ball.draw(self.screen)

    def bar_2_follow_ball(self):
        self.bar_2.rect.y = self.ball.rect.y - self.bar_2.height // 2

    def ball_1_follow_ball(self):
        self.bar_1.rect.y = self.ball.rect.y - self.bar_1.height // 2

    def save_score(self):
        with open("score.txt", "w") as f:
            f.write(str(self.bar_1.score) + "\n" + str(self.bar_2.score))

    def run(self):

        while True:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.save_score()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.bar_1.move(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.bar_1.move(0, 1)
                    elif event.key == pygame.K_w:
                        self.bar_2.move(0, -1)
                    elif event.key == pygame.K_s:
                        self.bar_2.move(0, 1)

            self.draw()

            self.update()


if __name__ == "__main__":
    game = Game()
    game.run()
