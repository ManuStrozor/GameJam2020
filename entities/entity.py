import pygame


class Entity(pygame.sprite.Sprite):

    original_image = None
    image = None
    rect = None

    max_health = None
    max_speed = None
    direction = None
    health = None
    attacker = None
    health_tmp = None
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
        entity.health_tmp = entity.health
        entity.attacker = self
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
