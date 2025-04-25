import pygame as pg
from settings import *
import os
from collections import deque


# Classe base para qualquer sprite estático (ex: candelabro)
class SpriteObject:
    def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png',
                 pos=(10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game
        self.player = game.player
        self.x, self.y = pos  # posição do sprite no mapa
        self.image = pg.image.load(path).convert_alpha()  # carrega a imagem com canal alpha (transparência)

        # Guarda as dimensões e proporção da imagem
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()

        # Variáveis relacionadas à renderização e posição relativa ao jogador
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale  # escala visual do sprite
        self.SPRITE_HEIGHT_SHIFT = shift  # deslocamento vertical (para ajustar a altura do sprite na tela)

    def get_sprite_projection(self):
        # Calcula o tamanho projetado do sprite na tela
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        # Redimensiona a imagem conforme a distância
        image = pg.transform.scale(self.image, (proj_width, proj_height))
        self.sprite_half_width = proj_width // 2

        # Ajusta a posição vertical com base no shift
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        # Adiciona o sprite para ser desenhado no frame atual
        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        # Calcula a posição relativa entre o jogador e o sprite
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy

        # Ângulo do sprite em relação ao jogador
        self.theta = math.atan2(dy, dx)
        delta = self.theta - self.player.angle

        # Corrige erro de ângulo em situações específicas
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        # Quantas "rays" separam o centro da tela do sprite
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        # Distância corrigida (sem efeito de olho de peixe)
        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)

        # Só renderiza o sprite se ele estiver visível na tela e suficientemente perto
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()


# Subclasse para sprites animados (como luzes piscantes)
class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time  # tempo entre quadros da animação (ms)
        self.path = path.rsplit('/', 1)[0]  # pega o diretório base da animação
        self.images = self.get_images(self.path)  # carrega todos os quadros da animação
        self.animation_time_prev = pg.time.get_ticks()  # marca o tempo do último frame animado
        self.animation_trigger = False  # flag para ativar a animação

    def update(self):
        super().update()  # atualiza posição e renderização
        self.check_animation_time()  # verifica se é hora de trocar o quadro
        self.animate(self.images)  # gira os quadros da animação

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)  # move o primeiro quadro para o final
            self.image = images[0]  # define o novo quadro atual

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True  # ativa a troca de quadro

    def get_images(self, path):
        # Lê todos os arquivos de imagem no diretório e os coloca numa fila circular (deque)
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
