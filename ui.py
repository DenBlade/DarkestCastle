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
