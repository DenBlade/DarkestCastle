import pygame

class Progress_Bar:
    def __init__(self, x, y, max_progress):
        self.display = pygame.display.get_surface()
        self.progress_bg = pygame.image.load('assets/progress_bar.png')
        self.max_progress = max_progress
        self.x = x
        self.y = y
        self.max_width = self.progress_bg.get_width()-4
        self.height = self.progress_bg.get_height()-6

    def draw(self, progress):
        pygame.draw.rect(self.display, (255, 255, 255), (self.x+2, self.y+3, progress/self.max_progress*self.max_width, self.height))
        self.display.blit(self.progress_bg, (self.x, self.y))

class Button:
    def __init__(self, text, pos, size):
        self.display = pygame.display.get_surface()
        self.pos = pos
        self.font = pygame.font.SysFont('comicsans', size)
        self.text = text
        self.text_render = self.font.render(text, True, (255, 255, 255))
        self.rect = self.text_render.get_rect()
        self.rect.topleft = pos
        self.is_pressed = False
        self.is_hovered = False

    def on_hover(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        self.text_render = pygame.transform.smoothscale(self.text_render, (self.rect.width, self.rect.height+5))
        self.is_hovered = True
    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        self.display.blit(self.text_render, self.pos)
        if(self.rect.collidepoint(mouse_pos)):
            self.on_hover()
            if(pygame.mouse.get_pressed()[0]):
                if(not self.is_pressed):
                    self.is_pressed = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return True
            if(pygame.mouse.get_pressed()[0] == 0):
                self.is_pressed = False
        else:
            if(self.is_hovered):
                self.is_hovered = False
                self.text_render = self.font.render(self.text, True, (255, 255, 255))
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
