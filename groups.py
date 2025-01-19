import pygame

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
    def draw(self):
        for sprite in self:
            self.display.blit(sprite.image, sprite.rect.topleft)

    def offset(self, offset):
        offset_vec = pygame.Vector2(offset)
        for sprite in self:
            sprite.rect.topright += offset_vec


class CollisionSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def offset(self, offset):
        offset_vec = pygame.Vector2(offset)
        for sprite in self:
            sprite.rect.topright += offset_vec

