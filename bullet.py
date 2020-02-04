import pygame
from math import sqrt


class Bullet(pygame.sprite.Sprite):

    def __init__(self, weapon):
        super().__init__()
        self.weapon = weapon

        # Chargement de l'image
        self.bullet = pygame.image.load('assets/bullet.png')
        if self.weapon.player.direction == 1:
            self.image = self.bullet
        else:
            self.image = pygame.transform.flip(self.bullet, True, False)

        self.rect = self.image.get_rect()

        if weapon.player.direction == 1:
            self.rect.x = weapon.rect.x + 25
        else:
            self.rect.x = weapon.rect.x - 15
        self.rect.y = weapon.rect.y + 35

        self.direction = weapon.player.direction
        self.speed = 20

    def remove(self):
        self.weapon.all_bullets.remove(self)

    def move(self):
        if self.direction == 1:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        # Verification des collisions avec les aliens
        for alien in self.weapon.player.game.all_aliens:
            if self.collision(alien):
                self.remove()
                if alien.health <= self.weapon.atk:
                    self.weapon.player.game.score += 10
                alien.health_tmp = alien.health
                alien.attacker = self.weapon.player
                alien.health -= self.weapon.atk

        if self.rect.x > self.weapon.player.game.window.get_width() or self.rect.x < 0:
            self.remove()

    def collision(self, target):
        # calcul du point d'impact de la bullet
        if self.direction == 1:
            bulletX = self.rect.x + self.rect.width
        else:
            bulletX = self.rect.x
        bulletY = self.rect.y + self.rect.height/2

        # calcul du centre de la zone d'impact de la target
        targetX = target.rect.x + target.rect.width / 2
        targetY = target.rect.y + target.rect.height / 2

        return sqrt((targetX - bulletX)**2 + (targetY - bulletY)**2) < target.rect.width/2
