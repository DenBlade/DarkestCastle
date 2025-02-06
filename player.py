import pygame
import random

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
        self.light_sprites = []
        self.prepare_light_sprites(8)
        self.sprite_index = 0
        self.current_sprite = self.light_sprites[self.sprite_index]
        self.animation_speed = 16
        self.last_pos = pygame.Vector2(self.hitbox_rect.center)
        self.last_mouse_pos = pygame.Vector2(self.hitbox_rect.center)
        self.is_alive = True
        self.death_particles = []
        self.prepare_particles()
        self.prepare_light_mask()

    def prepare_light_sprites(self, sprites_number):
        for sprite_number in range(sprites_number):
            surface = pygame.Surface((self.radius*2, self.radius*2))
            for i in range(0, 255):
                brighter_rgb = min(255, i + 180 - sprite_number * 25)
                pygame.draw.circle(surface, (brighter_rgb, brighter_rgb, brighter_rgb/2), (self.radius,self.radius), self.radius/5 * ((256 - i) / 256))
            self.light_sprites.append(surface)

    def prepare_light_mask(self):
        for i in range(0, 255):
            pygame.draw.circle(self.dark_mask_circle, (i, i, i), (self.radius,self.radius), self.radius * ((256 - i) / 256))
            # brighter_rgb = min(255, i+180)
            # pygame.draw.circle(self.light_mask, (brighter_rgb, brighter_rgb, brighter_rgb/2), (self.radius,self.radius), self.radius/5 * ((256 - i) / 256))

    def prepare_particles(self):
        for i in range(0, 30):
            self.death_particles.append(Particle("square", (255, 255, 20), random.randint(30, 220), random.randint(2, 8), (random.uniform(-0.4, 0.4), random.uniform(-0.4, 0.4)), random.randint(20, 80)))

    def animate(self, delta_time):
        self.sprite_index += self.animation_speed * delta_time
        self.current_sprite = self.light_sprites[int(self.sprite_index)%len(self.light_sprites)]

    def draw(self, delta_time):
        self.dark_mask.fill((0,0,0))
        self.dark_mask.blit(self.dark_mask_circle, (self.hitbox_rect.center[0]-self.radius, self.hitbox_rect.center[1]-self.radius))
        self.display.blit(self.current_sprite, (self.hitbox_rect.center[0]-self.radius,self.hitbox_rect.center[1]-self.radius), special_flags=pygame.BLEND_ADD)
        self.display.blit(self.dark_mask, (0, 0), special_flags=pygame.BLEND_MULT)
        self.animate(delta_time)

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

    def defeat_animation(self):
        self.display.fill((0,0,0))
        for particle in self.death_particles:
            if not particle.draw(self.display,self.hitbox_rect.x+random.randint(-10, 10), self.hitbox_rect.y+random.randint(-10, 10)):
                self.death_particles.remove(particle)


    def is_out_of_bounds(self):
        return self.hitbox_rect.right < 0

    def get_is_alive(self):
        return self.is_alive

class Particle:
    def __init__(self, type, color, transparency, size, velocity, anim_time):
        self.type = type # circle/square
        self.size = size # serves as a radius for circle
        self.color = color
        self.transparency = transparency
        self.velocity = velocity
        self.x = 0
        self.y = 0
        self.anim_time = anim_time
        self.anim_timer = 0
        self.max_size = size*3
        self.surface_alpha = pygame.Surface((self.max_size*2, self.max_size*2), pygame.SRCALPHA)

    def draw(self, surface, x, y):
        if self.type == 'circle':
            if self.anim_timer<=self.anim_time:
                alpha = round(self.transparency * ((self.anim_time - self.anim_timer) / self.anim_time))
                pygame.draw.circle(self.surface_alpha, self.color + (alpha,), (self.max_size, self.max_size), self.size)
                surface.blit(self.surface_alpha, (x-self.max_size+self.x, y-self.max_size+self.y))
                self.x += self.velocity[0]
                self.y += self.velocity[1]
                if(self.size <= self.max_size):
                    self.size += 1
                self.anim_timer += 0.1
                return True
            return False
        elif self.type == 'square':
            if self.anim_timer<=self.anim_time:
                alpha = round(self.transparency * ((self.anim_time - self.anim_timer) / self.anim_time))
                rect = pygame.FRect(0, 0, self.size, self.size)
                rect.center = (self.max_size, self.max_size)
                pygame.draw.rect(self.surface_alpha, self.color + (alpha,), rect)
                surface.blit(self.surface_alpha, (x-self.max_size+self.x, y-self.max_size+self.y))
                self.x += self.velocity[0]
                self.y += self.velocity[1]
                if(self.size <= self.max_size):
                    self.size += 1
                self.anim_timer += 0.1
                return True
            return False


