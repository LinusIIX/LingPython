# contributors:
# Max

import settings
from random import choices, shuffle

class Upgrade:
    def __init__(self, text, header, effect, weight, value):
        self.text: str = text
        self.header: str = header
        self.effect: str = effect
        self.weight: int = weight
        self.value: int = value

class Upgrades:
    def __init__(self):
        self.min_word_length = Upgrade("MIN_ENEMY", "Smallest enemy", "Decreases the length of the shortest word that can spawn by 1.", 1, settings.CHANGABLE_VARIABLES["word_length_min"])
        self.max_word_length = Upgrade("MAX_ENEMY", "Largest enemy", "Decreases the length of the longest word that can spawn by 1.", 1, settings.CHANGABLE_VARIABLES["word_length_max"])
        self.enemy_speed = Upgrade("SPEED_ENEMY", "Enemy speed", "It takes enemies 1s longer to reach you.", 1, 10)
        self.player_max_hp = Upgrade("HP_PLAYER", "Max HP", "Increase your maximum HP by 1.", 5, 5)
        self.player_regen = Upgrade("REGEN_PLAYER", "Regeneration", "Restore 1 more health at the end of each wave.", 2, 0)
        self.score_multi = Upgrade("SCORE_MULTI", "Score multiplier", "Get 10% more points for every shot enemy (additive).", 5, 1)
        self.heal = Upgrade("HEAL", "Heal", "Heal yourself to full HP once.", 1, 0)
        self.summon_speed = Upgrade("SUMMON_SPEED", "Summon speed", "Decrease how frequent enemies spawn. Doesn't affect the overall amount of enemies per wave.", 3, settings.BASE_SUMMONING_CHANCE)
        self.second_upgrade = Upgrade("SECOND_UPGRADE", "Multiupgrade", "Increases the chance to get a second upgrade at the end of a wave.", 10, 0)

    def choose(self, curr_hp):
        upgrades: list[Upgrade] = [getattr(self, x) for x in self.__dict__]
        if self.min_word_length.value <= 1:
            upgrades.remove(self.min_word_length)
        if self.max_word_length.value <= self.min_word_length.value:
            upgrades.remove(self.max_word_length)
        if self.player_max_hp.value >= 10:
            upgrades.remove(self.player_max_hp)
        if self.player_regen.value >= self.player_max_hp.value-1:
            upgrades.remove(self.player_regen)
        if curr_hp >= self.player_max_hp.value:
            upgrades.remove(self.heal)
        if self.second_upgrade.value >= 100:
            upgrades.remove(self.second_upgrade)
        weights = [x.weight for x in upgrades]
        chosen: list[Upgrade] = []
        for i in range(3):
            chosen.append(choices(upgrades, weights)[0])
            weights.pop(upgrades.index(chosen[-1]))
            upgrades.remove(chosen[-1])
        shuffle(chosen)
        return chosen

    def upgrade(self, upgrade: str):
        match upgrade:
            case "MIN_ENEMY":
                self.min_word_length.value -= 1
            case "MAX_ENEMY":
                self.max_word_length.value -= 1
            case "SPEED_ENEMY":
                self.enemy_speed.value += 1
            case "HP_PLAYER":
                self.player_max_hp.value += 1
            case "REGEN_PLAYER":
                self.player_regen.value += 1
            case "SCORE_MULTI":
                self.score_multi.value = round(self.score_multi.value+0.1,1) # fp precision error handeling
            case "SUMMON_SPEED":
                self.summon_speed.value += 20
            case "SECOND_UPGRADE":
                self.second_upgrade.value += 20