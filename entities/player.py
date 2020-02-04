import pygame
from entities.entity import Entity


class Player(Entity):

    def __init__(self, game):
        super().__init__(game)

        self.image_name = "player"
        self.crouch_image = pygame.image.load('assets/player_crouch.png')

        # Spawn du joueur
        self.rect.x += game.window.get_width() / 2 - self.rect.width / 2
        self.rect.y += game.window.get_height() - 50 - self.rect.height

        self.crouchState = False
        self.jumping = False
        self.max_jumpDist = 10
        self.jumpDist = self.max_jumpDist

        self.set_max_health(100)
        self.set_max_speed(8)

    def update(self):
        super().update()

        # Déplacement (zqsd)
        alt = self.rect.y
        if self.game.keyPressed.get(pygame.K_LEFT) or self.game.keyPressed.get(pygame.K_a):
            if self.rect.x - self.speed > 0:
                self.move_left()
        if self.game.keyPressed.get(pygame.K_RIGHT) or self.game.keyPressed.get(pygame.K_d):
            if self.rect.x + self.rect.width + self.speed < self.game.window.get_width():
                self.move_right()
        if not self.jumping:
            if self.game.keyPressed.get(pygame.K_UP) or self.game.keyPressed.get(pygame.K_w):
                if self.rect.y > 0:
                    self.move_up()
            if self.game.keyPressed.get(pygame.K_DOWN) or self.game.keyPressed.get(pygame.K_s):
                if self.rect.y + self.rect.height + self.speed < self.game.window.get_height():
                    self.move_down()
            if self.game.keyPressed.get(pygame.K_SPACE):
                self.jumping = True
        # Jump
        elif self.jumpDist >= -self.max_jumpDist:
            neg = 1
            if self.jumpDist < 0:
                neg = -1
            dist = (self.jumpDist ** 2) * 0.3 * neg
            self.rect.y -= dist
            self.game.moveBGY(dist)
            self.jumpDist -= 1
        else:
            self.rect.y = alt
            if self.rect.y < 480:
                self.rect.y = 480
            self.jumping = False
            self.jumpDist = self.max_jumpDist

        # crouch
        if self.game.keyPressed.get(pygame.K_LCTRL) or self.game.keyPressed.get(pygame.K_RCTRL):
            self.crouch(True)
        else:
            self.crouch(False)

        self.set_image(pygame.image.load('assets/'+self.image_name+'_'+self.direction+'.png'))

    def crouch(self, state):
        self.crouchState = state
        self.speed = self.max_speed
        if state:
            self.speed /= 3
            self.image_name = "player_crouch"
        else:
            self.image_name = "player"


    def dead(self):
        self.game.gameover = True
