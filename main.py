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
import platform  # Biblioteca para detectar o sistema operacional

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
        # Inicializa variáveis do jogador
        self.player_name = player_name
        self.weapon_type = weapon_type
        pg.init()  # Inicializa o pygame
        pg.mouse.set_visible(False)  # Esconde o cursor do mouse

        # Pega a resolução atual do monitor
        info = pg.display.Info()
        self.monitor_width, self.monitor_height = info.current_w, info.current_h

        # Define a resolução da janela do jogo
        self.width, self.height = self.monitor_width, self.monitor_height
        
        # Cria a janela do jogo
        self.screen = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)
        
        # Atualiza variáveis globais de resolução
        global WIDTH, HEIGHT, HALF_WIDTH, HALF_HEIGHT
        WIDTH, HEIGHT = self.width, self.height
        HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
        
        pg.display.set_caption("Dungeon Game")  # Define título da janela
        pg.event.set_grab(True)  # Faz o mouse ficar preso na janela

        self.clock = pg.time.Clock()  # Controle de FPS
        self.delta_time = 1  # Delta de tempo para o próximo frame
        self.global_trigger = False  # Usado para eventos repetitivos
        self.global_event = pg.USEREVENT + 0  # Evento personalizado
        pg.time.set_timer(self.global_event, 40)  # Dispara a cada 40ms

        self.paused = False  # Indica se o jogo está pausado
        self.new_game()  # Inicia uma nova partida

    def new_game(self):
        # Inicializa todos os sistemas e objetos do jogo
        self.player = Player(self)
        self.map = Map(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self, weapon_type=self.weapon_type)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)  # Toca a música de fundo em loop

    def update(self):
        # Atualiza o estado do jogo, se não estiver pausado
        if not self.paused:
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
            self.weapon.update()
            pg.display.flip()  # Atualiza o display
            self.delta_time = self.clock.tick(FPS)  # Mantém o FPS
            pg.display.set_caption(f'{self.clock.get_fps():.1f}')  # Exibe o FPS

    def draw(self):
        # Desenha a cena do jogo
        if not self.paused:
            self.screen.fill((0, 0, 0))  # Preenche o fundo de preto
            self.object_renderer.draw()

            # Ajustes gráficos específicos para Linux
            if platform.system() == "Linux":
                floor_height = 110  # Altura do "chão" preto
                pg.draw.rect(self.screen, (0, 0, 0),
                             (0, self.screen.get_height() - floor_height,
                              self.screen.get_width(), floor_height))
                self.weapon.draw()

                # Corrige a borda direita da tela
                ray_width = NUM_RAYS * SCALE
                screen_width = self.screen.get_width()
                if ray_width < screen_width:
                    pg.draw.rect(self.screen, (0, 0, 0),
                                 (ray_width, 0, screen_width - ray_width,
                                  self.screen.get_height()))
            else:
                self.weapon.draw()

            # Desenha o minimapa
            minimap_size = (200, 200)
            minimap_pos = (self.screen.get_width() - minimap_size[0] - 10, 10)
            self.map.draw_minimap(minimap_pos, minimap_size)

    def show_pause_menu(self):
        # Exibe o menu de pausa
        pause_font = pg.font.SysFont("Arial", 36)
        options = ["Continuar", "Menu Principal", "Sair"]
        selected = 0

        while self.paused:
            self.screen.fill((30, 30, 30))  # Fundo cinza escuro

            # Desenha as opções
            for i, option in enumerate(options):
                color = (255, 255, 255) if i == selected else (150, 150, 150)
                text = pause_font.render(option, True, color)
                self.screen.blit(text, (100, 100 + i * 50))
            pg.display.flip()

            # Lida com eventos no menu de pausa
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
                        if selected == 0:  # Continuar o jogo
                            self.paused = False
                            pg.mouse.set_visible(False)
                        elif selected == 1:  # Voltar para o menu principal
                            from menu import menu_loop
                            player_info = menu_loop()
                            self.__init__(player_info["name"], class_to_weapon[player_info["class"]])
                        elif selected == 2:  # Sair do jogo
                            pg.quit()
                            sys.exit()

    def check_events(self):
        # Trata eventos do pygame
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                # Alterna o estado de pausa
                self.paused = not self.paused
                pg.mouse.set_visible(self.paused)
                pg.event.set_grab(not self.paused)
                if self.paused:
                    self.show_pause_menu()
            elif event.type == pg.VIDEORESIZE:
                # Ajusta para a nova resolução da janela
                self.width, self.height = event.w, event.h
                self.screen = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)

                # Atualiza variáveis globais de resolução
                global WIDTH, HEIGHT, HALF_WIDTH, HALF_HEIGHT
                WIDTH, HEIGHT = self.width, self.height
                HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2

            elif event.type == self.global_event:
                self.global_trigger = True

            # Detecta disparos apenas quando o jogo não está pausado
            if not self.paused:
                self.player.single_fire_event(event)

    def run(self):
        # Loop principal do jogo
        while True:
            self.check_events()
            self.update()
            self.draw()

# Executa o jogo se o script for rodado diretamente
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
