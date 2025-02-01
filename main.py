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
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 96)

        self.initial_game_settings()

        self.music = pygame.mixer.Sound(os_join('assets', 'audio', 'Checking Manifest.mp3'))
        self.music.set_volume(0.5)
        self.main_menu_music = pygame.mixer.Sound(os_join('assets', 'audio', 'Electricity.wav'))
        self.main_menu_music.set_volume(0.7)
        self.defeat_sound = pygame.mixer.Sound(os_join('assets', 'audio', 'soundeffects', 'game-die.mp3'))
        self.defeat_sound.set_volume(0.5)
        self.main_menu_music.play(loops=-1)

    def initial_game_settings(self):
        self.all_sprites = groups.AllSprites()
        self.visible_sprites = groups.VisibleSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.spike_colliders_sprites = pygame.sprite.Group()
        self.light_source = player.LightSource((200, 200), 100, self.collision_sprites, self.spike_colliders_sprites)
        self.is_dragging_light = False
        self.was_light_source_dragged = False
        self.screen_sliding_speed = 50
        self.x = 0
        self.distance = 0
        self.progress_bar = ui.Progress_Bar(80,610, LEVEL_WIDTH*(LEVELS))
        self.prepare_map()

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
        level_selection_sound = pygame.mixer.Sound(os_join('assets', 'audio', 'soundeffects', 'level_selection.wav'))
        thunder_sound = pygame.mixer.Sound(os_join('assets', 'audio', 'soundeffects', 'thunder.mp3'))
        lightning_event_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(lightning_event_timer, 1000)
        is_lighten = False
        lightning_blick_event_timer = pygame.USEREVENT + 1
        blicks = 0
        blicks_max = 12
        play_button = ui.Button("PLAY", (80, 200), 60)
        tutorial_button = ui.Button("tutorial", (80, 270), 40)
        exit_button = ui.Button("exit", (80, 310), 40)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # checking for click on buttons
                    if event.button == 1:
                        if play_button.is_hovered:
                            running = False
                            level_selection_sound.play()
                            pygame.time.wait(700)
                            play_button.change_cursor_to_arrow()
                            self.main_menu_music.stop()
                            self.run()
                        if tutorial_button.is_hovered:
                            running = False
                            tutorial_button.change_cursor_to_arrow()
                            self.tutorial_screen()
                        if exit_button.is_hovered:
                            pygame.quit()
                            sys.exit()

                if event.type == lightning_event_timer:
                    if not is_lighten:
                        thunder_sound.play()
                        is_lighten = True
                        pygame.time.set_timer(lightning_event_timer, 0)
                        pygame.time.set_timer(lightning_blick_event_timer, 100)
                        blicks_max = 12 + random.randint(0,3)*3
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
            play_button.draw()
            tutorial_button.draw()
            exit_button.draw()
            pygame.display.update()


    def screen_slide(self, delta_time):
        self.all_sprites.offset((-self.screen_sliding_speed*delta_time,0))
        self.light_source.offset((-self.screen_sliding_speed*delta_time,0))
        self.x += self.screen_sliding_speed*delta_time
        self.distance += self.screen_sliding_speed*delta_time
        if(self.distance >= CHANGING_SPEED_THRESHOLD):
            self.distance = 0
            self.screen_sliding_speed = self.screen_sliding_speed+10

    def run(self):
        running = True
        self.initial_game_settings()
        self.music.play(loops=-1)
        while running:
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
                    self.screen_slide(delta_time)
                else:
                    self.win_screen()
            running = (not self.light_source.is_out_of_bounds()) and self.light_source.get_is_alive()
            self.progress_bar.draw(self.x)
            pygame.display.update()
        self.defeat()

    def defeat(self):
        self.music.stop()
        self.defeat_sound.play()
        text = self.font.render("You lost", True, (255, 255, 255))
        try_button = ui.Button("try again", (180, 350), 40)
        main_menu_button = ui.Button("back to menu", (580, 350), 40)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # checking for click on buttons
                    if event.button == 1:
                        if try_button.is_hovered:
                            running = False
                            try_button.change_cursor_to_arrow()
                            self.run()
                        if main_menu_button.is_hovered:
                            running = False
                            main_menu_button.change_cursor_to_arrow()
                            self.main_menu_music.play(loops=-1)
                            self.main_menu()

            self.light_source.defeat_animation()
            self.display.blit(text, (280, 200))
            self.progress_bar.draw(self.x)
            try_button.draw()
            main_menu_button.draw()
            pygame.display.update()

    def win_screen(self):
        win_text = self.font.render("Congratulations", True, (255, 255, 255))
        main_menu_button = ui.Button("back to menu", (350, 300), 40)
        sprites.Sprite((-TILE_SIZE, 0), pygame.Surface((TILE_SIZE, WINDOW_HEIGHT)), self.collision_sprites) #collider for left screen side
        win_sound = pygame.mixer.Sound(os_join("assets", "audio", "soundeffects", "level_complete.wav"))
        win_sound.set_volume(0.5)
        win_sound.play()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.light_source.hitbox_rect.collidepoint(pygame.mouse.get_pos()):
                            self.is_dragging_light = True
                        # checking for click on buttons
                        if main_menu_button.is_hovered:
                            running = False
                            self.music.stop()
                            main_menu_button.change_cursor_to_arrow()
                            self.main_menu_music.play(loops=-1)
                            self.main_menu()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.is_dragging_light = False
            delta_time = self.clock.tick() / 1000
            if self.is_dragging_light:
                self.light_source.move_by_mouse(delta_time)
            else:
                if (abs(self.light_source.get_displacement()[0]) > APPROXIMATE_ZERO and abs(
                        self.light_source.get_displacement()[1]) > APPROXIMATE_ZERO):
                    self.light_source.momentum(delta_time)
            self.visible_sprites.draw()
            self.light_source.draw()
            self.progress_bar.draw(self.x)
            self.display.blit(win_text, (80, 200))
            main_menu_button.draw()
            pygame.display.update()
    def tutorial_screen(self):
        running = True
        bg_image = pygame.image.load(os_join("assets", "images", "tutorial.png"))
        main_menu_button = ui.Button("back to menu", (40, 540), 40)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # checking for click on buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if main_menu_button.is_hovered:
                            running = False
                            self.main_menu()

            self.display.blit(bg_image, (0, 0))
            main_menu_button.draw()
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.main_menu()
