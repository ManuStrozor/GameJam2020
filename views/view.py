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
        self.buttons = []

    def loop(self):
        while self.state:
            self.update()
            self.draw()

    def action(self):
        print(self.name + " : action spéciale !")

    def update(self):
        if pygame.mouse.get_focused():
            self.curr_btn = None
            for button in self.buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):  # La souris survol un bouton
                    self.curr_btn = button
                    button.color = (0, 0, 0)
                    button.background = (255, 255, 255)
                else:
                    button.color = (255, 255, 255)
                    button.background = (0, 0, 0)

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.curr_btn.target is not None:
                    if self.curr_btn.target != "exit":
                        if self.curr_btn.target != "game":
                            self.game.goto(self.curr_btn.target)
                        else:
                            self.game.run(self.name)
                    else:
                        self.game.exit()
                else:
                    self.action()
            if e.type == pygame.QUIT:
                self.game.exit()

    def draw(self):
        if self.background is not None:
            self.game.window.blit(self.background, (0, 0))

        if self.title is not None:
            text_menu = self.title_font.render(self.title, 1, self.color)
            self.game.window.blit(text_menu, (self.game.window.get_width()/2 - text_menu.get_rect().centerx, 130))

        for button in self.buttons:
            button.surface.fill(button.background)
            self.game.window.blit(button.surface, button.rect)
            text = self.normal_font.render(button.text, 1, button.color)
            self.game.window.blit(text, (button.rect.x + button.surface.get_width()/2 - text.get_rect().centerx,
                                         button.rect.y + text.get_rect().centery + 15))

        pygame.display.flip()

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
