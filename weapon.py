import pygame
from bullet import Bullet


class Weapon(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.player = player

        # Chargement de l'image
        self.original_image = pygame.image.load('assets/gun.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x += self.player.rect.x
        self.rect.y += self.player.rect.y

        self.atk = 35
        self.all_bullets = pygame.sprite.Group()

    def draw(self):
        self.rect.y = self.player.rect.y
        if self.player.crouchState:
            self.rect.y += 10

        if self.player.direction == 1:
            self.rect.x = self.player.rect.x
            self.player.game.window.blit(self.image, self.rect)
        else:
            self.rect.x = self.player.rect.x - 10
            self.player.game.window.blit(pygame.transform.flip(self.image, True, False), self.rect)

    def fire(self):
        self.all_bullets.add(Bullet(self))
