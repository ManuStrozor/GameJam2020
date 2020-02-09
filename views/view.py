import pygame


class View:

    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.state = 0
        self.title_font = pygame.font.SysFont('comicsans', 85, True)
        self.normal_font = pygame.font.SysFont('comicsans', 40, True)
        self.color = (255, 255, 255)
        self.background = None
        self.title = None
        self.curr_btn = None
        self.curr_btn_index = -1
        self.buttons = []

    def loop(self):
        while self.state:
            self.update()
            self.draw()
            pygame.display.flip()

    def update(self):
        self.update_focus()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1\
                    and self.curr_btn.rect.collidepoint(pygame.mouse.get_pos()):
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

        if self.title is not None:
            text_menu = self.title_font.render(self.title, 1, self.color)
            self.game.window.blit(text_menu, (self.game.window.get_width()/2 - text_menu.get_rect().centerx, 100))

        for button in self.buttons:
            button.surface.fill(button.background)
            self.game.window.blit(button.surface, button.rect)
            text = self.normal_font.render(button.text, 1, button.color)
            self.game.window.blit(text, (button.rect.x + button.surface.get_width()/2 - text.get_rect().centerx,
                                         button.rect.y + text.get_rect().centery + 15))

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
            else:
                if self.curr_btn != button:
                    button.color = (255, 255, 255)
                    button.background = (0, 0, 0)
            i += 1

    def set_curr_btn(self, index):
        self.curr_btn = self.buttons.__getitem__(index)
        self.curr_btn_index = index
        self.curr_btn.color = (0, 0, 0)
        self.curr_btn.background = (255, 255, 255)

    def set_background(self, filename):
        self.background = pygame.image.load(filename)

    def set_title(self, title):
        self.title = title


class Button:

    def __init__(self, size, pos, text, target):
        self.surface = pygame.Surface(size)
        self.surface.set_alpha(128)
        self.rect = self.surface.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.color = (255, 255, 255)
        self.background = (0, 0, 0)
        self.text = text
        self.target = target
