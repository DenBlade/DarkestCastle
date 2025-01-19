import sys

import pygame
import player
import sprites
import groups
from settings import *
from pytmx.util_pygame import load_pygame
from os.path import join as os_join
class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Darkest Castle")
        self.all_sprites = groups.AllSprites()
        self.clock = pygame.time.Clock()
        self.collision_sprites = groups.CollisionSprites()
        self.light_source = player.LightSource((600,200), 100, self.collision_sprites)
        self.is_dragging_light = False
        self.was_light_source_dragged = False
        self.screen_sliding_speed = (-0.1, 0)
        self.prepare_map()
    def prepare_map(self):
        pytmx_map = load_pygame(os_join("assets", "map", "MapTest3.tmx"))
        for x, y, tile in pytmx_map.get_layer_by_name("Background").tiles():
            sprites.Sprite((x*TILE_SIZE, y*TILE_SIZE), tile, self.all_sprites)
        for item in pytmx_map.get_layer_by_name("Collideable"):
            sprites.CollisionSprite((item.x, item.y), pygame.Surface((item.width, item.height)), self.collision_sprites)
    def screen_slide(self):
        self.collision_sprites.offset(self.screen_sliding_speed)
        self.all_sprites.offset(self.screen_sliding_speed)
        self.light_source.offset(self.screen_sliding_speed)
    def run(self):
        while True:
            delta_time = self.clock.tick()/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.light_source.hitbox_rect.collidepoint(pygame.mouse.get_pos()):
                            self.is_dragging_light = True
                            self.was_light_source_dragged = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.is_dragging_light = False
            if self.is_dragging_light:
                self.light_source.move_by_mouse(delta_time)
            else:
                if(abs(self.light_source.get_displacement()[0]) > APPROXIMATE_ZERO and abs(self.light_source.get_displacement()[1]) > APPROXIMATE_ZERO):
                    self.light_source.momentum(delta_time)
            self.all_sprites.draw()
            self.light_source.draw()
            if(self.was_light_source_dragged):
                self.screen_slide()
            pygame.display.update()

game = Game()
game.run()