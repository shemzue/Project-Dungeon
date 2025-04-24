from sprite_object import *
import math

class Weapon(AnimatedSprite):
    def __init__(self, game, weapon_type="fireball", scale=0.4, animation_time=90):
        self.weapon_type = weapon_type  # ← Adicionado aqui
        scale_factors = {
            'fireball': 0.4,
            'slash': 1.0,  #controla o tamanho das armas
            'shotgun': 0.4
        }

        scale = scale_factors.get(weapon_type, 0.4)
        dir_path = f'resources/sprites/weapon/{weapon_type}'
        image_files = sorted(os.listdir(dir_path))
        full_paths = [os.path.join(dir_path, img) for img in image_files]

        # DEBUG
        print(f"[DEBUG] Imagens carregadas: {full_paths}")

        # Chama o AnimatedSprite com o primeiro frame só pra base
        super().__init__(game=game, path=full_paths[0], scale=scale, animation_time=animation_time)

        # Substitui as imagens pela animação correta
        self.images = deque(
            [pg.transform.smoothscale(pg.image.load(img).convert_alpha(),
             (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in full_paths]
        )

        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = self.get_damage_by_type(weapon_type)

    def get_damage_by_type(self, weapon_type):
        return {
            'fireball': 50,
            'slash': 100,
            'shotgun': 40
        }.get(weapon_type, 50)    




    def apply_damage(self):
        player = self.game.player
        px, py = player.x, player.y

        for npc in self.game.object_handler.npc_list:
            if not npc.alive:
                continue

            nx, ny = npc.x, npc.y
            dx, dy = nx - px, ny - py
            distance = math.hypot(dx, dy)  # Distância entre o jogador e o NPC

            # Agora os ifs com base na arma e distância
            if self.weapon_type == 'fireball':
                # Se o jogador lançar uma fireball e o NPC estiver dentro de um alcance de 3 unidades
                if distance <= 3:
                    npc.health -= self.damage
                    npc.pain = True
                    npc.check_health()

            elif self.weapon_type == 'slash':
                # Para o ataque de "slash", aplicamos o dano apenas se o NPC estiver a uma distância de até 0.6 unidades
                # Essa lógica não leva mais em consideração o ângulo, apenas a distância
                if distance <= 0.6:
                    npc.health -= self.damage
                    npc.pain = True
                    npc.check_health()

            elif self.weapon_type == 'bullet':
                # Se o tipo de arma for "bullet", o NPC será atingido por uma bala
                if npc.ray_cast_value and HALF_WIDTH - npc.sprite_half_width < npc.screen_x < HALF_WIDTH + npc.sprite_half_width:
                    npc.health -= self.damage
                    npc.pain = True
                    npc.check_health()
                    break  # Apenas atinge o primeiro NPC no caminho da bala





    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()
