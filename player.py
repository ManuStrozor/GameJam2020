import pygame

from objects.object import Movable


class Player(Movable):

    coins = 0
    oxygen_bottle = 0

    max_speed = 3
    speed = max_speed
    step = 1
    chaussure = False
    direction = 0
    moving = False
    grab = False
    grabbing = False
    collide_saas = False
    num_sprite = 0

    def __init__(self, game, pos):
        super().__init__(game.niveau, pos)
        self.game = game
        self.type = "player"
        self.dest = self.rect

    def update(self):
        key = pygame.key.get_pressed()
        if (key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_UP] or key[pygame.K_DOWN]) and not self.moving:
            self.moving = True
            if key[pygame.K_LCTRL] or key[pygame.K_RCTRL]:
                self.grab = True
            if key[pygame.K_LEFT]:
                self.direction = 1
                self.dest = (self.rect.x - self.rect.width, self.rect.y)
            elif key[pygame.K_RIGHT]:
                self.direction = 2
                self.dest = (self.rect.x + self.rect.width, self.rect.y)
            elif key[pygame.K_UP]:
                self.direction = 3
                self.dest = (self.rect.x, self.rect.y - self.rect.height)
            else:
                self.direction = 0
                self.dest = (self.rect.x, self.rect.y + self.rect.height)

        if self.direction == 1:
            if self.rect.x <= self.dest[0]:
                self.moving = False
                self.grab = False
            else:
                if self.rect.x - self.speed >= self.dest[0]:
                    if not self.collide_saas:
                        self.move(-self.speed, 0)
                    self.step += 1
                    if self.step > self.rect.width / self.speed:
                        if self.rect.x - self.dest[0] > 0:
                            if self.rect.x - self.dest[0] < self.speed:
                                self.move(-(self.rect.x - self.dest[0]), 0)
                            self.moving = False
                            self.dest = self.rect
                        self.collide_saas = False
                        self.grab = False
                        self.step = 1

        elif self.direction == 2:
            if self.rect.x >= self.dest[0]:
                self.moving = False
                self.grab = False
            else:
                if self.rect.x + self.speed <= self.dest[0]:
                    if not self.collide_saas:
                        self.move(self.speed, 0)
                    self.step += 1
                    if self.step > self.rect.width / self.speed:
                        if self.dest[0] - self.rect.x > 0:
                            if self.dest[0] - self.rect.x < self.speed:
                                self.move(self.dest[0] - self.rect.x, 0)
                            self.moving = False
                            self.dest = self.rect
                        self.collide_saas = False
                        self.grab = False
                        self.step = 1

        elif self.direction == 3:
            if self.rect.y <= self.dest[1]:
                self.moving = False
                self.grab = False
            else:
                if self.rect.y - self.speed >= self.dest[1]:
                    if not self.collide_saas:
                        self.move(0, -self.speed)
                    self.step += 1
                    if self.step > self.rect.height / self.speed:
                        if self.rect.y - self.dest[1] > 0:
                            if self.rect.y - self.dest[1] < self.speed:
                                self.move(0, -(self.rect.y - self.dest[1]))
                            self.moving = False
                            self.dest = self.rect
                        self.collide_saas = False
                        self.grab = False
                        self.step = 1

        elif self.direction == 0:
            if self.rect.y >= self.dest[1]:
                self.moving = False
                self.grab = False
            else:
                if self.rect.y + self.speed <= self.dest[1]:
                    if not self.collide_saas:
                        self.move(0, self.speed)
                    self.step += 1
                    if self.step > self.rect.height / self.speed:
                        if self.dest[1] - self.rect.y > 0:
                            if self.dest[1] - self.rect.y < self.speed:
                                self.move(0, self.dest[1] - self.rect.y)
                            self.moving = False
                            self.dest = self.rect
                        self.collide_saas = False
                        self.grab = False
                        self.step = 1

    def move(self, dx, dy):
        super().move(dx, dy)

        # Calcul du numéro de sprite
        if dy == 0:  # deplacement right
            cap = self.rect.width / self.speed
        if dx == 0:  # deplacement bottom
            cap = self.rect.height / self.speed
        if self.step % cap-1 == 0:
            self.num_sprite += 1
        if self.num_sprite == 4:
            self.num_sprite = 0

        bloks = self.game.niveau.d_objs["wall"]\
                + self.game.niveau.d_objs["box"]\
                + self.game.niveau.d_objs["wind_jet"]\
                + self.game.niveau.d_objs["coin"]\
                + self.game.niveau.d_objs["porte"]\
                + self.game.niveau.d_objs["porte_lock"]\
                + self.game.niveau.d_objs["button"]

        # Collision mur
        for wall in self.game.niveau.d_objs["wall"]:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # deplacement right
                    self.rect.right = wall.rect.left
                if dx < 0:  # deplacement left
                    self.rect.left = wall.rect.right
                if dy > 0:  # deplacement bottom
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # deplacement top
                    self.rect.top = wall.rect.bottom

        # Collision Saas
        for saas in self.game.niveau.d_objs["saas"]:
            if saas.rect.colliderect(self.rect):
                self.collide_saas = True
                self.moving = False
                if saas.cardinal == "East":
                    self.game.set_lvl(self.game.niveau.sortieE)
                    self.rect.x = self.game.get_saas("West").rect.x + self.rect.width
                    self.rect.y = self.game.get_saas("West").rect.y
                elif saas.cardinal == "South":
                    self.game.set_lvl(self.game.niveau.sortieS)
                    self.rect.x = self.game.get_saas("North").rect.x
                    self.rect.y = self.game.get_saas("North").rect.y + self.rect.height
                elif saas.cardinal == "North":
                    self.game.set_lvl(self.game.niveau.sortieN)
                    self.rect.x = self.game.get_saas("South").rect.x
                    self.rect.y = self.game.get_saas("South").rect.y - self.rect.height
                else:
                    self.game.set_lvl(self.game.niveau.sortieW)
                    self.rect.x = self.game.get_saas("East").rect.x - self.rect.width
                    self.rect.y = self.game.get_saas("East").rect.y

        # Collision porte
        for porte in self.game.niveau.d_objs["porte"]:
            if self.rect.colliderect(porte.rect):
                self.game.get_audio("door").play()

        # Collision porte verrouillée
        for porte in self.game.niveau.d_objs["porte_lock"]:
            if self.rect.colliderect(porte.rect):
                if dx > 0:  # deplacement right
                    self.rect.right = porte.rect.left
                if dx < 0:  # deplacement left
                    self.rect.left = porte.rect.right
                if dy > 0:  # deplacement bottom
                    self.rect.bottom = porte.rect.top
                if dy < 0:  # deplacement top
                    self.rect.top = porte.rect.bottom

        # Collision dalle electrique SANS chaussures à propulsion
        for dalle_electrique in self.game.niveau.d_objs["dalle_electrique"]:
            if self.rect.colliderect(dalle_electrique.rect) and self.chaussure is not True:
                self.game.get_audio("electric").play()
                if dx > 0:  # deplacement right
                    self.rect.right = dalle_electrique.rect.left
                if dx < 0:  # deplacement left
                    self.rect.left = dalle_electrique.rect.right
                if dy > 0:  # deplacement bottom
                    self.rect.bottom = dalle_electrique.rect.top
                if dy < 0:  # deplacement top
                    self.rect.top = dalle_electrique.rect.bottom

            # Collision dalle electrique AVEC chaussures à propulsion
            if self.rect.colliderect(dalle_electrique.rect) and self.chaussure is True:
                self.game.get_audio("chaussure_propulsion").play()

        # Collision dalle innonde SANS oxygene
        for dalle_innonde in self.game.niveau.d_objs["dalle_innonde"]:
            if self.rect.colliderect(dalle_innonde.rect) and self.oxygen_bottle <= 0:
                if dx > 0:  # deplacement right
                    self.rect.right = dalle_innonde.rect.left
                if dx < 0:  # deplacement left
                    self.rect.left = dalle_innonde.rect.right
                if dy > 0:  # deplacement bottom
                    self.rect.bottom = dalle_innonde.rect.top
                if dy < 0:  # deplacement top
                    self.rect.top = dalle_innonde.rect.bottom

            # Collision dalle innonde AVEC oxygene
            if self.rect.colliderect(dalle_innonde.rect) and self.oxygen_bottle > 0:
                self.oxygen_bottle = self.oxygen_bottle - 0.1
                if self.oxygen_bottle <= 0.5:
                    self.game.state = 0
                    self.game.goto("gameover")
                self.game.get_audio("water").play()

        # Collision caisse (Pousser et Tirer)
        for caisse in self.game.niveau.d_objs["box"]:

            if self.rect.colliderect(caisse.rect):  # Pousser la caisse
                if dx > 0:  # deplacement right
                    if caisse.way_right(bloks):
                        caisse.rect.left = self.rect.right
                    else:
                        self.rect.right = caisse.rect.left
                if dx < 0:  # deplacement left
                    if caisse.way_left(bloks):
                        caisse.rect.right = self.rect.left
                    else:
                        self.rect.left = caisse.rect.right
                if dy > 0:  # deplacement bottom
                    if caisse.way_bottom(bloks):
                        caisse.rect.top = self.rect.bottom
                    else:
                        self.rect.bottom = caisse.rect.top
                if dy < 0:  # deplacement top
                    if caisse.way_top(bloks):
                        caisse.rect.bottom = self.rect.top
                    else:
                        self.rect.top = caisse.rect.bottom

            if self.grab:  # Tirer la caisse
                self.grabbing = True
                tmp = caisse.rect
                if dx > 0:  # deplacement right
                    if self.rect.collidepoint(tmp.midright[0] + dx + 1, tmp.midright[1]):
                        caisse.rect.right = self.rect.left
                if dx < 0:  # deplacement left
                    if self.rect.collidepoint(tmp.midleft[0] + dx - 1, tmp.midleft[1]):
                        caisse.rect.left = self.rect.right
                if dy > 0:  # deplacement bottom
                    if self.rect.collidepoint(tmp.midbottom[0], tmp.midbottom[1] + dy + 1):
                        caisse.rect.bottom = self.rect.top
                if dy < 0:  # deplacement top
                    if self.rect.collidepoint(tmp.midtop[0], tmp.midtop[1] + dy - 1):
                        caisse.rect.top = self.rect.bottom
            else:
                self.grabbing = False

        # Interaction souffleur
        for souffleur in self.game.niveau.d_objs["wind_jet"]:
            for caisse in self.game.niveau.d_objs["box"]:

                tmp = souffleur.rect
                souf_left = pygame.Rect(tmp.x - tmp.width, tmp.y, tmp.width, tmp.height)
                souf_right = pygame.Rect(tmp.x + tmp.width, tmp.y, tmp.width, tmp.height)
                souf_top = pygame.Rect(tmp.x, tmp.y - tmp.height, tmp.width, tmp.height)
                souf_bottom = pygame.Rect(tmp.x, tmp.y + tmp.height, tmp.width, tmp.height)

                if souf_left.colliderect(caisse.rect):
                    caisse.move(-self.speed, 0)
                if souf_left.colliderect(self.rect):
                    self.rect.x -= self.speed

                if souf_right.colliderect(caisse.rect):
                    caisse.move(self.speed, 0)
                if souf_right.colliderect(self.rect):
                    self.rect.x += self.speed

                if souf_top.colliderect(caisse.rect):
                    caisse.move(0, -self.speed)
                if souf_top.colliderect(self.rect):
                    self.rect.y -= self.speed

                if souf_bottom.colliderect(caisse.rect):
                    caisse.move(0, self.speed)
                if souf_bottom.colliderect(self.rect):
                    self.rect.y += self.speed

        # Collision piece (coins)
        for piece in self.game.niveau.d_objs["coin"]:
            if self.rect.colliderect(piece.rect):
                self.coins += 1
                self.game.niveau.remove(piece)
                self.game.get_audio("coins").play()

        # Collision oxygen_bottle
        for oxygen_bottle in self.game.niveau.d_objs["oxygen"]:
            if self.rect.colliderect(oxygen_bottle.rect):
                self.oxygen_bottle += 500
                self.game.niveau.remove(oxygen_bottle)
                self.game.get_audio("oxygen_bottle").play()

        # Collision chaussure
        for chaussure in self.game.niveau.d_objs["chaussure"]:
            if self.rect.colliderect(chaussure.rect):
                self.chaussure = True
                self.game.niveau.remove(chaussure)
                chaussure.type = None
                self.game.get_audio("chaussure").play()

        # Collision button
        for button in self.game.niveau.d_objs["button"]:
            if self.rect.colliderect(button.rect):
                button.press()
                self.game.get_audio("button").play()

                # changer l'etat de la porte verouillé en deverouillé
                for porte in self.game.niveau.d_objs["porte_lock"]:
                    porte.unlock()

        # Collision event_fin
        for fin in self.game.niveau.d_objs["event_fin"]:
            if self.rect.colliderect(fin.rect):
                self.game.state = 0
                self.game.goto("win")
