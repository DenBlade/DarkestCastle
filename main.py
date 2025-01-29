import sys

import pygame
import random

import player
import sprites
import groups
import ui
from settings import *
from pytmx.util_pygame import load_pygame
from os.path import join as os_join
class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Darkest Castle")
        self.all_sprites = groups.AllSprites()
        self.visible_sprites = groups.VisibleSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.spike_colliders_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.light_source = player.LightSource((200,200), 100, self.collision_sprites, self.spike_colliders_sprites)
        self.is_dragging_light = False
        self.was_light_source_dragged = False
        self.screen_sliding_speed = (-0.3, 0)
        self.x = 0
        self.distance = 0
        self.running = True
        self.prepare_map()
        self.progress_bar = ui.Progress_Bar(80,610, LEVEL_WIDTH*(LEVELS))
        self.font = pygame.font.Font('freesansbold.ttf', 128)

        self.music = pygame.mixer.Sound(os_join('assets', 'audio', 'Electricity.wav'))
        self.music.set_volume(0.5)
        self.music.play(loops=-1)
        self.defeat_sound = pygame.mixer.Sound(os_join('assets', 'audio', 'soundeffects', 'game-die.mp3'))
        self.defeat_sound.set_volume(0.5)

    def prepare_map(self):
        for i in range(0, LEVELS):
            file_name = "Level" + str(i) + ".tmx"
            pytmx_map = load_pygame(os_join("assets", "map", file_name))
            for x, y, tile in pytmx_map.get_layer_by_name("Background").tiles():
                sprites.Sprite((x*TILE_SIZE+LEVEL_WIDTH*i, y*TILE_SIZE-TILE_SIZE), tile, (self.all_sprites, self.visible_sprites))
            for x, y, tile in pytmx_map.get_layer_by_name("Tiles").tiles():
                sprites.Sprite((x*TILE_SIZE+LEVEL_WIDTH*i, y*TILE_SIZE-TILE_SIZE), tile, (self.all_sprites, self.visible_sprites))
            for item in pytmx_map.get_layer_by_name("Collideable"):
                sprites.Sprite((item.x+LEVEL_WIDTH*i, item.y-TILE_SIZE), pygame.Surface((item.width, item.height)), (self.all_sprites, self.collision_sprites))
            for item in pytmx_map.get_layer_by_name("SpikeColliders"):
                sprites.Spike(item.name, (item.x+LEVEL_WIDTH*i, item.y-TILE_SIZE), pygame.Surface((item.width, item.height)), (self.all_sprites, self.collision_sprites, self.spike_colliders_sprites))

        pytmx_map = load_pygame(os_join("assets", "map", "FinalScreen.tmx"))
        for x, y, tile in pytmx_map.get_layer_by_name("Background").tiles():
            sprites.Sprite((x * TILE_SIZE + LEVEL_WIDTH * LEVELS, y * TILE_SIZE - TILE_SIZE), tile,
                           (self.all_sprites, self.visible_sprites))
        for x, y, tile in pytmx_map.get_layer_by_name("Tiles").tiles():
            sprites.Sprite((x * TILE_SIZE + LEVEL_WIDTH * LEVELS, y * TILE_SIZE - TILE_SIZE), tile,
                           (self.all_sprites, self.visible_sprites))
        for item in pytmx_map.get_layer_by_name("Collideable"):
            sprites.Sprite((item.x + LEVEL_WIDTH * LEVELS, item.y - TILE_SIZE), pygame.Surface((item.width, item.height)),
                           (self.all_sprites, self.collision_sprites))

    def main_menu(self):
        bg_image = pygame.image.load(os_join("assets", "images", "background.jpg"))
        bg_image = pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        dark_mask = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        thunder_sound = pygame.mixer.Sound(os_join('assets', 'audio', 'soundeffects', 'thunder2.mp3'))
        lightning_event_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(lightning_event_timer, 1000)
        is_lighten = False
        lightning_blick_event_timer = pygame.USEREVENT + 1
        blicks = 0
        blicks_max = 9
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == lightning_event_timer:
                    if not is_lighten:
                        thunder_sound.play()
                        is_lighten = True
                        pygame.time.set_timer(lightning_event_timer, 0)
                        pygame.time.set_timer(lightning_blick_event_timer, 100)
                        blicks_max = 9 + random.randint(0,3)*3
                if event.type == lightning_blick_event_timer:
                    if blicks <= blicks_max:
                        if blicks % 3 == 0:
                            dark_mask.fill((0,0,0))
                        else:
                            mask_color = random.randint(20, 255)
                            dark_mask.fill((mask_color, mask_color, mask_color))
                        blicks += 1
                    else:
                        is_lighten = False
                        blicks = 0
                        pygame.time.set_timer(lightning_blick_event_timer, 0)
                        pygame.time.set_timer(lightning_event_timer, random.randint(2000, 6000))

            self.display.blit(bg_image, (0, 0))
            self.display.blit(dark_mask, (0, 0), special_flags=pygame.BLEND_MULT)
            pygame.display.update()


    def screen_slide(self):
        self.all_sprites.offset(self.screen_sliding_speed)
        self.light_source.offset(self.screen_sliding_speed)
        self.x += abs(self.screen_sliding_speed[0])
        self.distance += abs(self.screen_sliding_speed[0])
        if(self.distance >= CHANGING_SPEED_THRESHOLD):
            self.distance = 0
            self.screen_sliding_speed = (self.screen_sliding_speed[0]-0.05, 0)

    def run(self):
        while self.running:
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
            self.visible_sprites.draw()
            self.light_source.draw()
            if(self.was_light_source_dragged):
                if(self.x <= LEVEL_WIDTH*(LEVELS)):
                    self.screen_slide()
            self.running = (not self.light_source.is_out_of_bounds()) and self.light_source.get_is_alive()
            # self.display.blit(self.progress_bar, (80, 610))
            self.progress_bar.draw(self.x)
            pygame.display.update()
        self.defeat()

    def defeat(self):
        self.music.stop()
        self.defeat_sound.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.light_source.defeat_animation()
            text = self.font.render("Try again", True, (255, 255, 255))
            self.display.blit(text, (200, 200))
            self.progress_bar.draw(self.x)
            pygame.display.update()

class MainMenu:
    def __init__(self):
        pass
game = Game()
game.main_menu()
# game.run()