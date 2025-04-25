import pygame as pg
from settings import *


# Define um valor que representa espaço vazio no mapa (None -> False no contexto do mapa)
_ = False

# Matriz que representa o mapa do jogo (mini mapa)
# Cada número representa um tipo de parede ou objeto; False representa espaço vazio
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 3, 1, 3, 1, _, _, _, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, 3, 1, 3, 1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 4, _, _, _, 4, _, _, _, _, _, _, 1],
    [1, 1, 1, 3, 1, 3, 1, 1, 1, 1, _, _, 3, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, _, 3, 1, 1, 1],
    [1, 1, 3, 1, 1, 1, 1, 1, 1, 3, _, _, 1, 1, 1, 1],
    [1, 4, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, 3, 4, _, 4, 3, _, 1],
    [1, _, _, 5, _, _, _, _, _, _, 3, _, 3, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 4, _, _, _, _, _, _, 4, _, _, 4, _, _, _, 1],
    [1, 1, 3, 1, _, _, 1, 3, 1, 3, 3, 1, 3, 1, 1, 1],
    [1, 1, 1, 3, _, _, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 3, 4, _, _, 4, 3, 1, 3, 1, 3, 1, 3, 3, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, 5, _, _, _, 5, _, _, _, 5, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]


# Classe que representa o mapa do jogo
class Map:
    def __init__(self, game):
        self.game = game  # Referência ao objeto principal do jogo
        self.mini_map = mini_map  # Atribui o mini mapa à instância
        self.world_map = {}  # Dicionário que armazenará as posições ocupadas
        self.rows = len(self.mini_map)  # Número de linhas do mapa
        self.cols = len(self.mini_map[0])  # Número de colunas do mapa
        self.get_map()  # Preenche o world_map com as coordenadas dos blocos existentes

    def get_map(self):
        # Percorre cada linha (j) e coluna (i) do mini mapa
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:  # Se houver valor (parede/objeto), adiciona ao world_map
                    self.world_map[(i, j)] = value

    def draw(self):
        # Desenha cada célula ocupada do mapa como um retângulo na tela (para debug ou visualização)
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]

    def draw_minimap(self, minimap_pos, minimap_size):
        # Obtém a posição do jogador
        player_x, player_y = self.game.player.pos

        # Tamanho do mini mapa na tela
        minimap_width = minimap_size[0]
        minimap_height = minimap_size[1]
        
        # Converte a posição do jogador para a escala do mini mapa
        player_mini_map_x = int(player_x * minimap_width / self.cols)
        player_mini_map_y = int(player_y * minimap_height / self.rows)

        # Desenha o fundo do mini mapa
        pg.draw.rect(self.game.screen, 'black', (minimap_pos[0], minimap_pos[1], minimap_width, minimap_height))
        
        # Desenha cada célula ocupada no mini mapa
        for pos in self.world_map:
            pg.draw.rect(self.game.screen, 'darkgray', (
                pos[0] * minimap_width / self.cols + minimap_pos[0], 
                pos[1] * minimap_height / self.rows + minimap_pos[1], 
                minimap_width / self.cols, 
                minimap_height / self.rows), 1)
        
        # Desenha o jogador como um ponto vermelho no mini mapa
        pg.draw.circle(self.game.screen, 'red', 
                    (player_mini_map_x + minimap_pos[0], player_mini_map_y + minimap_pos[1]), 4)

