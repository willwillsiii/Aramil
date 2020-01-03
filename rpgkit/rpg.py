from uuid import uuid4
import math

class Entity:
    def __init__(self):
        self.id = uuid4()

def init(ent, *args, **kwargs):
    for dictionary in args:
        for key, val in dictionary.items():
            setattr(ent, key, val)
    for key, val in kwargs.items():
        setattr(ent, key, val)


def calc_mod(ability_score):
    return math.floor((ability_score - 10) / 2)

def calc_mods(scores):
    mods = {}
    for ability, score in scores.items():
        mods[ability + '_mod'] = calc_mod(score)
    return mods

def set_ability_score_from_dict(ent, scores):
    init(ent, scores, calc_mods(scores))

def set_ability_scores(ent, strength=None, dexterity=None, constitution=None,
        intelligence=None, wisdom=None, charisma=None, default=False):
    scores_tmp = {
        'str': strength,
        'dex': dexterity,
        'con': constitution,
        'int': intelligence,
        'wis': wisdom,
        'cha': charisma
        }
    scores = {}
    for ability, score in scores_tmp.items():
        if score is None:
            if default and not hasattr(ent, ability):
                scores[ability] = 10
        else:
            scores[ability] = score
    set_ability_score_from_dict(ent, scores)


DEFAULT_HP = 0
DEFAULT_HP_TMP = 0

def update_hp_total(ent):
    hp = getattr(ent, 'hp', DEFAULT_HP)
    hp_tmp = getattr(ent, 'hp_tmp', DEFAULT_HP_TMP)
    init(ent, hp_total=hp+hp_tmp)

def set_hp(ent, current_hp):
    init(ent, hp=current_hp)
    update_hp_total(ent)

def add_hp(ent, hp):
    hp += getattr(ent, 'hp', DEFAULT_HP)
    set_hp(ent, hp)

def reset_hp(ent):
    hp_max = getattr(ent, 'hp_max', DEFAULT_HP)
    set_hp(ent, hp_max)

def set_hp_max(ent, max_hitpoints, current_hp=None, start_full=True):
    init(ent, hp_max=max_hitpoints)
    # set hp to max by default without overwriting
    if current_hp is None:
        if start_full and not hasattr(ent, 'hp'):
            set_hp(ent, max_hitpoints)
    else:
        set_hp(ent, current_hp)
    update_hp_total(ent)

def add_hp_max(ent, hp_max):
    hp_max += getattr(ent, 'hp_max', DEFAULT_HP)
    set_hp_max(ent, hp_max)

def set_hp_tmp(ent, hp):
    init(ent, hp_tmp=hp)
    update_hp_total(ent)

def reset_hp_tmp(ent):
    set_hp_tmp(ent, 0)

def add_hp_tmp(ent, hp):
    hp += getattr(ent, 'hp_tmp', DEFAULT_HP_TMP)
    set_hp_tmp(ent, hp)

def reset_all_hp(ent):
    reset_hp(ent)
    reset_hp_tmp(ent)

def heal(ent, heal_hp):
    hp_max = getattr(ent, 'hp_max', math.inf)
    hp_current = getattr(ent, 'hp', DEFAULT_HP)
    healable_hp = hp_max - hp_current
    heal_hp = min(heal_hp, healable_hp)
    add_hp(ent, heal_hp)

def damage(ent, dealt):
    hp_tmp = getattr(ent, 'hp_tmp', DEFAULT_HP_TMP)
    hp_tmp_damage = min(dealt, hp_tmp)
    add_hp_tmp(ent, -hp_tmp_damage)
    dealt -= hp_tmp_damage
    hp_current = getattr(ent, 'hp', DEFAULT_HP)
    hp_damage = min(dealt, hp_current)
    add_hp(ent, -hp_damage)
