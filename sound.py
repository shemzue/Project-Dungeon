import pygame as pg

<<<<<<< HEAD
=======

>>>>>>> 034391dde53b17231855bacc11ab115141792795
class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'
<<<<<<< HEAD

        # Sons de armas
        self.weapon_sounds = {
            'fireball': pg.mixer.Sound(self.path + 'fireball.wav'),
            'slash': pg.mixer.Sound(self.path + 'slash.wav'),
            'shotgun': pg.mixer.Sound(self.path + 'shotgun.wav')
        }

        # Sons de NPC e jogador
=======
        self.shotgun = pg.mixer.Sound(self.path + 'fireball.wav')
>>>>>>> 034391dde53b17231855bacc11ab115141792795
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav')
        self.npc_shot.set_volume(0.2)
<<<<<<< HEAD

        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')

        # Música de fundo
        self.theme = pg.mixer.music.load(self.path + 'witch.mp3')
        pg.mixer.music.set_volume(0.3)

    def play_weapon_sound(self, weapon_type=None):
        # Usa a arma ativa se não for fornecida
        weapon_type = weapon_type or self.game.weapon.weapon_type
        sound = self.weapon_sounds.get(weapon_type)

        if sound:
            sound.play()
        else:
            print(f"[SOUND DEBUG] Nenhum som encontrado para arma: {weapon_type}")
=======
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        self.theme = pg.mixer.music.load(self.path + 'witch.mp3')
        pg.mixer.music.set_volume(0.3)
>>>>>>> 034391dde53b17231855bacc11ab115141792795
