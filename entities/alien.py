import math
import random
from entities.entity import Entity


class Alien(Entity):

    def __init__(self, game):
        super().__init__(game)
        self.player = self.game.player

        # Spawn aléatoire
        if random.randint(0, 2) - 1:
            self.rect.x = game.window.get_width()
            self.direction = "left"
        else:
            self.rect.x = -self.rect.width
            self.direction = "right"
        self.rect.y = game.window.get_height() - 50 - self.rect.height

        self.max_atk_delay = 60
        self.atk_delay = self.max_atk_delay / 2

        self.set_max_health(150)
        self.set_max_speed(2)

    def update(self):
        super().update()

        dist = math.sqrt((self.rect.x - self.game.player.rect.x)**2 + (self.rect.y - self.player.rect.y)**2)
        if dist > self.player.rect.width:
            if self.rect.x < self.game.player.rect.x:
                self.direction = 1
                self.rect.x += self.speed
            else:
                self.direction = -1
                self.rect.x -= self.speed
            if abs(self.rect.y - self.player.rect.y) > 1:
                if self.rect.y > self.player.rect.y:
                    self.rect.y -= self.speed
                else:
                    self.rect.y += self.speed

    def dead(self):
        self.game.all_aliens.remove(self)
