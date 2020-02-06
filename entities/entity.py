import pygame

import game

class Entity(pygame.sprite.Sprite):

    image_name = None
    image = None
    rect = None

    max_health = None
    max_speed = None
    direction = "bot"
    health = None
    attacker = None
    health_tmp = None
    speed = None
    atk = None

    def __init__(self, game):
        super().__init__()
        self.game = game

        self.image = pygame.image.load('assets/player_bot.png')
        self.rect = self.image.get_rect()

    def update(self):

        if self.health <= 0:
            self.dead()

        self.set_image(pygame.image.load('assets/' + self.image_name + '_' + self.direction + '.png'))

    def draw(self):
        self.game.window.blit(self.image, self.rect)
        self.draw_lifebar()
        if self.health != self.health_tmp and self.health_tmp is not None:
            self.game.draw_text('-' + str(self.attacker.atk), (self.rect.x, self.rect.y - 45), (255, 0, 0))
            self.attacker = None
            self.health_tmp = self.health

    def draw_lifebar(self):
        pygame.draw.rect(self.game.window, (0, 0, 0), (self.rect.x, self.rect.y - 20, 50, 5))
        if self.health > 0:
            pygame.draw.rect(self.game.window, (255, 0, 0),
                             (self.rect.x, self.rect.y - 20, (self.health / self.max_health) * 50, 5))

    def move_right(self):
        self.direction = "right"
        for wall in game.walls:
            if self.rect.colliderect(wall.rect):
                if self.rect.x > 0:  # deplacement droit, si coté gauche du mur touché
                    self.rect.right = wall.rect.left
                if self.rect.x < 0:  # deplacement gauche, si coté droit du mur touché
                    self.rect.left = wall.rect.right
        self.rect.x += self.speed
        print("move right")

    def move_left(self):
        self.direction = "left"
        for wall in game.walls:
            if self.rect.colliderect(wall.rect):
                if self.rect.x > 0:  # deplacement droit, si coté gauche du mur touché
                    self.rect.right = wall.rect.left
                if self.rect.x < 0:  # deplacement gauche, si coté droit du mur touché
                    self.rect.left = wall.rect.right
        self.rect.x -= self.speed
        print("move left")

    def move_up(self):
        self.direction = "top"
        for wall in game.walls:
            if self.rect.colliderect(wall.rect):
                if self.rect.y > 0:  # deplacement bas, si coté haut du mur touché
                    self.rect.bottom = wall.rect.top
                if self.rect.y < 0:  # deplacement haut, si coté bas du mur touché
                    self.rect.top = wall.rect.bottom
        self.rect.y -= self.speed
        print("move up")

    def move_down(self):
        self.direction = "bot"
        for wall in game.walls:
            if self.rect.colliderect(wall.rect):
                if self.rect.y > 0:  # deplacement bas, si coté haut du mur touché
                    self.rect.bottom = wall.rect.top
                if self.rect.y < 0:  # deplacement haut, si coté bas du mur touché
                    self.rect.top = wall.rect.bottom
        self.rect.y += self.speed
        print("move down")

    def dead(self):
        pass

    def set_image(self, newImage):
        if self.image != newImage:
            self.image = newImage

    def set_max_health(self, value):
        self.max_health = value
        self.health = value

    def set_max_speed(self, value):
        self.max_speed = value
        self.speed = value