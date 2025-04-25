from sprite_object import *
import math

# Classe Weapon, que herda de AnimatedSprite (representa armas como fireball, slash, shotgun etc.)
class Weapon(AnimatedSprite):
    def __init__(self, game, weapon_type="fireball", scale=0.4, animation_time=90):
        self.weapon_type = weapon_type  # Tipo da arma (usado para definir imagens, dano, lógica etc.)

        # Dicionário com os fatores de escala para cada tipo de arma
        scale_factors = {
            'fireball': 0.4,
            'slash': 1.0,
            'shotgun': 0.4
        }

        # Aplica a escala correspondente ao tipo da arma
        scale = scale_factors.get(weapon_type, 0.4)

        # Caminho para as imagens de animação da arma
        dir_path = f'resources/sprites/weapon/{weapon_type}'
        image_files = sorted(os.listdir(dir_path))  # Ordena os arquivos para manter a ordem da animação
        full_paths = [os.path.join(dir_path, img) for img in image_files]

        # DEBUG: imprime os caminhos das imagens carregadas
        print(f"[DEBUG] Imagens carregadas: {full_paths}")

        # Inicializa a classe base (AnimatedSprite) com o primeiro frame como imagem inicial
        super().__init__(game=game, path=full_paths[0], scale=scale, animation_time=animation_time)

        # Sobrescreve a lista de imagens com a animação completa, redimensionada
        self.images = deque(
            [pg.transform.smoothscale(pg.image.load(img).convert_alpha(),
             (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in full_paths]
        )

        # Posição da arma na tela (centro na parte inferior)
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())

        self.reloading = False  # Indica se a arma está no meio de uma animação de disparo
        self.num_images = len(self.images)  # Número de quadros da animação
        self.frame_counter = 0  # Controle de progresso na animação
        self.damage = self.get_damage_by_type(weapon_type)  # Dano causado pela arma

    # Retorna o valor de dano com base no tipo da arma
    def get_damage_by_type(self, weapon_type):
        return {
            'fireball': 50,
            'slash': 100,
            'shotgun': 40
        }.get(weapon_type, 50)  # Valor padrão é 50 caso o tipo seja desconhecido

    # Aplica dano aos NPCs com base no tipo da arma e distância
    def apply_damage(self):
        player = self.game.player
        px, py = player.x, player.y

        for npc in self.game.object_handler.npc_list:
            if not npc.alive:
                continue

            nx, ny = npc.x, npc.y
            dx, dy = nx - px, ny - py
            distance = math.hypot(dx, dy)  # Calcula a distância do jogador ao NPC

            # Lógica para cada tipo de arma
            if self.weapon_type == 'fireball':
                if distance <= 3:
                    npc.health -= self.damage
                    npc.pain = True
                    npc.check_health()

            elif self.weapon_type == 'slash':
                if distance <= 0.6:
                    npc.health -= self.damage
                    npc.pain = True
                    npc.check_health()

            elif self.weapon_type == 'bullet':
                # Verifica se o NPC está na linha de fogo (no centro da tela)
                if npc.ray_cast_value and HALF_WIDTH - npc.sprite_half_width < npc.screen_x < HALF_WIDTH + npc.sprite_half_width:
                    npc.health -= self.damage
                    npc.pain = True
                    npc.check_health()
                    break  # Apenas o primeiro NPC no caminho é atingido

    # Controla a animação de disparo
    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False  # Impede que o jogador atire novamente enquanto recarrega

            if self.animation_trigger:
                self.images.rotate(-1)  # Passa para o próximo frame
                self.image = self.images[0]
                self.frame_counter += 1

                if self.frame_counter == self.num_images:
                    # Fim da animação, reseta estados
                    self.reloading = False
                    self.frame_counter = 0

    # Desenha a arma atual na tela
    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    # Atualiza o estado da arma (animação de tempo e disparo)
    def update(self):
        self.check_animation_time()
        self.animate_shot()
