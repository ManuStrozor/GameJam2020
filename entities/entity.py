import pygame


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
        self.rect.x += self.speed

    def move_left(self):
        self.direction = "left"
        self.rect.x -= self.speed

    def move_up(self):
        self.direction = "top"
        self.rect.y -= self.speed

    def move_down(self):
        self.direction = "bot"
        self.rect.y += self.speed

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
