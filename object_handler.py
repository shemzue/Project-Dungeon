# Importa todas as classes e funções dos módulos sprite_object e npc
from sprite_object import *
from npc import *
from random import choices, randrange  # Importa funções para seleção aleatória

# Classe que gerencia todos os objetos do jogo (sprites e NPCs)
class ObjectHandler:
    def __init__(self, game):
        self.game = game  # Referência ao objeto principal do jogo
        self.sprite_list = []  # Lista de sprites (objetos estáticos ou animados)
        self.npc_list = []  # Lista de NPCs (personagens não jogáveis)
        self.npc_sprite_path = 'resources/sprites/npc/'  # Caminho para sprites dos NPCs
        self.static_sprite_path = 'resources/sprites/static_sprites/'  # Caminho para sprites estáticos
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'  # Caminho para sprites animados
        add_sprite = self.add_sprite  # Atalho para o método add_sprite
        add_npc = self.add_npc  # Atalho para o método add_npc
        self.npc_positions = {}  # Dicionário que guarda as posições dos NPCs

        # Configura a geração de NPCs
        self.enemies = 15  # Quantidade total de NPCs no mapa
        self.npc_types = [ZumbiNPC, GoblinNPC]  # Tipos de NPCs disponíveis

        # self.npc_types = [gato, cachorro, zumbi]  # Exemplo de outros tipos que podem ser usados
        self.weights = [70, 30]  # Probabilidades de aparecer cada tipo de NPC
        # self.weights = [70, 20, 10]  # Exemplo de proporções para mais tipos de NPCs
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}  # Área onde NPCs não podem nascer
        self.spawn_npc()  # Chama função que adiciona os NPCs no mapa aleatoriamente

        # Adiciona sprites animados em posições específicas do mapa
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 24.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 24.5)))
        # Vários sprites com sprite específico "red_light"
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 5.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(12.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 12.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(10.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 14.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 18.5)))


        # Exemplo de NPCs que poderiam ser adicionados manualmente:
        # add_npc(ZumbiNPC(game, pos=(2.0, 20.0)))
        # add_npc(GoblinNPC(game, pos=(5.5, 16.5)))

    # Gera NPCs em posições aleatórias, evitando áreas restritas e obstáculos
    def spawn_npc(self):
        for i in range(self.enemies):
            npc = choices(self.npc_types, self.weights)[0]  # Escolhe tipo de NPC com base nos pesos
            pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)  # Gera posição aleatória
            # Garante que a posição não está ocupada nem em área restrita
            while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
            self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))  # Adiciona o NPC ajustando a posição para o centro da célula

    # Verifica se todos os NPCs foram derrotados e reinicia o jogo se necessário
    def check_win(self):
        if not len(self.npc_positions):  # Se não há NPCs vivos
            self.game.object_renderer.win()  # Mostra tela de vitória
            pg.display.flip()  # Atualiza display
            pg.time.delay(1500)  # Espera 1.5 segundos
            self.game.new_game()  # Reinicia o jogo

    # Atualiza todos os sprites e NPCs do jogo
    def update(self):
        # Atualiza dicionário com posições dos NPCs vivos
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]  # Atualiza cada sprite
        [npc.update() for npc in self.npc_list]  # Atualiza cada NPC
        self.check_win()  # Verifica condição de vitória

    # Adiciona um NPC à lista
    def add_npc(self, npc):
        self.npc_list.append(npc)

    # Adiciona um sprite à lista
    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
