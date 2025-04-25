from settings import *  # Importa constantes e configurações do jogo
import pygame as pg  # Biblioteca gráfica
import math  # Funções matemáticas


class Player:
    def __init__(self, game, name='Player', weapon_type='fireball'):
        self.game = game  # Referência ao objeto principal do jogo
        self.name = name
        self.weapon_type = weapon_type
        self.x, self.y = PLAYER_POS  # Posição inicial do jogador
        self.angle = PLAYER_ANGLE  # Ângulo inicial de visão
        self.shot = False  # Controla se o jogador atirou
        self.health = PLAYER_MAX_HEALTH  # Vida inicial do jogador
        self.rel = 0  # Variação do mouse
        self.health_recovery_delay = 700  # Tempo entre recuperações de vida
        self.time_prev = pg.time.get_ticks()  # Marca o último momento de recuperação
        self.diag_move_corr = 1 / math.sqrt(2)  # Correção de velocidade para movimento diagonal

    def recover_health(self):
        # Recupera 1 ponto de vida se o tempo de espera passou
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        # Verifica se o tempo para recuperar vida passou
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):
        # Verifica se o jogador morreu
        if self.health < 1:
            self.game.object_renderer.game_over()  # Mostra tela de "game over"
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()  # Reinicia o jogo

    def get_damage(self, damage):
        # Aplica dano ao jogador
        self.health -= damage
        self.game.object_renderer.player_damage()  # Efeito visual de dano
        self.game.sound.player_pain.play()  # Som de dor
        self.check_game_over()

    def single_fire_event(self, event):
        # Evento de clique de mouse (tiro)
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.play_weapon_sound()  # Som da arma
                self.shot = True
                self.game.weapon.reloading = True  # Inicia recarregamento

    def movement(self):
        # Lógica de movimentação do jogador com base nas teclas pressionadas
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1  # Para verificar movimento diagonal

        if keys[pg.K_w]:  # Frente
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:  # Trás
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:  # Esquerda (strafe)
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:  # Direita (strafe)
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos

        # Corrige a velocidade em movimento diagonal
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        self.check_wall_collision(dx, dy)

        # ROTAÇÃO do jogador (foi comentado, porque agora usa mouse)
        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.delta_time

        self.angle %= math.tau  # Mantém o ângulo entre 0 e 2π

    def check_wall(self, x, y):
        # Verifica se a posição não é uma parede
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        # Evita que o jogador atravesse paredes
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        # Desenha linha de visão e posição do jogador no mini mapa
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                     (self.x * 100 + WIDTH * math.cos(self.angle),
                      self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        # Controle da rotação usando o mouse
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            # Centraliza o mouse se ele sair dos limites horizontais
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])

        self.rel = pg.mouse.get_rel()[0]  # Movimento horizontal do mouse
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))  # Limita rotação
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time  # Aplica rotação

    def update(self):
        # Atualização principal por frame: movimentação, mouse e recuperação de vida
        self.movement()
        self.mouse_control()
        self.recover_health()

    @property
    def pos(self):
        # Posição precisa do jogador
        return self.x, self.y

    @property
    def map_pos(self):
        # Posição arredondada para o grid do mapa
        return int(self.x), int(self.y)
