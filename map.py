import pygame as pg
from settings import *


_ = False
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


class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.rows = len(self.mini_map)
        self.cols = len(self.mini_map[0])
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)

         for pos in self.world_map]
        

    def draw_minimap(self, minimap_pos, minimap_size):
        player_x, player_y = self.game.player.pos
        # Ajuste da escala para o mini mapa, garantindo que a posição do jogador seja corretamente mapeada
        minimap_width = minimap_size[0]
        minimap_height = minimap_size[1]
        
        # Normaliza a posição do jogador para as dimensões do mini mapa
        player_mini_map_x = int(player_x * minimap_width / self.cols)
        player_mini_map_y = int(player_y * minimap_height / self.rows)

        # Desenha o mini mapa (tela reduzida)
        pg.draw.rect(self.game.screen, 'black', (minimap_pos[0], minimap_pos[1], minimap_width, minimap_height))
        
        # Desenha o mundo do mini mapa
        for pos in self.world_map:
            pg.draw.rect(self.game.screen, 'darkgray', (
                pos[0] * minimap_width / self.cols + minimap_pos[0], 
                pos[1] * minimap_height / self.rows + minimap_pos[1], 
                minimap_width / self.cols, 
                minimap_height / self.rows), 1)
        
        # Desenha o ponto vermelho representando o jogador no mini mapa
        pg.draw.circle(self.game.screen, 'red', 
                    (player_mini_map_x + minimap_pos[0], player_mini_map_y + minimap_pos[1]), 4)

