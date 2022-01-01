from functools import singledispatch
import random
import collections
import re

def roll_dice(max_val=20, num_dice=1):
    """Returns a list of random dice rolls.

    Keyword arguments:
    max_val -- maximum value of the dice (default 20)
    num_dice -- number of dice to roll (default 1)
    """
    # check inputs
    if max_val <= 0 or not isinstance(max_val, int):
        raise ValueError(f"{max_val}-sided die does not have a positive"
                         " integer number of faces.")
    if num_dice <= 0 or not isinstance(num_dice, int):
        raise ValueError(f"{num_dice} dice is not a positive integer"
                         " number of dice.")
    if max_val > 200:
        raise ValueError(f"{max_val}-sided die is too large."
                         " Maximum sides is 200.")
    if num_dice > 100:
        raise ValueError(f"{num_dice} dice is too many."
                         " Only roll up to 100 dice at once.")
    return [random.randint(1, max_val) for die in range(num_dice)]

def mod_roll(roll_str):
    """Modify a roll to normalize and expand abbreviations"""
    roll_str = roll_str.lower()
    if roll_str == '': roll_str = 'd'
    num_dice, rest = tuple(roll_str.split('d'))
    keep_str = ''
    if 'h' in rest:
        max_val, keep_str = tuple(rest.split('h'))
        keep_str = 'h' + keep_str
    elif 'l' in rest:
        max_val, keep_str = tuple(rest.split('l'))
        keep_str = 'L' + keep_str
    else:
        max_val = rest
    # set defaults
    if num_dice == '': num_dice = '1'
    if max_val == '': max_val = '20'
    if keep_str.endswith('h') or keep_str.endswith('L') or (
            keep_str.endswith('!')):
        keep_str = keep_str + '1'
    # check for decimals
    if '.' in num_dice:
        raise ValueError(f"invalid literal for int() with base 10: {num_dice}")
    if '.' in max_val:
        raise ValueError(f"invalid literal for int() with base 10: {max_val}")
    mod_roll_str = f'{num_dice}d{max_val}{keep_str}'
    Roll = collections.namedtuple('Roll', ['roll_str', 'num_dice',
                                           'max_val', 'keep_str'])
    return Roll(mod_roll_str, num_dice, max_val, keep_str)

def sort_and_trim(vals, keep):
    """Returns a sorted subset of values and the indices of the subset.

    Arguments:
    vals -- values to sort
    keep -- which values to keep
    """
    keep = keep.lower()
    trim_ndcs = sorted(range(len(vals)), key=vals.__getitem__)
    num_keep = int(keep[1:].replace('!', '-'))
    if num_keep < 0:
        if keep.startswith('h'):
            keep = keep.replace('h', 'l')
        elif keep.startswith('l'):
            keep = keep.replace('l', 'h')
        num_keep = len(vals) + num_keep
    if keep.startswith('h'):
        trim_ndcs = trim_ndcs[-num_keep:]
    elif keep.startswith('l'):
        trim_ndcs = trim_ndcs[:num_keep]
    vals = [vals[i] for i in trim_ndcs]
    return vals, trim_ndcs

def chat_roll_single(roll_str='', verbose=False, formatted=False):
    """Interpet and compute rolls from a string.
    
    Keyword arguments:
    roll_str -- what to interpret as a roll (default '')
    verbose -- whether each roll is returned (default False)
    formatted -- whether to format for Discord (default false)
    """
    mod_msg = []
    verbose_msg = []
    re_single_space = re.compile(r"\s+")
    roll_str = re_single_space.sub(" ", roll_str).lower().strip()
    roll_list = re.split(r'([\s\+\-\*/()])', roll_str)
    roll_list = list(filter(None, roll_list))
    if roll_list == []: roll_list = ['d']
    for i in range(len(roll_list)):
        if 'd' in roll_list[i]:
            roll = mod_roll(roll_list[i])
            mod_msg.append(roll.roll_str)
            roll_res = roll_dice(int(roll.max_val), int(roll.num_dice))
            if roll.keep_str:
                roll_res_trimmed, trim_ndcs = sort_and_trim(roll_res,
                                                            roll.keep_str)
                roll_sum = sum(roll_res_trimmed)
            else:
                roll_sum = sum(roll_res)
            if verbose:
                if formatted:
                    if roll.keep_str:
                        verbose_msg.append("**[")
                        # Handle the first roll separate in case it also
                        # needs to be bold. This prevents duplicate
                        # asterisks with the opening bracket.
                        verbose_msg.append(f"{roll_res[0]}**"
                            if 0 in trim_ndcs else f"**{roll_res[0]}")
                        verbose_msg.append(", ")
                        # Iterate through the middle.
                        verbose_msg.extend([f"**{roll_res[n]}**, " if n in
                                            trim_ndcs else f"{roll_res[n]}, "
                                            for n in range(1,
                                                           len(roll_res) - 1)])
                        # Handle the last roll separately as well.
                        verbose_msg.append(f"**{roll_res[-1]}"
                            if len(roll_res) - 1 in trim_ndcs
                            else f"{roll_res[-1]}**")
                        verbose_msg.append("]**")
                    else:
                        verbose_msg.append(f"**{roll_res}**".replace(
                            ", ", "**, **"))
                    if not (roll.num_dice == '1' or (roll.keep_str and
                                                     len(trim_ndcs) == 1)):
                        verbose_msg.append(f"{{{roll_sum}}}")
                else:
                    verbose_msg.append(f"{roll_res}{{{roll_sum}}}")
            roll_list[i] = str(roll_sum)
        else:
            safe = '\\' + roll_list[i] if (
                formatted and roll_list[i] in '*') else roll_list[i]
            mod_msg.append(safe)
            if verbose:
                verbose_msg.append(safe)
    if verbose:
        verbose_msg.extend(" = ")
    return_msg = mod_msg.copy()
    return_msg.append(" = ")
    return_msg.extend(verbose_msg.copy())
    result_str = str(eval(''.join(roll_list)))
    return_msg.append(f"**{result_str}**" if formatted else result_str)
    return ''.join(return_msg)

def parse_repeated_rolls(roll_str):
    roll_list = re.split('([,{}])', roll_str, 1)
    if len(roll_list) != 1:
        delim = roll_list.pop(1)
        if delim == ',':
            roll_list.extend(roll_list.pop(1).split(';', 1))
            repeated_roll = roll_list[0]
            num_times = int(roll_list[1])
            parsed_str = '; '.join([repeated_roll]*num_times)
            if len(roll_list) == 3:
                parsed_str = ''.join([parsed_str, ';',
                    parse_repeated_rolls(roll_list[2])])
        elif delim == '{':
            # counting to remove braces and recurse
            nest = 1
            close_index = None
            for i in range(len(roll_list[1])):
                char = roll_list[1][i]
                if char == '{':
                    nest += 1
                if char == '}':
                    nest -= 1
                if nest == 0:
                    close_index = i
                    # append rest of string to roll_list only if exists
                    if i != len(roll_list[1]) - 1:
                        roll_list.append(roll_list[1][i+1:])
                    roll_list[1] = roll_list[1][:i]
                    break
            if close_index == None:
                raise ValueError("Unmatched brace(s).")
            roll_list[1] = parse_repeated_rolls(roll_list[1])
            if len(roll_list) == 3:
                roll_list[1] = parse_repeated_rolls(''.join(roll_list[1:]))
                del roll_list[2]
            parsed_str = ''.join(roll_list)
        else:
            # delim == '}'
            raise ValueError("Unmatched brace(s).")
    else:
        parsed_str = roll_str
    return parsed_str

def chat_roll(roll_str='', verbose=False, formatted=False):
    """General purpose wrapper function for chat_roll_single."""
    # parse comment
    hashtag_index = roll_str.find('#')
    comment = ""
    if hashtag_index != -1:
        roll_str, comment = roll_str.split('#', 1)
    # parse for macros
    macros = {
             'stats' : '{4d6L!1, 6}',
             'stat' : '4d6L!',
             'disadvantage' : '2d20L1',
             'dis' : '2d20L1',
             'advantage' : '2d20h1',
             'adv' : '2d20h1'
             }
    for key, value in macros.items():
        re_macro = re.compile(re.escape(key), re.IGNORECASE)
        roll_str = re_macro.sub(value, roll_str)
    # parse for repeated rolls
    roll_str = parse_repeated_rolls(roll_str)
    # parse input by commas, call chat_roll_single on each token
    chat_list = roll_str.split(';')
    rolls = []
    for roll in chat_list:
        if '|' in roll:
            roll_str, indv_comment = tuple(roll.split('|', 1))
            indv_comment = indv_comment.strip()
            rolls.append(''.join([indv_comment, ': ',
                chat_roll_single(roll_str, verbose, formatted)]))
        else:
            rolls.append(chat_roll_single(roll, verbose, formatted))
    return (comment.strip() + "\n" +
            "\n".join(rolls)) if comment else "\n".join(rolls)

def roll(roll_str=''):
    """Wrapper around chat_roll for command line use.
    Returns a number for a single roll,
    or a tuple for multiple rolls."""
    chat_result = chat_roll(roll_str, verbose=False, formatted=False)
    if '\n' in chat_result:
        result = [int(res.split()[-1]) for res in chat_result.splitlines()]
    else:
        result = int(chat_result.split()[-1])
    return result
