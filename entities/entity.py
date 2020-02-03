import pygame


class Entity(pygame.sprite.Sprite):

    original_image = None
    image = None
    rect = None

    max_health = None
    max_speed = None
    direction = None
    health = None
    speed = None
    atk = None

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.set_original_image('assets/entity.png')

    def update(self):

        if self.health <= 0:
            self.dead()

        if self.direction == 1:
            self.game.setImage(self, self.original_image)
        else:
            self.game.setImage(self, pygame.transform.flip(self.original_image, True, False))

    def draw(self):
        self.game.window.blit(self.image, self.rect)
        self.game.draw_lifebar(self)

    def move_right(self):
        self.direction = 1
        self.rect.x += self.speed

    def move_left(self):
        self.direction = -1
        self.rect.x -= self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def attack(self, entity):
        entity.health -= self.atk

    def dead(self):
        pass

    def set_original_image(self, path):
        self.original_image = pygame.image.load(path)
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def set_max_health(self, value):
        self.max_health = value
        self.health = value

    def set_max_speed(self, value):
        self.max_speed = value
        self.speed = value
