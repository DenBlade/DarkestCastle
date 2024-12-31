import pygame

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
    def draw(self):
        for sprite in self:
            self.display.blit(sprite.image, sprite.position)


