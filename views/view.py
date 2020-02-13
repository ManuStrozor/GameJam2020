import pygame

BLUE = (0, 136, 123)
HL_BLUE = (42, 255, 238)
WHITE = (255, 255, 255)
CLOUD = (180, 180, 180)
GREY = (80, 80, 80)
DARK = (21, 21, 21)
FULL_DARK = (16, 16, 16)


class View:

    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.state = 0
        self.title_font = pygame.font.Font("assets/font/spacebar.ttf", 40)
        self.normal_font = pygame.font.Font("assets/font/spacebar.ttf", 20)
        self.default_font = pygame.font.SysFont("ComicSans", 32)
        self.color = CLOUD
        self.background = None
        self.title = None
        self.title_offset_x = 0
        self.curr_btn = None
        self.curr_btn_index = -1
        self.buttons = []
        self.cursor = 0

    def loop(self):
        while self.state:
            self.update()
            self.draw()
            pygame.display.flip()

    def update(self):
        self.update_focus()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1\
                    and self.curr_btn is not None and self.curr_btn.rect.collidepoint(pygame.mouse.get_pos()):
                self.game.goto(self.curr_btn.target)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN or e.key == pygame.K_RIGHT or e.key == pygame.K_UP or e.key == pygame.K_LEFT:
                    self.keyboard_navigation(e.key)
                elif e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    if self.curr_btn is not None:
                        self.game.goto(self.curr_btn.target)
                elif e.key == pygame.K_ESCAPE:
                    self.game.goto(self.game.last_view)
            if e.type == pygame.QUIT:
                self.game.exit()

    def draw(self):
        if self.background is not None:
            self.game.window.blit(pygame.transform.scale(self.background,
                (self.game.window.get_width(), self.game.window.get_height())), (0, 0))
        else:
            self.game.window.fill(FULL_DARK)
            step = 40
            i = step/2
            while i < self.game.window.get_width():
                j = step/2
                while j < self.game.window.get_height():
                    pygame.draw.rect(self.game.window, GREY, (i, j, 1, 1), 0)
                    j += step
                i += step

        if self.title is not None:
            text_menu = self.title_font.render(self.title, 1, BLUE)
            self.game.window.blit(text_menu,
                (self.game.window.get_width()/2 - text_menu.get_rect().centerx, self.title_offset_x))

        for btn in self.buttons:
            btn.draw(self.game.window)

    def keyboard_navigation(self, key):
        if key == pygame.K_DOWN or key == pygame.K_RIGHT:
            if self.curr_btn_index + 1 == len(self.buttons):
                self.set_curr_btn(0)
            else:
                self.set_curr_btn(self.curr_btn_index + 1)
        else:
            if self.curr_btn_index <= 0:
                self.set_curr_btn(len(self.buttons) - 1)
            else:
                self.set_curr_btn(self.curr_btn_index - 1)

    def update_focus(self):
        i = 0
        for button in self.buttons:
            if pygame.mouse.get_focused()\
                    and button.rect.collidepoint(pygame.mouse.get_pos()):  # La souris survol un bouton
                self.set_curr_btn(i)
                if not button.hover_sounded:
                    self.game.get_audio("button_hover").play()
                    button.hover_sounded = True
            else:
                if self.curr_btn != button:
                    button.update_colors(BLUE)
                    button.hover_sounded = False
            i += 1

        # Si la souris ne survol aucun bouton, alors mettre à jour le cursor
        i = 0
        for b in self.buttons:
            if not b.rect.collidepoint(pygame.mouse.get_pos()):
                i += 1
        if i == len(self.buttons):
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            self.cursor = 0

    def set_curr_btn(self, index):
        if self.cursor == 0:
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
            self.cursor = 1
        self.curr_btn = self.buttons.__getitem__(index)
        self.curr_btn_index = index
        self.curr_btn.update_colors(HL_BLUE)

    def set_background(self, filename):
        self.background = pygame.image.load(filename)

    def set_title(self, title, offset=100):
        self.title = title
        self.title_offset_x = offset


class Button:

    hover_sounded = False

    def __init__(self, size, pos, text, target):
        self.font = pygame.font.Font("assets/font/spacebar.ttf", 20)

        self.init_surface(size, pos)

        self.color = BLUE
        self.background = DARK

        self.text = text
        self.content = self.font.render(self.text, 1, self.color)
        if self.content.get_rect().width > size[0]:
            self.init_surface((self.content.get_rect().width + 20, size[1]), pos)

        self.target = target

    def draw(self, window):
        # fond noir
        self.surface.fill(self.background)
        window.blit(self.surface, self.rect)

        # contour du bouton
        thickness = 3
        pygame.draw.rect(window, HL_BLUE, (self.rect.x - thickness, self.rect.y, thickness, self.rect.height), 0)  # left
        pygame.draw.rect(window, HL_BLUE, (self.rect.x + self.rect.width, self.rect.y, thickness, self.rect.height), 0)  # right
        pygame.draw.rect(window, HL_BLUE, (self.rect.x, self.rect.y - thickness, self.rect.width, thickness), 0)  # top
        pygame.draw.rect(window, HL_BLUE, (self.rect.x, self.rect.y + self.rect.height, self.rect.width, thickness), 0)  # bottom

        # contenu
        window.blit(self.content, (self.rect.x + self.rect.width / 2 - self.content.get_rect().centerx, self.rect.y + self.rect.height / 2 - self.content.get_rect().centery))

    def update_colors(self, color):
        self.color = color
        self.content = self.font.render(self.text, 1, self.color)

    def init_surface(self, size, pos):
        self.surface = pygame.Surface(size)
        self.surface.set_alpha(230)
        self.rect = self.surface.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
