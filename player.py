import pygame

from settings import *

class LightSource:
    def __init__(self, position, radius, collision_sprites):
        self.collision_sprites = collision_sprites
        self.display = pygame.display.get_surface()
        self.radius = radius
        self.hitbox_rect = pygame.FRect(position, (radius/5+5, radius/5+5))
        self.hitbox_rect.center = position
        self.dark_mask = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.dark_mask_circle = pygame.Surface((self.radius*2, self.radius*2))
        self.light_mask = pygame.Surface((self.radius*2, self.radius*2))
        self.last_pos = pygame.Vector2(self.hitbox_rect.center)
        self.last_mouse_pos = pygame.Vector2(self.hitbox_rect.center)
        self.prepare_light_mask()

    def prepare_light_mask(self):
        for i in range(0, 255):
            pygame.draw.circle(self.dark_mask_circle, (i, i, i), (self.radius,self.radius), self.radius * ((256 - i) / 256))
            brighter_rgb = min(255, i+180)
            pygame.draw.circle(self.light_mask, (brighter_rgb, brighter_rgb, brighter_rgb/2), (self.radius,self.radius), self.radius/5 * ((256 - i) / 256))

    def draw(self):
        self.dark_mask.fill((0,0,0))
        self.dark_mask.blit(self.dark_mask_circle, (self.hitbox_rect.center[0]-self.radius, self.hitbox_rect.center[1]-self.radius))
        self.display.blit(self.light_mask, (self.hitbox_rect.center[0]-self.radius,self.hitbox_rect.center[1]-self.radius), special_flags=pygame.BLEND_ADD)
        self.display.blit(self.dark_mask, (0, 0), special_flags=pygame.BLEND_MULT)

    def offset(self, offset):
        offset_vec = pygame.Vector2(offset)
        self.hitbox_rect.center += offset_vec
    def move_by_mouse(self, delta_time):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        displacement = (mouse_pos - self.last_pos)
        speed = displacement * delta_time
        self.hitbox_rect.x += speed.x
        self.collision("horizontal", displacement)
        self.hitbox_rect.y += speed.y
        self.collision("vertical", displacement)
        self.last_pos = pygame.Vector2(self.hitbox_rect.center)
        self.last_mouse_pos = mouse_pos
    def get_displacement(self):
        return self.last_mouse_pos - self.last_pos
    def momentum(self, delta_time):
        displacement = (self.last_mouse_pos - self.last_pos)
        self.hitbox_rect.x += displacement.x * delta_time
        self.collision("horizontal", displacement)
        self.hitbox_rect.y += displacement.y * delta_time
        self.collision("vertical", displacement)
        self.last_pos = pygame.Vector2(self.hitbox_rect.center)

    def collision(self, direction, displacement):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if displacement.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if displacement.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if displacement.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    if displacement.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom

