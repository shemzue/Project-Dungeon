import pygame as pg
import math
from settings import *  # Importa constantes como FOV, TEXTURE_SIZE, etc.


class RayCasting:
    def __init__(self, game):
        self.game = game  # Referência ao objeto principal do jogo
        self.ray_casting_result = []  # Armazena os dados de cada raio (profundidade, altura projetada, textura, offset)
        self.objects_to_render = []  # Lista de objetos a serem desenhados na tela
        self.textures = self.game.object_renderer.wall_textures  # Dicionário de texturas das paredes

    def get_objects_to_render(self):
        """Converte os resultados do ray casting em colunas de textura que serão desenhadas na tela."""
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            # Se a projeção é menor que a altura da tela
            if proj_height < HEIGHT:
                # Recorta uma coluna da textura baseada no offset
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                # Redimensiona a coluna para altura projetada
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                # Se a parede é maior que a tela, recorta só a parte visível da textura
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE),
                    HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE,
                    texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            # Armazena para renderização posterior
            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        """Realiza o ray casting em múltiplos ângulos, um para cada raio da tela."""
        self.ray_casting_result = []
        texture_vert, texture_hor = 1, 1  # Texturas padrão
        ox, oy = self.game.player.pos  # Posição do jogador
        x_map, y_map = self.game.player.map_pos  # Posição arredondada (tile) do jogador

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001  # Começa do lado esquerdo da visão
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # ---------- Interseções horizontais ----------
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # ---------- Interseções verticais ----------
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # ---------- Escolhe a menor profundidade (mais próxima) ----------
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1  # Pega a fração da coordenada para offset da textura
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # ---------- Corrige o efeito fish-eye ----------
            depth *= math.cos(self.game.player.angle - ray_angle)

            # ---------- Projeção na tela ----------
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # ---------- Salva resultado ----------
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            # Avança para o próximo raio
            ray_angle += DELTA_ANGLE

    def update(self):
        """Atualiza o ray casting e os objetos a serem desenhados na tela."""
        self.ray_cast()
        self.get_objects_to_render()
