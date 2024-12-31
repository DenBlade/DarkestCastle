import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, image, groups):
        super().__init__(groups)
        self.image = image
        self.position = position
class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups):
        super().__init__(groups)
        self.rect = surface.get_rect(topleft=position)

