
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centraliza a janela

import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
from menu import menu_loop

player_info = menu_loop()
print("Iniciando jogo com:", player_info)

class_to_weapon = {
    "Mago": "fireball",
    "Guerreiro": "slash",
    "Atirador": "shotgun"
}

class Game:
    def __init__(self, player_name, weapon_type):
        self.player_name = player_name
        self.weapon_type = weapon_type
        pg.init()
        pg.mouse.set_visible(False)  # Mouse invisível
        # Pega a resolução atual do monitor
        info = pg.display.Info()  # Informações sobre o monitor
        monitor_width, monitor_height = info.current_w, info.current_h
        self.screen = pg.display.set_mode((monitor_width, monitor_height), pg.RESIZABLE)  # Janela redimensionável
        pg.display.set_caption("Dungeon Game")  # Só pra dar um nome à janela
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.paused = False
        self.new_game()

    def new_game(self):
        self.player = Player(self)
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self, weapon_type=self.weapon_type)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        if not self.paused:
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
            self.weapon.update()
            pg.display.flip()
            self.delta_time = self.clock.tick(FPS)
            pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        if not self.paused:
            self.object_renderer.draw()
            self.weapon.draw()
            # Chama o método para desenhar o mini mapa
            minimap_size = (200, 200)
            minimap_pos = (self.screen.get_width() - minimap_size[0] - 10, 10)
            self.map.draw_minimap(minimap_pos, minimap_size)

    def show_pause_menu(self):
        pause_font = pg.font.SysFont("Arial", 36)
        options = ["Continuar", "Menu Principal", "Sair"]
        selected = 0
        while self.paused:
            self.screen.fill((30, 30, 30))
            for i, option in enumerate(options):
                color = (255, 255, 255) if i == selected else (150, 150, 150)
                text = pause_font.render(option, True, color)
                self.screen.blit(text, (100, 100 + i * 50))
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pg.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pg.K_RETURN:
                        if selected == 0:
                            self.paused = False
                            pg.mouse.set_visible(False)
                        elif selected == 1:
                            from menu import menu_loop
                            player_info = menu_loop()
                            self.__init__(player_info["name"], class_to_weapon[player_info["class"]])
                        elif selected == 2:
                            pg.quit()
                            sys.exit()


    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.paused = not self.paused
                pg.mouse.set_visible(self.paused)
                pg.event.set_grab(not self.paused)
                if self.paused:
                    self.show_pause_menu()
            elif event.type == pg.VIDEORESIZE:
                # Quando a janela for redimensionada, ajuste a tela e o mapa
                self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                # Atualize as variáveis de largura e altura
                global WIDTH, HEIGHT
                WIDTH, HEIGHT = event.w, event.h
                HALF_WIDTH = WIDTH // 2
                HALF_HEIGHT = HEIGHT // 2
                # Aqui você pode chamar outras funções que precisam ser ajustadas com a nova resolução
            elif event.type == self.global_event:
                self.global_trigger = True
            if not self.paused:
                self.player.single_fire_event(event)


    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
if __name__ == '__main__':
    player_info = menu_loop()
    print("Iniciando jogo com:", player_info)

    class_to_weapon = {
        "Mago": "fireball",
        "Guerreiro": "slash",
        "Atirador": "shotgun"
    }

    weapon_type = class_to_weapon.get(player_info["class"], "fireball")
    game = Game(player_info["name"], weapon_type)
    game.run()
