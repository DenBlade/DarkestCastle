import pygame

from settings import *

class LightSource:
    def __init__(self, position, radius, collision_sprites, spike_colliders_sprites):
        self.collision_sprites = collision_sprites
        self.spike_colliders_sprites = spike_colliders_sprites
        self.display = pygame.display.get_surface()
        self.radius = radius
        self.hitbox_rect = pygame.FRect(position, (radius/5*2, radius/5*2))
        self.hitbox_rect.center = position
        self.dark_mask = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.dark_mask_circle = pygame.Surface((self.radius*2, self.radius*2))
        self.light_mask = pygame.Surface((self.radius*2, self.radius*2))
        self.last_pos = pygame.Vector2(self.hitbox_rect.center)
        self.last_mouse_pos = pygame.Vector2(self.hitbox_rect.center)
        self.is_alive = True
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
        self.spikes_check("horizontal", displacement)
        self.collision("horizontal", displacement)

        self.hitbox_rect.y += speed.y
        self.spikes_check("vertical", displacement)
        self.collision("vertical", displacement)

        self.last_pos = pygame.Vector2(self.hitbox_rect.center)
        self.last_mouse_pos = mouse_pos

    def get_displacement(self):
        return self.last_mouse_pos - self.last_pos

    def momentum(self, delta_time):
        displacement = (self.last_mouse_pos - self.last_pos)
        self.hitbox_rect.x += displacement.x * delta_time
        self.spikes_check("horizontal", displacement)
        self.collision("horizontal", displacement)

        self.hitbox_rect.y += displacement.y * delta_time
        self.spikes_check("vertical", displacement)
        self.collision("vertical", displacement)
        self.last_pos = pygame.Vector2(self.hitbox_rect.center)

    def collision(self, direction, displacement):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if displacement.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    elif displacement.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                elif direction == 'vertical':
                    if displacement.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    elif displacement.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom

    def spikes_check(self, direction, displacement):
        for spike in self.spike_colliders_sprites:
            if spike.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if spike.direction == 'right':
                        if displacement.x < 0:
                            self.is_alive = False
                    elif spike.direction == 'left':
                        if displacement.x > 0:
                            self.is_alive = False
                elif direction == 'vertical':
                    if spike.direction == 'bottom':
                        if displacement.y < 0:
                            self.is_alive = False
                    elif spike.direction == 'top':
                        if displacement.y > 0:
                            self.is_alive = False


    def is_out_of_bounds(self):
        return self.hitbox_rect.right < 0

    def get_is_alive(self):
        return self.is_alive


