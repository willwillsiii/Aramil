from uuid import uuid4
import math
import itertools

# consider using an update list for each stat
# when each stat is reset,
# all of the functions in the list would be called
# this would make it easier to keep track of calculated values
# such as total weight and total hp

class Entity:
    def __init__(self):
        self.id = uuid4()

def init(ent, *args, **kwargs):
    for dictionary in args:
        for key, val in dictionary.items():
            setattr(ent, key, val)
    for key, val in kwargs.items():
        setattr(ent, key, val)


DEFAULT_WT = 0

def set_wt(ent, weight):
    init(ent, wt=weight)
    update_total_wt(ent)

def update_total_wt(ent):
    wt = getattr(ent, 'wt', DEFAULT_WT)
    inv_wt = getattr(ent, 'inv_wt', DEFAULT_WT)
    init(ent, total_wt=wt+inv_wt)


DEFAULT_LVL = 1

def set_level(ent, lvl=DEFAULT_LVL, prof=False):
    init(ent, level=lvl)
    if prof or hasattr(ent, 'prof_mod'):
        reset_prof_mod(ent)

def add_level(ent, level=1):
    current_level = getattr(ent, 'level', DEFAULT_LVL)

def reset_level(ent):
    set_level(ent, DEFAULT_LVL)

def calc_prof_mod(level):
    return math.floor((level + 7) / 4)

def set_prof_mod(ent, mod):
    init(ent, prof_mod=mod)

def add_prof_mod(ent, mod=1):
    level = getattr(ent, 'level', DEFAULT_LVL)
    prof_mod = getattr(ent, 'prof_mod', calc_prof_mod(level))
    set_prof_mod(ent, prof_mod + mod)

def reset_prof_mod(ent):
    level = getattr(ent, 'level', DEFAULT_LVL)
    set_prof_mod(ent, calc_prof_mod(ent, level))


DEFAULT_HP = 0
DEFAULT_HP_TMP = 0

def set_hp(ent, current_hp=DEFAULT_HP):
    init(ent, hp=current_hp)
    update_total_hp(ent)

def add_hp(ent, hp=1):
    hp += getattr(ent, 'hp', DEFAULT_HP)
    set_hp(ent, hp)

def reset_hp(ent):
    hp_max = getattr(ent, 'hp_max', DEFAULT_HP)
    set_hp(ent, hp_max)

def set_hp_max(ent, max_hitpoints=DEFAULT_HP,
        current_hp=None, start_full=True):
    init(ent, hp_max=max_hitpoints)
    # set hp to max by default without overwriting
    if current_hp is None:
        if start_full and not hasattr(ent, 'hp'):
            set_hp(ent, max_hitpoints)
    else:
        set_hp(ent, current_hp)
    update_total_hp(ent)

def add_hp_max(ent, hp_max=1):
    hp_max += getattr(ent, 'hp_max', DEFAULT_HP)
    set_hp_max(ent, hp_max)

def set_hp_tmp(ent, hp=DEFAULT_HP_TMP):
    init(ent, hp_tmp=hp)
    update_total_hp(ent)

def reset_hp_tmp(ent):
    set_hp_tmp(ent, DEFAULT_HP_TMP)

def add_hp_tmp(ent, hp=1):
    hp += getattr(ent, 'hp_tmp', DEFAULT_HP_TMP)
    set_hp_tmp(ent, hp)

def update_total_hp(ent):
    hp = getattr(ent, 'hp', DEFAULT_HP)
    hp_tmp = getattr(ent, 'hp_tmp', DEFAULT_HP_TMP)
    init(ent, total_hp=hp+hp_tmp)

def reset_all_hp(ent):
    reset_hp(ent)
    reset_hp_tmp(ent)

def heal(ent, heal_hp=1):
    hp_max = getattr(ent, 'hp_max', math.inf)
    hp_current = getattr(ent, 'hp', DEFAULT_HP)
    healable_hp = hp_max - hp_current
    heal_hp = min(heal_hp, healable_hp)
    add_hp(ent, heal_hp)

def damage(ent, dealt=1):
    hp_tmp = getattr(ent, 'hp_tmp', DEFAULT_HP_TMP)
    hp_tmp_damage = min(dealt, hp_tmp)
    add_hp_tmp(ent, -hp_tmp_damage)
    dealt -= hp_tmp_damage
    hp_current = getattr(ent, 'hp', DEFAULT_HP)
    hp_damage = min(dealt, hp_current)
    add_hp(ent, -hp_damage)


DEFAULT_ABILITY_SCORE = 10

def calc_mod(ability_score):
    return math.floor((ability_score - 10) / 2)

def calc_mods(scores):
    mods = {}
    for ability, score in scores.items():
        mods[ability + '_mod'] = calc_mod(score)
    return mods

def set_ability_scores_from_dict(ent, scores):
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
                scores[ability] = DEFAULT_ABILITY_SCORE
        else:
            scores[ability] = score
    set_ability_scores_from_dict(ent, scores)

def add_ability_scores_from_dict(ent, scores_to_add):
    new_scores = {}
    for ability, score in scores_to_add.items():
        old_score = getattr(ent, ability, DEFAULT_ABILITY_SCORE)
        new_scores[ability] = old_score + score
    set_ability_scores_from_dict(ent, new_scores)

def add_ability_scores(ent, strength=None, dexterity=None, constitution=None,
        intelligence=None, wisdom=None, charisma=None):
    scores_tmp = {
        'str': strength,
        'dex': dexterity,
        'con': constitution,
        'int': intelligence,
        'wis': wisdom,
        'cha': charisma
        }
    scores_to_add = {}
    for ability, score in scores_tmp.items():
        if score is not None:
            scores_to_add[ability] = score
    add_ability_scores_from_dict(ent, scores_to_add)

def get_score_dict(ent, fill=False):
    score_dict = {}
    abilities = ('str', 'dex', 'con', 'int', 'wis', 'cha')
    if fill:
        for ability in abilities:
            score_dict[ability] = getattr(ent, ability, None)
    else:
        for ability in abilities:
            if hasattr(ent, ability):
                score_dict[ability] = getattr(ent, ability)
    return score_dict


def set_jack_of_all_trades(ent, has):
    init(ent, jack_of_all_trades=has)
    # probably want this to work with a dictionary or list of proficiencies


DEFAULT_INV = []

def set_inv(ent, current_inv):
    init(ent, inv=current_inv)
    update_inv_wt(ent)

def add_item_to_inv(ent, item):
    inv = getattr(ent, 'inv', DEFAULT_INV).copy()
    inv.append(item)
    set_inv(ent, inv)

def add_items_to_inv(ent, items):
    inv = getattr(ent, 'inv', DEFAULT_INV).copy()
    inv.extend(items)
    set_inv(ent, inv)

def update_inv_wt(ent):
    weight = 0
    inv = getattr(ent, 'inv', DEFAULT_INV).copy()
    for item in inv:
        weight += getattr(item, 'total_wt', DEFAULT_WT)
    init(ent, inv_wt=weight)
    update_total_wt(ent)


def turn_gen(initiative_dict, surprisers=None, start_at=None,
        start_round=None, start_turn=None):
    if start_at is not None:
        if start_round is None:
            start_round = start_at[0]
        if start_turn is None:
            start_turn = start_at[1]
    if start_round is None:
        start_round = 0
    if start_round < 0:
        raise ValueError(f'Negative "start_round" given: "{start_round}"')
    include_surprise_round = False
    if start_round == 0:
        if surprisers is not None and (
            start_turn is None or start_turn in surprisers):
            include_surprise_round = True
            surprise_turn_order = sorted(surprisers,
                key=initiative_dict.__getitem__, reverse=True)
            surprise_turns = ((0, turn) for turn in surprise_turn_order)
        start_round = 1
    turn_order = sorted(initiative_dict,
        key=initiative_dict.__getitem__, reverse=True)
    turns = ((current_round, current_turn)
            for current_round in itertools.count(start_round)
            for current_turn in turn_order)
    if include_surprise_round:
        turns = itertools.chain(surprise_turns, turns)
    if start_turn:
        if start_turn not in initiative_dict:
            raise ValueError("Supplied starting turn is not valid.")
        turns = itertools.dropwhile(lambda turn: turn[1] != start_turn, turns)
    return turns
