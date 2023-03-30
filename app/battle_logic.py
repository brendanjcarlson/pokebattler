from random import randint, choice

class BattlePokemon:
    def __init__(self, pokename, base_hp, base_atk, base_def, base_spd):
        self.pokename = pokename
        self.base_def = base_def
        self.base_atk = base_atk
        self.base_spd = base_spd
        self.base_hp = base_hp
        self.curr_hp = base_hp

    def attack(self, other):
        dmg = self.base_atk
        crit = False
        # critical hit chance
        if randint(0, 100) < 10:
            dmg *= 2
            crit = True
        # dodge chance
        if other.base_spd - 20 > self.base_spd:
            if randint(0, 100) < 20:
                return 'missed', crit
        # damage calculation
        if other.base_def - self.base_atk > 20:
            dmg *= choice([0.5, 0.6, 0.7, 0.8, 0.9])
        elif other.base_def - self.base_atk < -20:
            dmg *= choice([1, 1.1, 1.2, 1.3, 1.4])
        dmg = int(dmg)
        other.curr_hp -= dmg
        return dmg, crit

    @property
    def is_fainted(self):
        return self.curr_hp <= 0

class BattleTeam:
    def __init__(self, user):
        self.user = user
        self.team = []
        self.is_turn = False

    def build_team(self):
        for poke in self.user.caught.all():
            battle_poke = BattlePokemon(poke.name.title(), poke.base_hp, poke.base_atk, poke.base_def, poke.base_spd)
            self.team.append(battle_poke)

    def faint_pokemon(self, pokemon):
        self.team.remove(pokemon)

class BattleGame:
    def __init__(self, A, B):
        self.A = BattleTeam(A)
        self.B = BattleTeam(B)
        self.log = []

    def start(self):
        self.A.build_team()
        self.B.build_team()
        if self.A.team[0].base_spd > self.B.team[0].base_spd:
            self.A.is_turn = True

    def next_player(self):
        self.A.is_turn, self.B.is_turn = not self.A.is_turn, not self.B.is_turn

    def battle(self):
        self.start()
        while True:

            if self.A.is_turn:
                fight = self.A.team[0].attack(self.B.team[0])
                if isinstance(fight[0], str):
                    self.log.append(f'{self.A.team[0].pokename} tried to attack {self.B.team[0].pokename} but {fight[0]}!')
                elif fight[1]:
                    self.log.append(f'{self.A.team[0].pokename} attacked {self.B.team[0].pokename} for {fight[0]} damage! Critical hit!')
                else:
                    self.log.append(f'{self.A.team[0].pokename} attacked {self.B.team[0].pokename} for {fight[0]} damage')

                if self.B.team[0].is_fainted:
                    self.log.append(f'{self.B.team[0].pokename} fainted!')
                    self.B.faint_pokemon(self.B.team[0])

                    if not self.B.team:
                        self.log.append(f'{self.B.user.username} is out of pokemans!')
                        self.log.append(f'{self.A.user.username} wins!')
                        self.A.user.ADD_WIN()
                        self.B.user.ADD_LOSS()
                        return (self.A.user.username, self.B.user.username, self.log)

            else:
                fight = self.B.team[0].attack(self.A.team[0])
                if isinstance(fight[0], str):
                    self.log.append(f'{self.B.team[0].pokename} tried to attack {self.A.team[0].pokename} but {fight[0]}!')
                elif fight[1]:
                    self.log.append(f'{self.B.team[0].pokename} attacked {self.A.team[0].pokename} for {fight[0]} damage! Critical hit!')
                else:
                    self.log.append(f'{self.B.team[0].pokename} attacked {self.A.team[0].pokename} for {fight[0]} damage')

                if self.A.team[0].is_fainted:
                    self.log.append(f'{self.A.team[0].pokename} fainted!')
                    self.A.faint_pokemon(self.A.team[0])

                    if not self.A.team:
                        self.log.append(f'{self.A.user.username} is out of pokemans!')
                        self.log.append(f'{self.B.user.username} wins!')
                        self.B.user.ADD_WIN()
                        self.A.user.ADD_LOSS()
                        return (self.B.user.username, self.A.user.username, self.log)

            self.next_player()