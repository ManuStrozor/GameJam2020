import pygame


class Player:

    grid_x = None
    grid_y = None
    speed = 2
    coins = 0
    oxygen_bottle = 0
    chaussure = False

    def __init__(self, game, pos):
        self.game = game
        self.grid_x = int(pos[0]/self.game.niveau.size_x)
        self.grid_y = int(pos[1]/self.game.niveau.size_y)
        self.rect = pygame.Rect(pos[0], pos[1], self.game.niveau.size_x, self.game.niveau.size_y)

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.move(-self.speed, 0)
        if key[pygame.K_RIGHT]:
            self.move(self.speed, 0)
        if key[pygame.K_UP]:
            self.move(0, -self.speed)
        if key[pygame.K_DOWN]:
            self.move(0, self.speed)

    def move(self, dx, dy):
        self.game.audio_walk.set_volume(0.05)
        self.game.audio_walk.play()
        self.rect.x += dx
        self.rect.y += dy

        bloks = self.game.walls + self.game.caisses + self.game.souffleurs + self.game.pieces + self.game.portes_lock + self.game.portes_unlock

        # Collision mur (petit bug d'1 pixel)
        for wall in self.game.walls:
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
        for saas in self.game.all_saas:
            if saas.cardinal == "North"\
                    and saas.rect.collidepoint(self.rect.x + self.rect.width/2, self.rect.y - 1)\
                    or saas.cardinal == "East"\
                    and saas.rect.collidepoint(self.rect.x + self.rect.width + 1, self.rect.y + self.rect.height/2)\
                    or saas.cardinal == "West"\
                    and saas.rect.collidepoint(self.rect.x - 1, self.rect.y + self.rect.height/2)\
                    or saas.cardinal == "South"\
                    and saas.rect.collidepoint(self.rect.x + self.rect.width/2, self.rect.y + self.rect.height + 1):

                if saas.cardinal == "East":
                    a = self.game.niveau.sortieE
                elif saas.cardinal == "South":
                    a = self.game.niveau.sortieS
                elif saas.cardinal == "North":
                    a = self.game.niveau.sortieN
                elif saas.cardinal == "West":
                    a = self.game.niveau.sortieW

                self.game.niveau.generer(a)

                self.game.clear_bloks()

                self.game.niveau.afficher()

                if saas.cardinal == "East":
                    self.rect.x = self.game.get_saas("West").rect.x + self.game.niveau.size_x + 2
                    self.rect.y = self.game.get_saas("West").rect.y
                elif saas.cardinal == "South":
                    self.rect.x = self.game.get_saas("North").rect.x
                    self.rect.y = self.game.get_saas("North").rect.y + self.game.niveau.size_y + 2
                elif saas.cardinal == "North":
                    self.rect.x = self.game.get_saas("South").rect.x
                    self.rect.y = self.game.get_saas("South").rect.y - self.game.niveau.size_y - 2
                elif saas.cardinal == "West":
                    self.rect.x = self.game.get_saas("East").rect.x - self.game.niveau.size_x - 2
                    self.rect.y = self.game.get_saas("East").rect.y

        # Collision porte verrouillée
        for porte_lock in self.game.portes_lock:
            if self.rect.colliderect(porte_lock.rect):
                if dx > 0:  # deplacement right
                    self.rect.right = porte_lock.rect.left
                if dx < 0:  # deplacement left
                    self.rect.left = porte_lock.rect.right
                if dy > 0:  # deplacement bottom
                    self.rect.bottom = porte_lock.rect.top
                if dy < 0:  # deplacement top
                    self.rect.top = porte_lock.rect.bottom

        # Collision dalle electrique SANS chaussures à propulsion
        for dalle_electrique in self.game.dalles_electriques:
            if self.rect.colliderect(dalle_electrique.rect) and self.chaussure is not True:
                pygame.mixer.stop()
                self.game.audio_electric.set_volume(1)
                self.game.audio_electric.play()
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
                pygame.mixer.stop()
                self.game.audio_chaussure_propulsion.set_volume(1)
                self.game.audio_chaussure_propulsion.play()

        # Collision dalle innonde SANS oxygene
        for dalle_innonde in self.game.dalles_innondes:
            if self.rect.colliderect(dalle_innonde.rect) and self.oxygen_bottle <= 0:
                pygame.mixer.stop()
                self.game.audio_electric.set_volume(1)  # a changer
                self.game.audio_electric.play()  # a changer
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
                    self.game.game_lost = True
                pygame.mixer.stop()
                self.game.audio_chaussure_propulsion.set_volume(1)
                self.game.audio_chaussure_propulsion.play()

        # Collision porte déverrouillée
        for porte_unlock in self.game.portes_unlock:
            if self.rect.colliderect(porte_unlock.rect):
                pygame.mixer.stop()
                self.game.audio_door.set_volume(3)
                self.game.audio_door.play()

        # Collision caisse (Pousser et Tirer)
        for caisse in self.game.caisses:
            if self.rect.colliderect(caisse.rect):  # Pousser la caisse quand on se dirige vers elle
                if dx > 0:  # deplacement right
                    if caisse.way_right(bloks):
                        caisse.rect.right += dx
                        pygame.mixer.stop()
                        self.game.audio_moving_box.set_volume(3)
                        self.game.audio_moving_box.play()
                    else:
                        self.rect.x -= dx
                if dx < 0:  # deplacement left
                    if caisse.way_left(bloks):
                        caisse.rect.left += dx
                        pygame.mixer.stop()
                        self.game.audio_moving_box.set_volume(3)
                        self.game.audio_moving_box.play()
                    else:
                        self.rect.x -= dx
                if dy > 0:  # deplacement bottom
                    if caisse.way_bottom(bloks):
                        caisse.rect.bottom += dy
                        pygame.mixer.stop()
                        self.game.audio_moving_box.set_volume(3)
                        self.game.audio_moving_box.play()
                    else:
                        self.rect.y -= dy
                if dy < 0:  # deplacement top
                    if caisse.way_top(bloks):
                        caisse.rect.top += dy
                        pygame.mixer.stop()
                        self.game.audio_moving_box.set_volume(3)
                        self.game.audio_moving_box.play()
                    else:
                        self.rect.y -= dy
            if pygame.key.get_pressed()[pygame.K_LCTRL]:  # Tirer la caisse quand la touche (Ctrl gauche) est appuyé
                tmp = caisse.rect
                if dx > 0:  # deplacement right
                    if caisse.way_right(bloks) and self.rect.collidepoint(tmp.x + dx + self.rect.width + self.speed, tmp.y + int(tmp.height/2))\
                            or self.rect.collidepoint(tmp.x + dx + self.speed - 1, tmp.y + int(tmp.height/2)):
                        caisse.rect.right = self.rect.left
                        pygame.mixer.stop()
                        self.game.audio_moving_box.set_volume(3)
                        self.game.audio_moving_box.play()
                if dx < 0:  # deplacement left
                    if caisse.way_left(bloks) and self.rect.collidepoint(tmp.x + dx - self.speed, tmp.y + int(tmp.height/2))\
                            or self.rect.collidepoint(tmp.x + dx + self.rect.width + self.speed - 1, tmp.y + int(tmp.height/2)):
                        caisse.rect.left = self.rect.right
                        pygame.mixer.stop()
                        self.game.audio_moving_box.set_volume(3)
                        self.game.audio_moving_box.play()
                if dy > 0:  # deplacement bottom
                    if caisse.way_bottom(bloks) and self.rect.collidepoint(tmp.x + int(tmp.width / 2), tmp.y + dy + self.rect.height + self.speed)\
                            or self.rect.collidepoint(tmp.x + int(tmp.width / 2), tmp.y + dy + self.speed - 1):
                        caisse.rect.bottom = self.rect.top
                        pygame.mixer.stop()
                        self.game.audio_moving_box.set_volume(3)
                        self.game.audio_moving_box.play()
                if dy < 0:  # deplacement top
                    if caisse.way_top(bloks) and self.rect.collidepoint(tmp.x + int(tmp.width / 2), tmp.y + dy - self.speed)\
                            or self.rect.collidepoint(tmp.x + int(tmp.width / 2), tmp.y + dy + self.rect.height + self.speed - 1):
                        caisse.rect.top = self.rect.bottom
                        pygame.mixer.stop()
                        self.game.audio_moving_box.set_volume(3)
                        self.game.audio_moving_box.play()

        # Interaction souffleur
        for souffleur in self.game.souffleurs:
            for caisse in self.game.caisses:
                tmp = souffleur.rect

                souf_right = pygame.Rect(tmp.x + tmp.width, tmp.y, tmp.width, tmp.height)
                if souf_right.colliderect(caisse.rect):
                    caisse.move(self.speed, 0)
                if souf_right.colliderect(self.rect):
                    self.rect.x += self.speed

                souf_left = pygame.Rect(tmp.x - tmp.width, tmp.y, tmp.width, tmp.height)
                if souf_left.colliderect(caisse.rect):
                    caisse.move(-self.speed, 0)
                if souf_left.colliderect(self.rect):
                    self.rect.x -= self.speed

                souf_bottom = pygame.Rect(tmp.x, tmp.y + tmp.height, tmp.width, tmp.height)
                if souf_bottom.colliderect(caisse.rect):
                    caisse.move(0, self.speed)
                if souf_bottom.colliderect(self.rect):
                    self.rect.y += self.speed

                souf_top = pygame.Rect(tmp.x, tmp.y - tmp.height, tmp.width, tmp.height)
                if souf_top.colliderect(caisse.rect):
                    caisse.move(0, -self.speed)
                if souf_top.colliderect(self.rect):
                    self.rect.y -= self.speed

        # Collision piece (coins)
        for piece in self.game.pieces:
            if self.rect.colliderect(piece.rect):
                self.coins += 1
                self.game.pieces.remove(piece)
                self.game.get_obj(piece.grid[0], piece.grid[1]).type = None
                pygame.mixer.stop()
                self.game.audio_coins.set_volume(3)
                self.game.audio_coins.play()

        # Collision oxygen_bottle
        for oxygen_bottle in self.game.oxygen_bottles:
            if self.rect.colliderect(oxygen_bottle.rect):
                self.oxygen_bottle += 100
                self.game.oxygen_bottles.remove(oxygen_bottle)
                self.game.get_obj(oxygen_bottle.grid[0], oxygen_bottle.grid[1]).type = None
                print("bouteille oxygene récup")
                pygame.mixer.stop()
                self.game.audio_oxygen_bottle.set_volume(3)
                self.game.audio_oxygen_bottle.play()

        # Collision chaussure
        for chaussure in self.game.chaussures:
            if self.rect.colliderect(chaussure.rect):
                self.chaussure = True
                self.game.chaussures.remove(chaussure)
                self.game.get_obj(chaussure.grid[0], chaussure.grid[1]).type = None
                print("chaussure récup")
                pygame.mixer.stop()
                self.game.audio_chaussure_recup.set_volume(1)
                self.game.audio_chaussure_recup.play()

        # Collision button
        for button in self.game.buttons:
            if self.rect.colliderect(button.rect):
                self.game.buttons.remove(button)
                self.game.get_obj(button.grid[0], button.grid[1]).type = "button_pressed"
                pygame.mixer.stop()
                self.game.audio_button.set_volume(3)
                self.game.audio_button.play()
                print("appui boutton")

                # changer l'etat de la porte verouillé en deverouillé
                for porte_lock in self.game.portes_lock:
                    self.game.portes_lock.remove(porte_lock)
                    self.game.get_obj(porte_lock.grid[0], porte_lock.grid[1]).type = "porte_unlock"


    def way_right(self, list_of_items):
        for item in list_of_items:
            if self.rect.collidepoint(item.rect.midleft[0]-1, item.rect.midleft[1]):
                self.rect.right = item.rect.left
                return False
            if self.rect.collidepoint(item.rect.topleft[0]-1, item.rect.topleft[1]):
                return False
            if self.rect.collidepoint(item.rect.bottomleft[0]-1, item.rect.bottomleft[1]-1):
                return False
        return True

    def way_left(self, list_of_items):
        for item in list_of_items:
            if self.rect.collidepoint(item.rect.midright[0]+1, item.rect.midright[1]):
                self.rect.left = item.rect.right
                return False
            if self.rect.collidepoint(item.rect.topright[0]+1, item.rect.topright[1]):
                return False
            if self.rect.collidepoint(item.rect.bottomright[0]+1, item.rect.bottomright[1]-1):
                return False
        return True

    def way_top(self, list_of_items):
        for item in list_of_items:
            if self.rect.collidepoint(item.rect.midbottom[0], item.rect.midbottom[1]+1):
                self.rect.top = item.rect.bottom
                return False
            if self.rect.collidepoint(item.rect.bottomleft[0], item.rect.bottomleft[1]+1):
                return False
            if self.rect.collidepoint(item.rect.bottomright[0]-1, item.rect.bottomright[1]):
                return False
        return True

    def way_bottom(self, list_of_items):
        for item in list_of_items:
            if self.rect.collidepoint(item.rect.midtop[0], item.rect.midtop[1]-1):
                self.rect.bottom = item.rect.top
                return False
            if self.rect.collidepoint(item.rect.topleft[0], item.rect.topleft[1]-1):
                return False
            if self.rect.collidepoint(item.rect.topright[0]-1, item.rect.topright[1]-1):
                return False
        return True
