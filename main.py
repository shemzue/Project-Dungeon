# Centraliza a janela do jogo ao abrir
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Importações de bibliotecas e módulos do projeto
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

# Exibe o menu e captura as informações do jogador (nome e classe)
player_info = menu_loop()
print("Iniciando jogo com:", player_info)

# Dicionário que associa a classe do jogador à arma correspondente
class_to_weapon = {
    "Mago": "fireball",
    "Guerreiro": "slash",
    "Atirador": "shotgun"
}

# Classe principal do jogo
class Game:
    def __init__(self, player_name, weapon_type):
        self.player_name = player_name
        self.weapon_type = weapon_type
        pg.init()  # Inicializa o pygame
        pg.mouse.set_visible(False)  # Esconde o cursor do mouse

        # Pega a resolução atual do monitor
        info = pg.display.Info()
        monitor_width, monitor_height = info.current_w, info.current_h

        # Cria uma janela redimensionável com resolução do monitor
        self.screen = pg.display.set_mode((monitor_width, monitor_height), pg.RESIZABLE)
        pg.display.set_caption("Dungeon Game")
        pg.event.set_grab(True)  # Captura o mouse dentro da janela do jogo

        self.clock = pg.time.Clock()  # Relógio para controle de FPS
        self.delta_time = 1  # Delta de tempo entre frames
        self.global_trigger = False  # Usado para controlar eventos repetitivos
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)  # Dispara o evento a cada 40ms

        self.paused = False  # Estado de pausa
        self.new_game()  # Inicializa todos os componentes do jogo

    def new_game(self):
        # Instancia todos os sistemas e objetos necessários para uma nova partida
        self.player = Player(self)
        self.map = Map(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self, weapon_type=self.weapon_type)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)  # Toca música de fundo em loop

    def update(self):
        # Atualiza o estado do jogo se ele não estiver pausado
        if not self.paused:
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
            self.weapon.update()
            pg.display.flip()  # Atualiza a tela
            self.delta_time = self.clock.tick(FPS)  # Controle de FPS
            pg.display.set_caption(f'{self.clock.get_fps():.1f}')  # Exibe o FPS na barra de título

    def draw(self):
        # Desenha todos os elementos visuais na tela
        if not self.paused:
            self.object_renderer.draw()
            self.weapon.draw()

            # Desenha o mini mapa no canto superior direito
            minimap_size = (200, 200)
            minimap_pos = (self.screen.get_width() - minimap_size[0] - 10, 10)
            self.map.draw_minimap(minimap_pos, minimap_size)

    def show_pause_menu(self):
        # Exibe o menu de pausa
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
                        if selected == 0:  # Continuar
                            self.paused = False
                            pg.mouse.set_visible(False)
                        elif selected == 1:  # Voltar ao menu principal
                            from menu import menu_loop
                            player_info = menu_loop()
                            self.__init__(player_info["name"], class_to_weapon[player_info["class"]])
                        elif selected == 2:  # Sair
                            pg.quit()
                            sys.exit()

    def check_events(self):
        # Lida com os eventos do pygame
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                # Alterna entre o estado pausado e não pausado
                self.paused = not self.paused
                pg.mouse.set_visible(self.paused)
                pg.event.set_grab(not self.paused)
                if self.paused:
                    self.show_pause_menu()
            elif event.type == pg.VIDEORESIZE:
                # Quando a janela for redimensionada, atualiza a tela e os parâmetros globais
                self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                global WIDTH, HEIGHT
                WIDTH, HEIGHT = event.w, event.h
                HALF_WIDTH = WIDTH // 2
                HALF_HEIGHT = HEIGHT // 2
            elif event.type == self.global_event:
                self.global_trigger = True

            if not self.paused:
                self.player.single_fire_event(event)  # Detecta cliques para disparo

    def run(self):
        # Loop principal do jogo
        while True:
            self.check_events()
            self.update()
            self.draw()

# Executa o jogo se este script for executado diretamente
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
